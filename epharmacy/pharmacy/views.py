import json
from django.db.models import Q
from django.core.serializers import serialize
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Medicine, User, OrderItem, Cart, Order, Payment, Category
from .serializer import MedicineSerializer, UserSerializer, LoginSerializer, OrderSerializer, CartSerializer, \
    OrderItemSerializer
from rest_framework.parsers import MultiPartParser

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Tạo payload cho JWT
            user = serializer.instance
            payload = jwt_payload_handler(user)
            # Encode payload để tạo ra JWT
            token = jwt_encode_handler(payload)
            # Trả về thông tin người dùng và JWT token
            return Response({
                'user': {
                    'username': user.username,
                    'email': user.email,
                },
                'access_token': token,
            }, status=status.HTTP_201_CREATED)
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


class UserListAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Cho phép truy cập không cần xác thực

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # list(GET) --> XEM dnah sách khóa học
    #...(POST)--> THEM KHOA HOC
    #detail --> XEM CHI TIET 1 KHOA HOC
    # ...(PUT)--> cap nhat
    # ...(DELETE)--> xoa khoa hoc


def index(request):
    return render(request, template_name='index.html', context={
        'name': 'Hoai Thu'
    })

def generate_pdf(request):
    # Lấy dữ liệu hoặc context cần thiết để điền vào mẫu PDF
    context = {
        'order': Order.objects.get(id_order=1),
        'items': OrderItem.objects.all(),
    }
    template = get_template('index.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error creating PDF', status=500)
    return response


def order(request, id):
    return JsonResponse("rde", str(id))


def get_all_category(request):
    category_all = Category.objects.all()
    category_list = []
    for category in category_all:
        category_list.append({'id': category.id,'name': category.name })
    return JsonResponse(category_list, safe=False)


def get_category_medicine(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Danh mục không tồn tại'}, status=404)
    medicines_in_category = Medicine.objects.filter(category=category)
    medicines_list = []
    for medicine in medicines_in_category:
        medicines_list.append(medicine.to_dict())
    return JsonResponse(medicines_list, safe=False)


def get_all_medicines(request):
    all_medicines = Medicine.objects.all()
    medicines_list = []
    for medicine in all_medicines:
        medicines_list.append(medicine.to_dict())
    return JsonResponse(medicines_list, safe=False)


def get_detail_medicine(request, id):
    try:
        medicine = Medicine.objects.get(id_medicine=id)
        return JsonResponse(medicine.to_dict())
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'No Medicine matches the given query.'}, status=404)

def calculate_total_price(user):
    cart_items = Cart.objects.filter(user=user)
    total_price = sum(cart_item.medicine.price * cart_item.quantity for cart_item in cart_items)
    return total_price


@api_view(['POST'])
def checkout(request, username):
    try:
        # Tìm người dùng dựa trên username
        user = User.objects.get(username=username)
        payment = Payment.objects.first()
        total_price = calculate_total_price(user)
        body_data = json.loads(request.body)
        shipping_address = body_data.get("deliveryAddress")
        # Tạo một đơn đặt hàng mới
        order = Order.objects.create(user=user, payment=payment, status='pending', total_price=total_price, shipping_address=shipping_address)
        # Lặp qua các mục trong giỏ hàng và tạo OrderItem cho mỗi mục
        cart_items = Cart.objects.filter(user=user)
        for cart_item in cart_items:
            if cart_item.medicine.stock_quantity >= cart_item.quantity:
                order_item = OrderItem.objects.create(
                    id_order=order,
                    id_medicine=cart_item.medicine,
                    quantity=cart_item.quantity,
                    price=cart_item.medicine.price * cart_item.quantity
                )
                cart_item.medicine.stock_quantity -= cart_item.quantity
                cart_item.medicine.save()
            else:

                return JsonResponse({'error': 'Số lượng đặt hàng lớn hơn số lượng tồn kho của sản phẩm.'},
                                status=status.HTTP_400_BAD_REQUEST)
        # Xóa tất cả các mục trong giỏ hàng
        cart_items.delete()

        return Response({'message': 'Đã tạo đơn hàng thành công.'}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'error': 'Người dùng không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_item_cart(request, username):
    try:
        cart_items = Cart.objects.filter(user__username=username)
        serialized_data = []
        for cart_item in cart_items:
            cart_data = CartSerializer(cart_item).data
            # Lấy thông tin của sản phẩm từ liên kết khóa ngoại
            item_data = {
                'medicine_id': cart_item.medicine.id_medicine,
                'medicine_name': cart_item.medicine.name_medicine,
                'medicine_price': cart_item.medicine.price,
                'medicine_img': serialize('python', [cart_item.medicine])[0]['fields'].get("image"),

            }
            cart_data['medicine'] = item_data
            serialized_data.append(cart_data)
        return Response(serialized_data, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({'error': 'Không tìm thấy mục giỏ hàng.'}, status=status.HTTP_404_NOT_FOUND)


class CartViewSet(APIView):
    def post(self, request):
        try:
            # fix
            body_data = json.loads(request.body)
            username = body_data.get("username")
            medicine_id = body_data.get("medicine_id")
            quantity = body_data.get("quantity", 1)
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

    def delete(self, request, item_id):
        cart_item = Cart.objects.get(id_cart=item_id)
        cart_item.delete()
        return JsonResponse({})

    def put(self, request, item_id):
        if request.method == 'POST':
            cart_item_id = request.POST.get('item_id')
            new_quantity = int(request.POST.get('new_quantity'))
            try:
                cart_item = Cart.objects.get(id_cart=cart_item_id)
                cart_item.quantity = new_quantity
                cart_item.save()
                return JsonResponse({'success': True})
            except Cart.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Cart item not found'})
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


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
        query = request.GET.get('q', '')
        keywords = query.split()
        conditions = Q()
        for keyword in keywords:
            conditions |= Q(name_medicine__icontains=keyword)

        all_medicines = Medicine.objects.filter(conditions)
        medicines_list = []
        for medicine in all_medicines:
            medicines_list.append(medicine.to_dict())

        return JsonResponse(medicines_list, safe=False)


class HistoryViewSet(APIView):
    serialize_class = OrderSerializer

    def get_orders(self, user_id):
        orders = Order.objects.filter(user_id=user_id)
        serializer = self.serialize_class(orders, many=True)
        return Response({'orders': serializer.data})

    def get_order_items(self, order_id):
        order_items = OrderItem.objects.filter(id_order_id=order_id)
        serialized_data = []
        for order_item in order_items:
            order_data = OrderItemSerializer(order_item).data
            item_data = {
                'id': order_item.id,
                'quantity': order_item.quantity,
                'name': order_item.id_medicine.name_medicine,
                'price': order_item.id_medicine.price
            }
            order_data['id_medicine'] = item_data
            serialized_data.append(item_data)
        return Response(serialized_data)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        order_id = self.kwargs.get('order_id')
        if user_id:
            return self.get_orders(user_id)
        elif order_id:
            return self.get_order_items(order_id)
        return Response(status=400)




