from passlib.context import CryptContext
import bcrypt

# Configure password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt",
    bcrypt__ident="2b",  # Use the more secure 2b identifier
    bcrypt__rounds=12,   # Number of hashing rounds
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if not password:
        raise ValueError("Password cannot be empty")
    # Ensure password is encoded to bytes and not too long for bcrypt
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Truncate password if it's too long for bcrypt (72 bytes max)
    if len(password) > 72:
        password = password[:72]
    # Hash the password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    if not plain_password or not hashed_password:
        return False
    # Ensure both are in bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    # Truncate password if it's too long for bcrypt (72 bytes max)
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password, hashed_password)
