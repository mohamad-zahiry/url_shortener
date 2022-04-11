from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from Ushort.api.serializers import UrlCreateSerializer
from Ushort.models import Creator


@login_required(login_url="Ushort:login")
@api_view(["POST"])
def url_add(request):
    serializer = UrlCreateSerializer(data=request.data)
    creator = Creator.by_request(request)

    if creator:
        if serializer.is_valid():
            serializer.save(creator=creator)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
