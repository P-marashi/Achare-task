import redis
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import AuthenticationSerializer
from achare.utils.helper_functions import otp_code, send_otp, generate_unique_hash
from drf_spectacular.utils import extend_schema

User = get_user_model()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


class UserAuthentication(APIView):
    """api class for check status of user"""

    @extend_schema(tags=["account"], request=AuthenticationSerializer)
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_number = serializer.validated_data["mobile_number"]
            try:
                user = User.objects.get(mobile_number=mobile_number, is_active=True)
                return Response(
                    {"its_new_user": False, "login_url": "/login/"},
                    status=status.HTTP_200_OK,
                )

            except User.DoesNotExist:
                otp = otp_code()

                logger.debug(f"Generated OTP: {otp}")
                unique_hash = generate_unique_hash()
                redis_client.set(f"otp:{mobile_number}", otp, ex=300)

                # Store the unique hash in Redis with the mobile number as the value
                redis_client.set(f"hash:{unique_hash}", mobile_number, ex=3600)

                send_otp(mobile_number, otp)

                # Return the unique hash to the front end
                return Response(
                    {
                        "is_new_user": True,
                        "user": unique_hash,
                        "message": "OTP sent to mobile number.",
                    },
                    status=status.HTTP_200_OK,
                )


class VerifyOtp(APIView):
    """api class for check status of user"""