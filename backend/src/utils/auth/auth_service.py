from datetime import datetime  # used to handle expiry time for tokens
from datetime import timedelta

import jwt  # used for encoding and decoding jwt tokens
from fastapi import HTTPException  # used to handle error handling
from fastapi import Request
from passlib.context import CryptContext

from settings import SECRET  # used for hashing the password


class AuthService:
    hasher = CryptContext(schemes=["bcrypt"])
    secret = SECRET

    def verify_credentials(self, req: Request):
        credentials = req.headers["Authorization"].split(" ")[1]
        if self.decode_token(credentials):
            return True
        else:
            return False

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=5, minutes=0),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError as error:
            raise HTTPException(status_code=401, detail="Token expired") from error
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=401, detail="Invalid token") from error

    def encode_refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError as error:
            raise HTTPException(status_code=401, detail="Refresh token expired") from error
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=401, detail="Invalid refresh token") from error
