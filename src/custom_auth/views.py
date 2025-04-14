from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, TokenCheckSerializer, LogoutSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        examples=[
            OpenApiExample(
                "Example",
                value={"username": "john_doe", "password": "securepassword123"}
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]





class CheckTokenView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenCheckSerializer  # Добавляем сериализатор

    @extend_schema(
        responses={200: TokenCheckSerializer},
        description="Проверка валидности токена"
    )
    def get(self, request):
        return Response({"message": "Token is valid"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(description="Successfully logged out"),
            400: OpenApiResponse(description="Invalid token"),
            401: OpenApiResponse(description="Unauthorized")
        }
    )
    def post(self, request):
        # Вручную проверяем данные, так как это APIView
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )