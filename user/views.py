from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import MyTokenObtainPairSerializer, UserSignUpSerializer


class SignUpView(APIView):
    """
    Assignee : 정석

    회원가입
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignUpSerializer)
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            res = Response(
                {
                    "message": "회원가입에 성공했습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """
    Assignee : 정석

    로그인

    로그인 성공시 access token과 refresh token만 리턴
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignUpSerializer)
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "이메일 또는 비밀번호를 잘못 입력했습니다."}, status=status.HTTP_404_NOT_FOUND)
        login(request, user)
        token = MyTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = Response(
            {
                "message": f"{user.username}님 반갑습니다!",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        return res
