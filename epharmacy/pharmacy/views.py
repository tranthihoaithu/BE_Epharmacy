import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Medicine, User, OrderItem, Cart
from .serializer import MedicineSerializer, UserSerializer, LoginSerializer, OrderSerializer, CartSerializer
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
            user = serializer.validated_data  # Lấy đối tượng người dùng từ dữ liệu đã xác thực
            if user:  # Kiểm tra xem người dùng đã tồn tại không
                refresh = RefreshToken.for_user(user)  # Tạo RefreshToken cho người dùng đã xác thực
                access_token = refresh.access_token # Lấy mã token truy cập từ RefreshToken

            return Response({
                'user': {
                    'username': user.username,
                    'email': user.email,
                },
                'access_token': str(access_token),
            }, status=status.HTTP_200_OK)
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
    try:
        medicine = Medicine.objects.get(id_medicine=id)
        return JsonResponse(medicine.to_dict())
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'No Medicine matches the given query.'}, status=404)

# @login_required
# def add_to_cart(request, medicine_id):
#     try:
#         medicine = Medicine.objects.get(id=medicine_id)
#         cart_item, created = Cart.objects.get_or_create(medicine=medicine, user=request.user)
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()
#         else:
#             cart_item.quantity = 1
#             cart_item.save()
#         serializer_class = CartSerializer(cart_item)
#         return JsonResponse(serializer_class.data, status=status.HTTP_201_CREATED)
#
#     except Medicine.DoesNotExist:
#         return JsonResponse({'error': 'No Medicine matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


class CartViewSet(APIView):
    def post(self, request):
        try:
            # fix
            body_data = json.loads(request.body)
            username = body_data.get("username")
            medicine_id = body_data.get("medicine_id")
            # fix

            medicine = Medicine.objects.get(id_medicine=medicine_id)
            user = User.objects.get(username=username)
            cart_item, created = Cart.objects.get_or_create(medicine=medicine, user=user)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item.quantity = 1
                cart_item.save()
            serializer_class = CartSerializer(cart_item)
            return JsonResponse(serializer_class.data, status=status.HTTP_201_CREATED)

        except Medicine.DoesNotExist:
            return JsonResponse({'error': 'No Medicine matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(APIView):
    serializer_class = OrderSerializer
    parser_classes = [MultiPartParser, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in request.session['cart']:
                medicine = Medicine.objects.get(pk=item['medicine'])
                OrderItem.objects.create(
                    medicine=medicine,
                    order=order,
                    quantity=item['quantity'],
                    price=medicine.price
                )
            del request.session['cart']  # Move this line outside the loop
            return JsonResponse(serializer.data)
        else:
            return Response(serializer.errors)


class SearchResultsView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')  # Lấy tham số tìm kiếm từ URL
        all_medicines = Medicine.objects.filter(name_medicine=query)  # Tìm kiếm sản phẩm theo tên
        medicines_list = []  # Danh sách kết quả

        # Format kết quả dưới dạng JSON
        for medicine in all_medicines:
            medicines_list.append(medicine.to_dict())

        return JsonResponse(medicines_list, safe=False)

# def place_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
#             # Lưu thông tin chi tiết đơn hàng
#             for item in request.session['cart']:
#                 product = Product.objects.get(pk=item['product_id'])
#                 OrderItem.objects.create(
#                     order=order,
#                     product=product,
#                     quantity=item['quantity'],
#                     price=product.price
#                 )
#             # Xóa giỏ hàng sau khi đặt hàng
#             del request.session['cart']
#             return redirect('order_success')
#     else:
#         form = OrderForm()
#     return render(request, 'place_order.html', {'form': form})



