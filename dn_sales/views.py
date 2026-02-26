import json
from datetime import datetime
import uuid

from django.shortcuts import render
from django.http import HttpRequest
from django.apps import apps
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum, Count,Q,Min,Max,F
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.conf import settings


from django_htmx import http

from dn_products import models as product_models
from dn_sales import models
from dn_utilities import utilities


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].title() + ''.join(x.title() for x in components[1:])

# VIEW for products already sold
def generalFinances(req:HttpRequest):
    user = req.user
    user_profile = user.worker_profile
    is_owner = user_profile.is_owner
    today = timezone.now().date()
    
    queryset = models.Sale.objects.all()
    context = {}
    
    def clean(val): return val or 0

    if is_owner:
        # OWNER: Full financial stats + Date Range (First to Last)
        today=datetime.today().date()
        stats = queryset.aggregate(
            total_sales_figure=Sum('amount_recieved'),
            total_sales_count=Count('sale_pk'),
            total_profits_figure=Sum('profit'),
            today_sales_figure=Sum('amount_recieved', filter=Q(sale_dt__date=today)),
            today_sales_count=Count('sale_pk', filter=Q(sale_dt__date=today)),
            today_profits_figure=Sum('profit', filter=Q(sale_dt__date=today)),
            # Date boundaries
            first_sale=Min('sale_dt'),
            last_sale=Max('sale_dt')
        )
        context["sales_breakdown"] = {
            "Total Sales": {
                "figure": clean(stats['total_sales_figure']), 
                "count": stats['total_sales_count'],
                "since": stats['first_sale'],
                "until": stats['last_sale'] # The "To" date
            },
            "Sales Today": {
                "figure": clean(stats['today_sales_figure']), 
                "count": stats['today_sales_count']
            },
            "Total Profits": {"figure": clean(stats['total_profits_figure'])},
            "Profits Today": {"figure": clean(stats['today_profits_figure'])},
        }
        shop_cash_list = models.CashTracker.objects.filter(
        cash_dt=today
        ).annotate(
            total_cash=Sum('amount')
        ).order_by('-total_cash')
        grand_total_cash = shop_cash_list.aggregate(Sum('total_cash'))['total_cash__sum'] or 0
        context["cash_tracker"]=shop_cash_list
        context["cash_date"]=today
        context["cash_sum"]=grand_total_cash
    else:
        # WORKER: Count-based breakdown + their specific date range
        worker_qs = queryset.filter(worker_handler=user.worker_profile)
        worker_stats = worker_qs.aggregate(
            total_count=Count('sale_pk'),
            today_count=Count('sale_pk', filter=Q(sale_dt__date=today)),
            first_sale=Min('sale_dt'),
            last_sale=Max('sale_dt')
        )
        
        context["worker_breakdown"] = {
            "Total Sales": {
                "count": worker_stats['total_count'],
                "since": worker_stats['first_sale'],
                "until": worker_stats['last_sale']
            },
            "Sales Today": {"count": worker_stats['today_count']},
        }
        queryset = worker_qs
    
    req.session["active_url"]=req.path
    return render(req,"dn_sales/general_finance.html",context=context)
def salesData(req: HttpRequest):
    user = req.user
    tnt_profile = user.worker_profile
    is_owner = tnt_profile.is_owner
    queryset = models.Sale.objects.all()
    context = {
        "table_headers":["Handler","Date","Financial Data","Products","Receipt"]
    }

    # Recent list (Top 20)
    sales_list = queryset.select_related('worker_handler', 'admin_handler').order_by("-sale_dt")
    if is_owner or (hasattr(req.user,"worker_profile") and req.user.worker_profile.role == "manager"):
        context["sales_data"] = sales_list[:10]
    else:
        context["sales_data"]=sales_list.filter(worker_handler=req.user.worker_profile)[:10]
    context["is_owner"] = is_owner
    req.session["active_url"] = req.path
    
    return render(req, "dn_sales/sales_data.html", context=context)



# View for products they can sale
def salesDashboard(req:HttpRequest):
    product_categories={k:v for k,v in product_models.category_groups.items()}
    prod_categories = {
            group_name: {to_camel_case(db_val): human_val for db_val, human_val in items.items()}
            for group_name, items in product_categories.items()
        }
    context={
        "product_categories":prod_categories
    }
    if "cart_count" not in req.session.keys():
        req.session["cart_count"]=0
        
    if "cart_data" not in req.session.keys():
        req.session["cart_data"]={}
    
    req.session["active_url"]=req.path
    return render(req,"dn_sales/sales_dashboard.html",context=context)


