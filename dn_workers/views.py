from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse
from django.db import transaction

from django.contrib import messages


from django_htmx import http

from dn_workers import models
from dn_workers import forms



def workerDashboard(req:HttpRequest):
    context={
        "workers":models.WorkerProfile.objects.filter(is_owner=False),
        "roles": {i[0]:i[1] for i in models.WorkerRoles.choices}
    }
    req.session["active_url"]=req.path
    return render(req,"dn_workers/worker_dashboard.html",context=context)

def pendingActivationPage(req:HttpRequest):
    return render(req,"dn_workers/pending_activation.html")


def createWorkerProfile(req:HttpRequest):
    context={}
    if req.method=="POST":
        form=forms.WorkerProfileForm(req.POST)
        if form.is_valid():
            with transaction.atomic():
                f_instance=form.save(commit=False)
                f_instance.user=req.user
                f_instance.save()
                messages.success(req,message=f"Worker profile created successfully. Welcome to Katrina's Electronics.")
            return http.HttpResponseClientRedirect(reverse("dashboard"))
        context["form"]=form
        return render(req,"dn_workers/includes/worker_profile_form.html",context=context)
    
    context["form"]=forms.WorkerProfileForm()
    return render(req,"dn_workers/create_worker_profile.html",context=context)


def changeWorkerRole(req:HttpRequest):
    data=req.POST
    role=data.get("worker-role")
    worker_id=data.get("worker-id")
    if role:
        try:
            with transaction.atomic():
                worker_profile=models.WorkerProfile.objects.get(pk=int(worker_id))
                worker_profile.role=role
                worker_profile.save()
                messages.success(req,"Role changed successfully.")
        except:
            messages.error("Erro changing role. Please try again")
                
    else:
        messages.error(req,"Invalid role")
        
    return http.HttpResponseClientRefresh()


def activateWorkerProfile(req:HttpRequest):
    data=req.POST
    worker_pk=int(data.get("worker-id",0))
    if worker_pk:
        try:
            worker_profile=models.WorkerProfile.objects.get(pk=worker_pk)
            if not worker_profile.is_active:
                with transaction.atomic():
                    worker_profile.is_active=True
                    worker_profile.save()
                    messages.success(req,"Worker profile has been activated successfully.")
            else:
                 with transaction.atomic():
                    worker_profile.is_active=False
                    worker_profile.save()
                    messages.success(req,"Worker profile has been de-activated successfully.")
        except:
            messages.error("Invalid worker profile")
    else:
        messages.error("Invalid parameters")
        
    return http.HttpResponseClientRefresh()


def layoffWorker(req:HttpRequest):
    worker_pk=int(req.POST.get("worker-id",0))
    if worker_pk:
        try:
            with transaction.atomic():
                worker_profile=models.WorkerProfile.objects.get(pk=worker_pk)
                worker_profile.is_active=False
                worker_profile.save()
                
                messages.success(req,f"{worker_profile} has been laid-off. No access will be permitted moving foward.")
        except:
            messages.error("Invalid worker profile")    
    else:
        messages.error("Invalid parameters")
        
    return http.HttpResponseClientRefresh()
