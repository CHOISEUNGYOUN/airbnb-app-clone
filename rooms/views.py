# from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    elif request.method == "POST":
        if request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
        # class ListRoomsView(ListAPIView):

        #     queryset = Room.objects.all()
        #     serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer