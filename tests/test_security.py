import pytest
from app.core.security import hash_password, verify_password

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