def getProducts(req:HttpRequest,class_name:str):
    try:
        context={
            "class_name":class_name,
            "search_by":{
                "product_brand":"Brand",
                "product_name":"Product Name"
            }
        }
        model=apps.get_model("dn_products",class_name)
        products = model.objects.all()
        
        if products:
            products_by_brand = {}
            hide_fields=["Product buy price","Restock threshold","Stocker","Added date","Product count"]
            for product in products:
                if product.product_brand in products_by_brand.keys():
                    products_by_brand[product.product_brand].append(product)
                else:
                    products_by_brand[product.product_brand]=[product]
            
            context["products"]=products_by_brand
            context["hide_fields"]=hide_fields
        return render(req,"dn_sales/partials/sale_products.html",context=context)
        
    except LookupError:
        messages.error(req,"Error retrieving products")
        return http.HttpResponseClientRefresh()
    
    

def addToCart(req:HttpRequest):
    data=req.POST
    product_pk=data.get("product-pk")
    product_count=data.get("product-count")
    class_name=data.get("class-name")
    context={
        "product_pk":product_pk
    }
    if product_pk and product_count:
        product_count=int(product_count)
        if product_pk not in req.session["cart_data"].keys():
            req.session["cart_data"][product_pk]={
                "class_name":class_name,
                "count":1
            }
            req.session["cart_count"]+=1
        elif product_pk in req.session["cart_data"].keys() and product_count > req.session["cart_data"][product_pk]["count"]:
            req.session["cart_data"][product_pk]["count"]+=1
            req.session["cart_count"]+=1
        elif req.session["cart_data"][product_pk]["count"] >= product_count:
            req.session["cart_data"][product_pk]["count"]= product_count
        context["count"]=req.session["cart_data"][product_pk]["count"]
    else:
        if product_pk in req.session["cart_data"].keys():
            context["count"]=req.session["cart_data"][product_pk]["count"]
        else:
            context["count"]=0
            
    return render(req,"dn_sales/partials/add_or_remove_from_cart.html",context=context)

def removeFromCart(req:HttpRequest):
    data=req.POST
    product_pk=data.get("product-pk")
    context={
        "product_pk":product_pk
    }
    
    if product_pk in req.session["cart_data"].keys() and req.session["cart_data"][product_pk]["count"]>0:
        req.session["cart_count"]-=1
        req.session["cart_data"][product_pk]["count"]-=1
        
        context["count"]=req.session["cart_data"][product_pk]["count"]
    if product_pk in req.session["cart_data"].keys() and req.session["cart_data"][product_pk]["count"]==0:
        context["count"]=0
        del req.session["cart_data"][product_pk]
        
    return render(req,"dn_sales/partials/add_or_remove_from_cart.html",context=context)


def cartView(req:HttpRequest):
    cart_data:dict[dict]=req.session["cart_data"]
    context={
        "products":[],
        "payment_methods":{
            "cash":"Cash",
        }
    }
    sim_map={"single":1,"dual":2,"three":3,"quad":4}
    if cart_data:
        for key,val in cart_data.items():
            count=val["count"]
            class_name=val["class_name"]
            try:
                model=apps.get_model("dn_products",class_name)
                product:product_models.Product=model.objects.get(pk=key)
                fields=product.display_fields
                fields.pop("Stocker")
                obj={
                        "product_name":product.product_name,
                        "product_sell_price":product.product_sell_price,
                        "product_discount":product.product_discount,
                        "count":count,
                        "product_pk":product.pk,
                        "delete_info":{"hx-post":reverse("remove_from_cart_items"),"hx-target":f"#delete-{product.pk}-indicator","hx-vals":f'{{"product-pk":"{product.pk}"}}'},
                        "discount":product.product_discount,
                        "class_name":product.className
                    }
                if product.className in ["SmartPhone","FeaturedPhone"]:
                    obj["sim_count"]=list(range(1,sim_map[product.sim_type]+1))
                context["products"].append(obj)
            except LookupError:
                pass
            
    return render(req,"dn_sales/partials/cart_view.html",context=context)
        
        
