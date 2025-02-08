import jwt
from asgiref.sync import sync_to_async
from django.contrib.auth import aauthenticate
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from ninja import NinjaAPI

from .auth import JWTAuth, generate_jwt_token
from .models import Log
from .parser import ORJSONParser
from .schema import LogbookIn, UserIn
from .utils import (
    JWT_ALGORITHM,
    JWT_EXPIRATION_TIME,
    JWT_REFRESH_EXPIRATION,
    JWT_SECRET_KEY,
)

api = NinjaAPI(version="1.0.0", parser=ORJSONParser())


@api.get("/logbooks", auth=JWTAuth())
async def get_logbooks(request):
    logbooks = [model_to_dict(logbook) async for logbook in Log.objects.all()]
    res = {
        "status": 200,
        "data": logbooks,
    }
    return JsonResponse(res)


@api.get("/logbook", auth=JWTAuth())
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


@api.post("/logbook", auth=JWTAuth())
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


@api.put("/logbook", auth=JWTAuth())
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


@api.delete("/logbook", auth=JWTAuth())
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


@api.post("/login", response=TokenResponse)
async def login(request, data: TokenRequest):
    # Check user authentication
    try:
        user = User.objects.get(username=data.username)
        if not user.check_password(data.password):
            return api.create_response(
                request, {"error": "Invalid credentials"}, status=401
            )
    except User.DoesNotExist:
        return api.create_response(request, {"error": "User not found"}, status=401)

    access_token = await generate_jwt_token(user)

    refresh_token = await generate_jwt_token(user)

    return {"access_token": access_token, "refresh_token": refresh_token}


# Refresh Token API
@api.post("/refresh", response=TokenResponse)
async def refresh_token(request, data: RefreshRequest):
    try:
        payload = jwt.decode(
            data.refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        user = User.objects.get(pk=payload["sub"])

        new_access_token = await generate_jwt_token(user)
        return {"access_token": new_access_token, "refresh_token": data.refresh_token}
    except jwt.ExpiredSignatureError:
        return api.create_response(
            request, {"error": "Refresh token expired"}, status=401
        )
    except jwt.InvalidTokenError:
        return api.create_response(
            request, {"error": "Invalid refresh token"}, status=401
        )
    except User.DoesNotExist:
        return api.create_response(request, {"error": "User not found"}, status=401)


@api.post("/ai/generate")
async def generate_logbook_with_ai():
    return


@api.post("/ai/ask")
async def ask_question_to_ai():
    return
