from pathlib import Path

from pydantic import BaseModel

cwd = Path.cwd()


class AuthJWT(BaseModel):
    private_key_path: Path = cwd / 'certs' / 'jwt-private.pem'
    public_key_path: Path = cwd / 'certs' / 'jwt-public.pem'
    algorithm: str = "RS256"


class Settings:
    auth: AuthJWT = AuthJWT()
