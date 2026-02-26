
from django.urls import path
from dn_workers import views

urlpatterns = [
    path("",views.workerDashboard,name="worker_dashboard"),
    path("create_profile/",views.createWorkerProfile,name="create_worker_profile"),
    path("activate_worker_profile/",views.activateWorkerProfile,name="activate_worker_profile"),
    path("change_worker_role/",views.changeWorkerRole,name="change_worker_role"),
    path("layoff_worker/",views.layoffWorker,name="layoff_worker"),
    path("pending_activation/",views.pendingActivationPage,name="pending_activation"),
]

    