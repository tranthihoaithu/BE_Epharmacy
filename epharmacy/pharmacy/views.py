

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView

from .models import Medicine, User
from .serializer import MedicineSerializer, UserSerializer, LoginSerializer
from rest_framework.parsers import MultiPartParser


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({'user': user.username, 'email': user.email, }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.ListAPIView,
                  generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]


    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.filter(active=True)
    serializer_class = MedicineSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # list(GET) --> XEM dnah sách khóa học
    #...(POST)--> THEM KHOA HOC
    #detail --> XEM CHI TIET 1 KHOA HOC
    # ...(PUT)--> cap nhat
    # ...(DELETE)--> xoa khoa hoc


def index(request):
    return render(request, template_name='index.html', context={
        'name': 'Hoai Thu'
    })


def order(request, id):
    return JsonResponse("rde", str(id))

def get_all_medicines(request):
    # Lấy tất cả các đối tượng Medicine từ cơ sở dữ liệu
    all_medicines = Medicine.objects.all()
    medicines_list = []
    for medicine in all_medicines:
        medicines_list.append(medicine.to_dict())
    # Trả về chuỗi chứa thông tin về tất cả các sản phẩm
    return JsonResponse(medicines_list, safe=False)

def get_detail_medicine(request, id):
    medicine = get_object_or_404(Medicine, id_medicine = id)
    return JsonResponse(medicine.to_dict())





