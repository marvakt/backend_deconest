


# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import check_password, make_password
# from .models import User
# from .serializers import UserSerializer

# # ---------------- Token ----------------
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {"refresh": str(refresh), "access": str(refresh.access_token)}

# # ---------------- Register ----------------
# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ---------------- Login ----------------
# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({
#                 "tokens": get_tokens_for_user(user),
#                 "user": UserSerializer(user).data
#             }, status=status.HTTP_200_OK)

#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# # ---------------- Logout ----------------
# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         try:
#             token = RefreshToken(request.data["refresh"])
#             token.blacklist()
#             return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
#         except Exception:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

# # ---------------- Profile ----------------
# class ProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class UpdateProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def patch(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChangePasswordView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def patch(self, request):
#         user = request.user
#         current_password = request.data.get("current_password")
#         new_password = request.data.get("new_password")

#         if not current_password or not new_password:
#             return Response({"error": "Both current and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         if not check_password(current_password, user.password):
#             return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

#         user.password = make_password(new_password)
#         user.save()
#         return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)



from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer

# ---------------- Token ----------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

# ---------------- Register ----------------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # ✅ Manually create the user
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                role=data.get("role", "user")  # default to user
            )

            # ✅ Send success email to user
            subject_user = "Welcome to DecoNest!"
            message_user = (
                f"Hi {user.username},\n\n"
                "Your registration on DecoNest was successful. We're excited to have you join our decor community! 🪴✨\n\n"
                "Warm regards,\nTeam DecoNest"
            )
            send_mail(
                subject_user,
                message_user,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # ✅ Send notification email to admin
            subject_admin = "New User Registered - DecoNest"
            message_admin = (
                f"Hello Admin,\n\nA new user has registered on DecoNest.\n\n"
                f"Username: {user.username}\n"
                f"Email: {user.email}\n\n"
                "Login to the admin panel for details."
            )
            send_mail(
                subject_admin,
                message_admin,
                settings.DEFAULT_FROM_EMAIL,
                ['your_admin_email@gmail.com'],  # change this
                fail_silently=False,
            )

            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Login ----------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            return Response({
                "tokens": get_tokens_for_user(user),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ---------------- Logout ----------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

# ---------------- Profile ----------------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response({"error": "Both current and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(current_password, user.password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
