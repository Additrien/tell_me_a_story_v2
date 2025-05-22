import pytest
from app.models.user import User

def test_create_user_instance():
    """
    Test creating a User instance and checking its attributes.
    """
    email = "test@example.com"
    hashed_password = "hashedpassword123"
    
    user = User(email=email, hashed_password=hashed_password)
    
    assert user.email == email
    assert user.hashed_password == hashed_password
    assert user.id is None # ID would be set by the database

def test_user_tablename():
    """
    Test if the tablename is correctly set.
    """
    assert User.__tablename__ == "users"
