from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_not_required
# Create your views here.

from dn_workers import models as worker_models

@login_not_required
def homePage(req:HttpRequest):
    return render(req,"dn_home/index.html")


def dashBoard(req:HttpRequest):
    all_items = {
        "sales": {
            "name": "Sales Dashboard",
            "link": reverse("sales_data"),
            "link_id": "sales_data"
        },
        "stock": {
            "name": "Stock Dashboard",
            "link": reverse("products_dashboard"),
            "link_id": "prod_dash"
        },
        "product": {
            "name": "Product Dashboard", 
            "link": reverse("sales_dashboard"),
            "link_id": "sales_dash"
        },
        "finance": {
            "name": "Finance Dashboard",
            "link": reverse("general_sales"),
            "link_id": "general_sales"
        },
        "workers": {
            "name": "Worker Dashboard",
            "link": reverse("worker_dashboard"),
            "link_id": "worker_dash",
        },
    }

    # Determine Access
    allowed_keys = []
    
    # Check Owner
    try:
        if req.user.worker_profile.is_owner:
            # Owner sees EVERYTHING
            allowed_keys = ["sales", "stock", "product", "finance", "hub", "workers", "subscription"]
    except:
        pass

    # Check Worker Role (if not Owner, or inclusive?)
    # Usually owner check handles it, but if not owner:
    if not allowed_keys:
        try:
            role = req.user.worker_profile.role
            
            if role == worker_models.WorkerRoles.SELLER:
                allowed_keys = ["sales", "product"] # Can sell and see products
            elif role == worker_models.WorkerRoles.STOCKER:
                allowed_keys = ["stock"] # Can stock and see products
            elif role == worker_models.WorkerRoles.MANAGER:
                # Manager sees Sales, Stock, Product, Finance
                allowed_keys = ["sales", "stock", "product"]
        except:
            pass
            
    # Construct Context Paths
    # We map the keys back to the specific structure expected by the template
    paths = {
        item["name"]: {"link": item["link"], "link_id": item["link_id"]}
        for key, item in all_items.items()
        if key in allowed_keys
    }

    # Determine Default Link (First available)
    default_link = next(iter(paths.values()))['link'] if paths else reverse("worker_dashboard")

    context={
        "paths":paths,
        "default_link": default_link
    }
    return render(req,"dn_home/dashboard.html",context=context)