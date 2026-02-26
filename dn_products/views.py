from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
from django.forms import ModelForm
from django.db import transaction
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

from django_htmx import http
from dn_utilities import utilities
from dn_products import models as product_models



def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].title() + ''.join(x.title() for x in components[1:])


def productsDashboard(req:HttpRequest):
    product_categories={k:v for k,v in product_models.category_groups.items()}
    prod_categories = {
            group_name: {to_camel_case(db_val): human_val for db_val, human_val in items.items()}
            for group_name, items in product_categories.items()
        }
    context={
        "product_categories":prod_categories
    }
    req.session["active_url"]=req.path
    return render(req,"dn_products/products_dashboard.html",context=context)

def addProduct(req:HttpRequest,class_name:str):
    context={
        "class_name":class_name,
        "add":True,
        "view_url":reverse("add_product",args=[class_name])
    }
    _form=utilities.get_form_class("dn_products",f"{class_name}Form")
    if req.method=="POST":
        form:ModelForm=_form(req.POST)
        if form.is_valid():
            with transaction.atomic():
                f_instance=form.save(commit=False)
                f_instance.stocker=req.user
                f_instance.save()
                
                messages.success(req,message=f"{f_instance.product_count} {f_instance.product_name}(s) have been added successfully.")
                return http.HttpResponseClientRedirect(reverse("dashboard"))
        
        context["form"]=form
                    
        
    else:
        context["form"]=_form

        
    return render(req,"dn_products/forms/add_product.html",context=context)

def searchProduct(req:HttpRequest):
    data=req.POST
    product_name=data.get("product_name")
    class_name=data.get("class-name")
    context={}
    try:
        if product_name:
            model=apps.get_model("dn_products",class_name)
            products=model.objects.filter(product_name__icontains=product_name)
            context["products"]=products
            context["class_name"]=class_name
        else:
            context["is_empty"]=True
    except LookupError:
        context["products"]=None
        
        
    return render(req,"dn_products/partials/search_product_results.html",context=context)


def updateProduct(req:HttpRequest,product_uuid,class_name):
    try:
        context={
            "view_url":reverse("update_product",args=[product_uuid,class_name])
        }
        model=apps.get_model("dn_products",class_name)
        product=model.objects.get(pk=product_uuid)
        FormClass:ModelForm=utilities.get_form_class("dn_products",f"{class_name}Form")
        if req.method=="POST":
            form=FormClass(req.POST,instance=product)
            if form.is_valid():
                with transaction.atomic():
                    f_instance=form.save(commit=False)
                    f_instance.stocker=req.user
                    f_instance.save()
                messages.success(req,message=f"{f_instance.product_name} has been updated successfully.")
                return http.HttpResponseClientRefresh()
                    
        context["form"]=FormClass(instance=product)
        
        return render(req,"dn_products/forms/add_product.html",context=context)
        
    except ObjectDoesNotExist:
        messages.error(req,message="Product does not exist.")
    
    
    
def productDetails(req:HttpRequest,class_name:str):
    try:
        context={}
        model=apps.get_model("dn_products",class_name)
        products:product_models.Product=model.objects.all()
        if products:
            products_by_brand = {}
            for product in products:
                if product.product_brand in products_by_brand.keys():
                    products_by_brand[product.product_brand].append(product)
                else:
                    products_by_brand[product.product_brand]=[product]
            
            context["products"]=products_by_brand
        return render(req,"dn_products/partials/product_details.html",context=context)
    except LookupError:
        messages.error(req,"Error retrieving info.")
        return http.HttpResponseClientRefresh()
    