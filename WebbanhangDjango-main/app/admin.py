from django.contrib import admin
from .models import Order, Product, OrderItem, ShippingAddress, Category, Slide, Slide2
from django.utils.html import format_html

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'customer_address','complete', 'order_delivery_status', 'order_total', 'order_products']

    def customer_name(self, obj):
        return obj.customer.get_full_name() if obj.customer else ''

    def customer_phone(self, obj):
        shipping_address = obj.shippingaddress_set.first()
        return shipping_address.mobile if shipping_address else ''

    def customer_address(self, obj):
        shipping_address = obj.shippingaddress_set.first()
        if shipping_address:
            return f"{shipping_address.street_address}, {shipping_address.city}, {shipping_address.state}"
        return ''


    def order_total(self, obj):
        order_items = obj.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in order_items if item.product])
        return total

    def order_products(self, obj):
        order_items = obj.orderitem_set.all()
        products = []
        for item in order_items:
            product_name = item.product.name if item.product else ''
            product_quantity = item.quantity
            product_price = item.product.price if item.product else 0
            products.append(f"Tên sản phẩm: {product_name}, Số lượng: {product_quantity}, Giá: {product_price}")
        return format_html("<br>".join(products))
    def order_delivery_status(self, obj):
        if obj.status == 'Chưa giao':
            return format_html('<span style="color: red; font-weight: bold; text-align: center;">{}</span>', obj.status)
        else:
            return format_html('<span style="color: green; font-weight: bold; text-align: center;">{}</span>', obj.status)
 
    customer_name.short_description = 'Họ tên khách hàng'
    customer_phone.short_description = 'Số điện thoại'
    customer_address.short_description = 'Địa chỉ'
    order_delivery_status.short_description = 'Trạng thái giao hàng'
    order_total.short_description = 'Tổng tiền'
    order_products.short_description = 'Danh sách sản phẩm'



admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Slide)
admin.site.register(Slide2)
