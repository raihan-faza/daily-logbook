from django.http.response import JsonResponse
from ninja import NinjaAPI

from .models import Log
from .schema import LogbookIn

# Logbook manual crud
api = NinjaAPI(version="1.0.0")


@api.get("/logbooks")
async def get_logbooks(request):
    logbooks = {logbook async for logbook in Log.objects.all()}
    res = {"status": 200, "data": logbooks}
    return JsonResponse(res)


async def create_logbooks(request, payload: LogbookIn):
    logbook = await Log.objects.acreate(**payload.dict())
    res = {"status": 200, "data": logbook}
    return JsonResponse(res)
