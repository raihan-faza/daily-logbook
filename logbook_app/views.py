from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from ninja import NinjaAPI

from .auth import generate_jwt_token
from .models import Log
from .parser import ORJSONParser
from .schema import LogbookIn, UserIn

api = NinjaAPI(version="1.0.0", parser=ORJSONParser())


@api.get("/logbooks")
async def get_logbooks(request):
    logbooks = [model_to_dict(logbook) async for logbook in Log.objects.all()]
    res = {"status": 200, "data": logbooks}
    return JsonResponse(res)


@api.get("/logbook")
async def get_logbook(request, logbook_id):
    try:
        logbook = await Log.objects.aget(id=logbook_id)
        res = {
            "status": 200,
            "message": "logbook retrieved.",
            "data": model_to_dict(logbook),
        }
    except:
        res = {"status": 400, "message": "Invalid Data"}
    return JsonResponse(res)


@api.post("/logbook")
async def create_logbook(request, payload: LogbookIn):
    try:
        logbook = await Log.objects.acreate(**payload.dict())
        res = {
            "status": 200,
            "message": "logbook created.",
            "data": model_to_dict(logbook),
        }
    except:
        res = {"status": 400, "message": "Invalid Data"}
    return JsonResponse(res)


@api.put("/logbook")
async def update_logbook(request, logbook_id: int):
    try:
        logbook = await Log.objects.aget(id=logbook_id)
        res = {
            "status": 200,
            "message": "logbook updated.",
            "data": model_to_dict(logbook),
        }
    except:
        res = {"status": 400, "message": "logbook not found."}
    return JsonResponse(res)


@api.delete("/logbook/")
async def delete_logbook(request, logbook_id: int):
    try:
        logbook = await Log.objects.aget(id=logbook_id)
        await logbook.adelete()
        res = {"status": 200, "message": "logbook deleted."}
    except:
        res = {"status": 400, "message": "logbook not found."}
    return JsonResponse(res)


@api.post("/user")
async def create_user(request, payload: UserIn):
    try:
        await sync_to_async(User.objects.create_user)(**payload.dict())
        res = {"status": 200, "message": f"user created."}
    except:
        res = {"status": 400, "message": "invalid data."}
    return JsonResponse(res)


@api.post("/token")
async def login(request, payload: UserIn):
    res = {"status": 400, "message": "invalid user."}
    try:
        user = await User.objects.aget(**payload.dict())
        if not user.is_authenticated:
            return JsonResponse(res)
        token = await generate_jwt_token(user=user)
        res = {"status": 200, "token": token}
    except:
        pass
    return JsonResponse(res)
