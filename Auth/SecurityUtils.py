from datetime import datetime, timedelta, UTC

import bcrypt
import jwt

from Auth.config import Settings


def encode_jwt(payload: dict, private_key: str = Settings.auth.private_key_path.read_text(),
               algorithm: str = Settings.auth.algorithm) -> str:
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=15)
    payload["exp"] = expire
    payload["iat"] = now
    encode = jwt.encode(payload, private_key, algorithm=algorithm)
    return encode


def decode_jwt(
        token: str | bytes,
        public_key: str = Settings.auth.public_key_path.read_text(),
        algorithm: str = Settings.auth.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_pw: bytes = password.encode("utf8")
    return bcrypt.hashpw(bytes_pw, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode("utf8"), hashed_password=hashed_password)
