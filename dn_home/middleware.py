from django.shortcuts import render
from dn_workers.models import WorkerRoles


class WorkerRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Path Prefix -> Allowed Roles
        # If a path isn't here, it defaults to ALLOW ALL (or handled by other middlewares)
        self.role_map = {
            "/sales/": [WorkerRoles.MANAGER, WorkerRoles.SELLER,WorkerRoles.OWNER],
            "/products/": [WorkerRoles.MANAGER, WorkerRoles.STOCKER,WorkerRoles.OWNER],
            "/workers/": [], # Owner Only
            "/accounts/":[WorkerRoles.MANAGER, WorkerRoles.SELLER, WorkerRoles.STOCKER,WorkerRoles.OWNER],
            "/dashboard/": [WorkerRoles.MANAGER, WorkerRoles.SELLER, WorkerRoles.STOCKER,WorkerRoles.OWNER], # Everyone
        }

    def _handle_unauthorized(self, request, message, role=None):
        return render(request, "403.html", status=403)

    def __call__(self, request):
        # 1. Skip if not authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Get User Context
        try:
            profile = request.user.tnt_profile
            is_owner = profile.is_owner
        except:
            is_owner = False
            
        # Owner overrides everything
        if is_owner:
             return self.get_response(request)

        # 3. Check Worker Role
        try:
            worker = request.user.worker_profile
            # Ensure worker is active
            if not worker.is_active:
                 return self._handle_unauthorized(request, "Your worker account is inactive.")
            user_role = worker.role
        except:
            # Not an owner, Not a worker? -> Probably a public user or error state
             if any(request.path.startswith(prefix) for prefix in self.role_map):
                 return self._handle_unauthorized(request, "You do not have a valid role in this tenant.")
             return self.get_response(request)

        # 4. Check Path Permissions
        for prefix, allowed_roles in self.role_map.items():
            if request.path.startswith(prefix):
                # Owner Only path (empty list) and we determined above user is NOT owner
                if not allowed_roles:
                     state_role = user_role if 'user_role' in locals() else None
                     return self._handle_unauthorized(request, "Access Restricted: Owners Only.", role=state_role)
                
                # Worker Role Check
                if user_role not in allowed_roles:
                     return self._handle_unauthorized(request, f"Access Denied. Required Roles: {', '.join(allowed_roles)}", role=user_role)
                
                # Match found and validated
                return self.get_response(request)

        return self.get_response(request)
