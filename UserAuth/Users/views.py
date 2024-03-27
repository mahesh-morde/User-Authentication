from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .helper import send_forgot_password_mail
import uuid

def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        name = request.POST.get("uname")
        email = request.POST.get("email")
        upass1 = request.POST.get("upass")
        upass2 = request.POST.get("ucom")

        if fname=='' or lname=='' or name=='' or email=='' or upass1=='':
            return JsonResponse({"error": "Field cannot be empty!"}, status=400)

        if upass1 != upass2:
            return JsonResponse({"error": "Password and Confirm password do not match!"}, status=400)

        try:
            user = User.objects.create_user(username=name, email=email, first_name=fname, last_name=lname, password=upass1)
            return JsonResponse({"success": "Successfully registered"})
        except Exception as e:
            return JsonResponse({"error": "Username already exists"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        if not all([username, password]):
            return JsonResponse({"error": "Fields cannot be empty"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": "Successfully logged in"})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('uname')

        if not User.objects.filter(username=username).exists():
            return JsonResponse({"error": "No user found with this username."}, status=404)

        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        send_forgot_password_mail(user_obj, token)
        return JsonResponse({"success": "An email has been sent."})

    return JsonResponse({"error": "Method not allowed"}, status=405)


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def change_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not all([new_password, confirm_password]):
            return JsonResponse({"error": "Fields cannot be empty"}, status=400)

        if new_password != confirm_password:
            return JsonResponse({"error": "New password and confirm password do not match"}, status=400)

        try:
            user = User.objects.get(forgot_password_token=token)
            user.password = make_password(new_password)  # Hash the new password
            user.forgot_password_token = None  # Clear the token after password change
            user.save()
            return JsonResponse({"success": "Password changed successfully"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=404)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)
