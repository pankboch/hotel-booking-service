from django.http import JsonResponse


def json_response(data: dict, status: int = 200) -> JsonResponse:
    return JsonResponse(
        data=data,
        status=status,
        json_dumps_params={"ensure_ascii": False, "indent": 4},
        content_type="application/json; charset=utf-8",
    )
