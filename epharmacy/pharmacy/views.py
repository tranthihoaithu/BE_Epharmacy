from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Medicine, User
from .serializer import MedicineSerializer, UserSerializer
from rest_framework.parsers import MultiPartParser


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
            return[permissions.AllowAny()]
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

