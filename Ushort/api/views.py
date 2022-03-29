from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

# local imports
from Ushort.api.serializers import UrlCreateSerializer
from Ushort.models import Url, Creator


@api_view(["POST"])
def url_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            serializer = UrlCreateSerializer(request.data or None)
            creator = Creator.objects.get(user=request.user)
            try:
                Url.objects.create(creator=creator, **serializer.data)
            except Exception as e:
                return Response(e)
    else:
        return redirect("Ushot:login")

    return Response(serializer.data)
