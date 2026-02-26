from django.urls import path
from dn_sales import views

urlpatterns = [
    path("",views.salesDashboard,name="sales_dashboard"),
    path("get_products/<str:class_name>/",views.getProducts,name="get_sale_products"),
    path("add_to_cart/",views.addToCart,name="add_to_cart"),
    path("remove_from_cart/",views.removeFromCart,name="remove_from_cart"),
    path("cart_view",views.cartView,name="cart_view"),
    path("remove_from_cart_items/",views.deleteFromCart,name="remove_from_cart_items"),
    path("complete_sale/",views.completeSale,name="complete_sale"),
    path("print_receipt/",views.printReceipt,name="print_receipt"),
    path("print_receipt/<str:receipt_url>/",views.printReceipt,name="receipt_link"),
    
    # sales data
    
    path("sales_data/",views.salesData,name="sales_data"),
    path("genaral_sales/",views.generalFinances,name="general_sales")
]
