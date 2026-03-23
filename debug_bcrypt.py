from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    password = "test123"
    print(f"Testing password: {password}")
    hashed = pwd_context.hash(password)
    print(f"Hash success: {hashed}")
except Exception as e:
    print(f"Error: {e}")

try:
    long_pass = "a" * 80
    print(f"\nTesting long password (80 chars)")
    hashed = pwd_context.hash(long_pass)
    print(f"Hash success: {hashed}")
except Exception as e:
    print(f"Error with long pass: {e}")
