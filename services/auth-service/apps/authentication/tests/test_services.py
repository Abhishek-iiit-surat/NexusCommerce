from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.models import User
from apps.authentication.services import AuthService
from apps.authentication.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
    InvalidTokenError,
)


# Helper to create a user directly in the database (bypasses service layer)
def make_user(email="test@example.com", mobile="9999999999", password="Test@1234"):
    return User.objects.create_user(
        email=email,
        mobile_number=mobile,
        first_name="Test",
        last_name="User",
        password=password,
    )


class RegisterUserTest(TestCase):
    def setUp(self):
        # setUp runs before every single test method in this class
        self.service = AuthService()

    def test_register_success_returns_tokens(self):
        result = self.service.register_user(
            email="new@example.com",
            password="Test@1234",
            mobile_number="9876543210",
            first_name="John",
            last_name="Doe",
        )
        # Assert that both keys exist in the returned dict
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)

    def test_register_duplicate_email_raises(self):
        make_user(email="dup@example.com", mobile="1111111111")

        # assertRaises checks that the code inside the `with` block raises the given exception
        with self.assertRaises(UserAlreadyExistsError):
            self.service.register_user(
                email="dup@example.com",  # same email
                password="Test@1234",
                mobile_number="2222222222",
                first_name="Jane",
            )

    def test_register_duplicate_mobile_raises(self):
        make_user(email="first@example.com", mobile="9999999999")

        with self.assertRaises(UserAlreadyExistsError):
            self.service.register_user(
                email="second@example.com",
                password="Test@1234",
                mobile_number="9999999999",  # same mobile
                first_name="Jane",
            )


class LoginUserTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        # Create a real user in the test database to log in with
        self.user = make_user(email="login@example.com", mobile="8888888888", password="Test@1234")

    def test_login_success_returns_tokens(self):
        # request=None works here because our backend doesn't use the request object
        result = self.service.login_user(request=None, username="login@example.com", password="Test@1234")
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)

    def test_login_wrong_password_raises(self):
        with self.assertRaises(InvalidCredentialsError):
            self.service.login_user(request=None, username="login@example.com", password="WrongPass")

    def test_login_nonexistent_user_raises(self):
        with self.assertRaises(InvalidCredentialsError):
            self.service.login_user(request=None, username="ghost@example.com", password="Test@1234")


class RefreshTokenTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        self.user = make_user()

    def test_refresh_success_returns_new_tokens(self):
        # Generate a real refresh token for our test user
        refresh = RefreshToken.for_user(self.user)
        result = self.service.refresh_token(str(refresh))
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)

    def test_refresh_invalid_token_raises(self):
        with self.assertRaises(InvalidTokenError):
            self.service.refresh_token("this.is.not.a.valid.token")


class LogoutUserTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        self.user = make_user()

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user)
        result = self.service.logout_user(str(refresh))
        self.assertEqual(result["message"], "User logged out successfully")


class DeleteUserTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        self.user = make_user()

    def test_delete_success(self):
        self.service.delete_user(self.user.id)
        # After deletion, user should not exist in the database
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_nonexistent_user_raises(self):
        with self.assertRaises(UserNotFoundError):
            self.service.delete_user(user_id=99999)


class UpdateUserDetailsTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        self.user = make_user()

    def test_update_success(self):
        result = self.service.update_user_details(self.user.id, first_name="Updated")
        self.assertEqual(result["first_name"], "Updated")
        # Also verify it actually changed in the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_nonexistent_user_raises(self):
        with self.assertRaises(UserNotFoundError):
            self.service.update_user_details(user_id=99999, first_name="Ghost")

    def test_protected_fields_are_ignored(self):
        original_email = self.user.email
        # Passing email should be silently ignored, not updated
        self.service.update_user_details(self.user.id, email="hacker@example.com", first_name="Safe")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, original_email)


class ResetPasswordTest(TestCase):
    def setUp(self):
        self.service = AuthService()
        self.user = make_user()

    def test_reset_password_success_returns_tokens(self):
        result = self.service.reset_password(self.user.id, "NewPass@9999")
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)

    def test_reset_password_nonexistent_user_raises(self):
        with self.assertRaises(UserNotFoundError):
            self.service.reset_password(user_id=99999, new_password="NewPass@9999")
