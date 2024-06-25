import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


# @pytest.fixture
# def api_client_auth():
#     from rest_framework.test import APIClient
#     from users.tests.factories import UserFactory
#     user = UserFactory(refresh_token="1234")
#     client = APIClient()
#     client.force_login(user)
#     return client
