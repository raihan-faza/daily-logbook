from ninja import Schema


class LogbookIn(Schema):
    title: str
    details: str
