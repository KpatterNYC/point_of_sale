from django.urls import path
from dn_products import views


urlpatterns = [
    path("products_dashboard/",views.productsDashboard,name="products_dashboard"),
    path("add_product/<str:class_name>/",views.addProduct,name="add_product"),
    path("search_product",views.searchProduct,name="search_product"),
    path("update_product/<uuid:product_uuid>/<str:class_name>",views.updateProduct,name="update_product"),
    path("product_details/<str:class_name>/",views.productDetails,name="product_details"),
]
