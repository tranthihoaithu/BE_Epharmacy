

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView


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


def get_detail_medicine(request, id_medicine):
    medicine = get_object_or_404(Medicine, id_medicine=id_medicine)
    return JsonResponse(medicine.to_dict())


class CartViewSet(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, ]
    serializer_class = CartSerializer

    def post(self, request):
        # Check if the POST request contains the id_medicine parameter
        if 'id_medicine' in request.data:
            id_medicine = request.data['id_medicine']

            # Get the medicine information from the database
            medicine_info = get_detail_medicine(request, id_medicine)

            if medicine_info:
                # Create or update the cart object in the database
                cart, created = Cart.objects.get_or_create(user=request.user, id_medicine=id_medicine)

                # If the product already exists in the cart, update the quantity
                if not created:
                    cart.quantity += 1
                else:
                    cart.quantity = 1  # If the product does not exist, set the quantity to 1
                # Save the cart in the database
                cart.save()
                data = {
                    'name': medicine_info['name'],
                    'price': medicine_info['price'],
                    'quantity': cart.quantity
                }

                # Serialize the cart object

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                # Handle the case where the medicine information cannot be retrieved
                return Response({"message": "Failed to retrieve medicine information"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle the case where the id_medicine parameter is missing in the POST request
            return Response({"message": "Missing id_medicine parameter"}, status=status.HTTP_400_BAD_REQUEST)

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



