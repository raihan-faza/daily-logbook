from ninja import Schema


class LogbookIn(Schema):
    title: str
    details: str


class UserIn(Schema):
    username: str
    password: str


class AiGenIn(Schema):
    query: str
