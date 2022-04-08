from .models import UserRole

def admin_processor(request):
    try:
        is_admin = request.user.roles.filter(role="Admin").exists()
    except:
        is_admin = False
    return {"is_admin": is_admin}