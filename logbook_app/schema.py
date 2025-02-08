from ninja import Schema


class LogbookIn(Schema):
    title: str
    details: str


class UserIn(Schema):
    username: str
    password: str


class AiGenIn(Schema):
    query: str


class TokenRequest(Schema):
    username: str
    password: str


class RefreshRequest(Schema):
    refresh_token: str


# Response Schema
class TokenResponse(Schema):
    access_token: str
    refresh_token: str
