import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from achare.core.messages import (
    INVALID_OR_EXPIRED_NONCE,
    INVALID_OR_EXPIRED_OTP,
    PROFILE_UPDATED_SUCCESSFULLY,
)

from achare.authentication.helper_functions import (
    generate_and_cache_nonce,
    generate_send_and_cache_otp,
)

User = get_user_model()
client = APIClient()


@pytest.mark.django_db
@pytest.fixture
def user():
    user = User.objects.create(
        mobile_number="09100953795", password="passwordtest12345", is_active=True
    )
    user.save()
    return user


@pytest.fixture
def valid_otp():
    mobile_number = "09100953795"
    otp = generate_send_and_cache_otp(mobile_number)
    nonce = generate_and_cache_nonce(mobile_number)
    return otp, nonce


@pytest.mark.django_db
def test_user_authenticate(user):
    response = client.post(
        "/authentication/user/account/", {"mobile_number": "09100953795"}
    )
    print(response.data)
    assert response.status_code == 200
    assert "nonce" in response.data
    assert response.data["its_new_user"] == False


@pytest.mark.django_db
def test_verify_otp_invalid_nonce():
    response = client.post(
        "/authentication/user/verify/", {"nonce": "invalidnonce", "otp": "123456"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == INVALID_OR_EXPIRED_NONCE


@pytest.mark.django_db
def test_verify_otp_invalid_otp(valid_otp):
    otp, nonce = valid_otp
    response = client.post(
        "/authentication/user/verify/", {"nonce": nonce, "otp": "000000"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == INVALID_OR_EXPIRED_OTP


@pytest.mark.django_db
def test_successful_verify_otp(valid_otp):
    otp, nonce = valid_otp
    response = client.post("/authentication/user/verify/", {"nonce": nonce, "otp": otp})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_login_user_invalid_nonce():
    response = client.post(
        "/authentication/user/login/",
        {"nonce": "invalidnonce", "password": "password123"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == INVALID_OR_EXPIRED_NONCE


@pytest.mark.django_db
def test_login_user_success(valid_otp, user):
    otp, nonce = valid_otp
    response = client.post(
        "/authentication/user/login/", {"nonce": nonce, "password": otp}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_complete_profile_success(user):
    client.force_authenticate(user=user)
    response = client.put(
        "/authentication/user/profile/",
        {
            "name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "date_birth": "2000-01-01",
            "password": "newpassword123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == PROFILE_UPDATED_SUCCESSFULLY
