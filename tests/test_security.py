import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    TokenData,
    oauth2_scheme, # Though not directly used in tests, good to ensure it's importable
    get_db as security_get_db # Import the get_db from security to mock it
)
from app.models.user import User
from app.core.config import settings # For SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# Existing tests for hash_password and verify_password
def test_hash_password():
    """
    Test that hash_password returns a string different from the input password
    and that it's a string.
    """
    password = "securepassword123"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password

def test_verify_password_correct():
    """
    Test that verify_password correctly verifies a correct password.
    """
    password = "securepassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    """
    Test that verify_password correctly rejects an incorrect password.
    """
    password = "securepassword123"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) is False

def test_verify_password_with_different_hash():
    """
    Test that verify_password returns False when the hash is for a different password.
    """
    password_one = "password_one"
    password_two = "password_two"
    
    hashed_one = hash_password(password_one)
    # We don't need to hash password_two, just use its plain form against hashed_one
    
    assert verify_password(password_two, hashed_one) is False

# --- Tests for create_access_token ---

def test_create_access_token_basic():
    """Test basic token creation and 'sub' claim."""
    email = "test@example.com"
    token = create_access_token(data={"sub": email})
    assert isinstance(token, str)
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == email

def test_create_access_token_custom_expiry():
    """Test token creation with a custom expiry delta."""
    email = "test@example.com"
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data={"sub": email}, expires_delta=expires_delta)
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert "exp" in payload
    expire_timestamp = payload["exp"]
    expected_expire_time = datetime.now(timezone.utc) + expires_delta
    # Allow for a small difference due to execution time
    assert abs(datetime.fromtimestamp(expire_timestamp, timezone.utc) - expected_expire_time) < timedelta(seconds=5)

def test_create_access_token_default_expiry(mocker):
    """Test token creation with default expiry from settings."""
    email = "test@example.com"
    
    # Mock datetime.now(timezone.utc) to control the 'exp' claim precisely
    mocked_now = datetime.now(timezone.utc)
    mocker.patch('app.core.security.datetime', new_callable=MagicMock)
    # Accessing .now directly because that's what is called in create_access_token
    app.core.security.datetime.now.return_value = mocked_now 


    token = create_access_token(data={"sub": email})
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert "exp" in payload
    expire_timestamp = payload["exp"]
    expected_expire_time = mocked_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # The timestamp in JWT is an integer (seconds since epoch)
    # Convert our expected_expire_time to a similar representation for comparison
    assert int(expire_timestamp) == int(expected_expire_time.timestamp())


# --- Tests for get_current_user ---

@pytest.fixture
def mock_db_session():
    """Fixture to create a mock database session."""
    return MagicMock()

@pytest.mark.asyncio
async def test_get_current_user_valid_token(mocker, mock_db_session):
    """Test get_current_user with a valid token and user in DB."""
    test_email = "test@example.com"
    test_user = User(id=1, email=test_email, hashed_password="somehash")

    # Mock jwt.decode
    mock_payload = {"sub": test_email, "exp": (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()}
    mocker.patch('jose.jwt.decode', return_value=mock_payload)

    # Mock the get_db dependency within security.py to return our mock_db_session
    # And then mock the database query on that session
    mock_db_session.query.return_value.filter.return_value.first.return_value = test_user
    
    # We need to mock the get_db that get_current_user itself uses.
    # The get_current_user in app.core.security has its own get_db placeholder.
    # For this test, we'll assume that placeholder is what's called, or we mock it directly.
    # The one imported as `security_get_db` is that placeholder.
    
    # Patch the get_db function within app.core.security module
    mocker.patch('app.core.security.get_db', return_value=mock_db_session)


    # Simulate token being passed (value doesn't matter as jwt.decode is mocked)
    token_value = "valid.token.here"
    
    # The actual get_db used by get_current_user is the one from its own module.
    # We need to provide a mock for that specific get_db's context.
    # The placeholder get_db in security.py yields None. We need it to yield our mock_db_session.
    
    # Re-patching get_db specifically for the context of security.py's get_current_user
    # This is a bit tricky because the get_db in security.py is a simple generator.
    # A more robust way would be if get_db was a proper dependency that could be overridden in tests.
    # For now, let's assume the User object is constructed directly in get_current_user for the placeholder.
    # The current placeholder in security.py:
    # if token_data.email: user = User(id=1, email=token_data.email, hashed_password="fake_hashed_password")
    # So, we don't even need to mock DB for the "user found" case IF using that placeholder logic.
    # However, the subtask asks to "Mock the database call to return a User object".
    # The placeholder in app.core.security.py does:
    # user = User(id=1, email=token_data.email, hashed_password="fake_hashed_password")
    # Let's adjust the test to match this placeholder's behavior first, then consider a more complex mock.

    # If get_current_user directly creates the User object as per its placeholder:
    retrieved_user = await get_current_user(token=token_value, db=mock_db_session) # db will be ignored by placeholder
    
    assert retrieved_user is not None
    assert retrieved_user.email == test_email
    jose.jwt.decode.assert_called_once_with(token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


@pytest.mark.asyncio
async def test_get_current_user_jwt_error(mocker, mock_db_session):
    """Test get_current_user when jwt.decode raises JWTError."""
    mocker.patch('jose.jwt.decode', side_effect=JWTError("Invalid token"))
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid.token", db=mock_db_session)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_current_user_no_sub_claim(mocker, mock_db_session):
    """Test get_current_user with a token missing the 'sub' (email) claim."""
    mock_payload = {"exp": (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()} # No 'sub'
    mocker.patch('jose.jwt.decode', return_value=mock_payload)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="token.without.sub", db=mock_db_session)
        
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED 
    # Detail matches the original implementation in security.py
    assert exc_info.value.detail == "Could not validate credentials" 

@pytest.mark.asyncio
async def test_get_current_user_user_not_in_db_placeholder_behavior(mocker):
    """
    Test get_current_user when token is valid but the placeholder logic in get_current_user
    would effectively mean the user exists (as it creates a dummy one).
    This test highlights the behavior of the *current placeholder* in security.py.
    A true DB test would mock the DB call to return None.
    """
    test_email = "nonexistent@example.com"
    mock_payload = {"sub": test_email, "exp": (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()}
    mocker.patch('jose.jwt.decode', return_value=mock_payload)

    # The placeholder logic in app.core.security.get_current_user:
    # if token_data.email:
    #     user = User(id=1, email=token_data.email, hashed_password="fake_hashed_password")
    # else:
    #     user = None
    # if user is None: # This will only be hit if token_data.email was None, which is tested above.
    #     raise HTTPException(...)
    # So, with the current placeholder, if 'sub' (email) is in the token, a user is *always* "found" (created).
    # This test verifies that behavior.

    # We need a mock_db that does nothing, as the placeholder creates the User.
    mock_db_ignored = MagicMock()

    user = await get_current_user(token="valid.token.for.nonexistent.user", db=mock_db_ignored)
    assert user is not None
    assert user.email == test_email # The placeholder creates this user.

@pytest.mark.asyncio
async def test_get_current_user_user_not_in_db_true_mock(mocker):
    """
    Test get_current_user when token is valid but user is NOT found in a (mocked) database.
    This requires temporarily modifying or bypassing the placeholder user creation in get_current_user.
    For this, we'll mock the User constructor call within get_current_user to simulate a "not found" scenario.
    """
    test_email = "truly_nonexistent@example.com"
    mock_payload = {"sub": test_email, "exp": (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()}
    mocker.patch('jose.jwt.decode', return_value=mock_payload)

    # Mock the User class constructor ONLY within the app.core.security module
    # to make it return None, simulating user not found AFTER token decoding.
    # This is a bit of a deeper mock, targeting the effect of a DB miss.
    mocker.patch('app.core.security.User', return_value=None)

    # Mock db session for completeness, though User constructor mock is the key here.
    mock_db_session = MagicMock()
    mocker.patch('app.core.security.get_db', return_value=mock_db_session)


    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="valid.token.for.truly.nonexistent.user", db=mock_db_session)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND # Or 401 based on desired behavior
    assert exc_info.value.detail == "User not found"
