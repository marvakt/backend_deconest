# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
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
#             user = serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ---------------- Login ----------------
# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=400)
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({
#                 "tokens": get_tokens_for_user(user),
#                 "user": UserSerializer(user).data
#             })
#         return Response({"error": "Invalid credentials"}, status=401)

# # ---------------- Logout ----------------
# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         try:
#             token = RefreshToken(request.data["refresh"])
#             token.blacklist()
#             return Response({'message': 'Logged out successfully'})
#         except Exception:
#             return Response({'error': 'Invalid token'}, status=400)



from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
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
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
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
