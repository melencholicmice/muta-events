import bcrypt

def hash_password(password: str) -> str:
    """
    Generate a hashed password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hashed version using bcrypt.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    print(password, hashed_password)    
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