def deleteFromCart(req:HttpRequest):
    data=req.POST
    product_pk=data.get("product-pk")
    if product_pk in req.session["cart_data"]:
        req.session["cart_count"]-=req.session["cart_data"][product_pk]["count"]
        del req.session["cart_data"][product_pk]
        req.session.modified=True
        messages.success(req,f"Product removed from cart, successfully.")
    
    return http.HttpResponseClientRefresh()

def completeSale(req: HttpRequest):
    data = req.POST
    c_name=data.get("c-name")
    c_phone=data.get("c-phone")
    payment_method="cash"
    amount=int(data.get("cash-amount"))
    products_data = json.loads(data.get("products-data"))
    products = products_data["products"]
    
    receipt_no = f"DE-{datetime.now().strftime('%Y%m%d%H%M%S')}" # More robust format

    receipt_object = {
        "business_name": settings.CLIENT_NAME,
        "customer_name": c_name.title(),
        "customer_phone": c_phone,
        "sale_id": receipt_no,
        "thank_you": "Thank you for shopping with us!",
        "return_policy": "Items once sold can not be returned.",
        "served_by": req.user.worker_profile,
        "products": []
    }

    with transaction.atomic():
        # Instead of creating and then checking owner status separately
        cash_to_track=0
        sale = models.Sale.objects.create(
            amount_recieved=amount,
            payment_method=payment_method,
            customer_name=c_name,
            customer_phone_number=c_phone,
            receipt_number=receipt_no,
            admin_handler=req.user if req.user.worker_profile.is_owner else None,
            worker_handler=None if req.user.worker_profile.is_owner else req.user.worker_profile,
    
        )
    
        sale.cash_amount=amount
        cash_to_track=amount

        sale.save()
        
        t_profit = 0
        t_amount = 0
        for product in products:
            p_model = apps.get_model("dn_products", product["class_name"])
            # Use select_for_update to prevent double-selling the same stock
            p_instance = p_model.objects.select_for_update().get(pk=uuid.UUID(product["product_pk"]))

            count = int(product["count"])
            # SECURE PRICE: Use DB price, not POST data
            line_total = p_instance.product_sell_price * count
            p_profit = line_total - (count * p_instance.product_buy_price)
            
            t_profit += p_profit
            t_amount += line_total
            
            p_instance.product_count -= count
            p_instance.save()

            hide_fields=[
                "Product buy price","Product sell price","Stocker",
                "Added date","Restock threshold","Product count",
                "Product name","Product discount"
                ]
            attributes={k:v for k,v in p_instance.display_fields.items() if k not in hide_fields}
            if product["class_name"] in ["SmartPhone","FeaturePhone"]:
                attributes|=product["imei_data"]
            receipt_object["products"].append({
                "name": p_instance.product_name,
                "attributes": attributes,
                "quantity": count,
                "unit_price": p_instance.product_sell_price
            })
            attributes["Product Name"]=p_instance.product_name
            sold_product=models.SoldProduct()
            sold_product.product_details=attributes
            sold_product.sale=sale
            sold_product.save()
            

        sale.profit = t_profit
        sale.amount_recieved = t_amount # Ensure this matches calculated total
        sale.save()
        if cash_to_track > 0:
            cash_tracker, _ = models.CashTracker.objects.get_or_create(
                cash_dt=datetime.today().date(),
                defaults={'amount': 0}
            )
            cash_tracker.amount += cash_to_track
            cash_tracker.save()
            

    # GENERATE RECEIPT OUTSIDE ATOMIC BLOCK (Faster DB performance)
    receipt_object["total_amount"]=t_amount
    receipt_bytes = utilities.ReceiptGenerator(receipt_object).build_pdf_bytes()
    receipt_file = SimpleUploadedFile(f"{receipt_no}.pdf", receipt_bytes.getvalue(), content_type="application/pdf")
    sale.receipt = receipt_file
    sale.save()
    

    messages.success(req, "Sale completed successfully.")
    req.session.update({"cart_data": {}, "cart_count": 0})
    req.session["receipt_url"]=sale.receipt.url
    req.session["receipt_id"] = sale.receipt_number  # So they know which one they are printing
    req.session.modified = True
    return http.HttpResponseClientRedirect(reverse("print_receipt"))
    
            
            
def printReceipt(req:HttpRequest,receipt_url=None):
    context={}
    if receipt_url:
        context["receipt_url"]=receipt_url
    return render(req,"dn_sales/print_receipt.html",context=context)
            
                
            
            
            
        
        
    
