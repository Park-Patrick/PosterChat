from django.test import TestCase
from .models import User
from typing import Dict, List


class UserModelTests(TestCase):

    # Unfortunately these are valid email addresses
    # https://en.wikipedia.org/wiki/Email_address#Examples

    valid_emails = {
        r'simple@example.com': "",
        r'very.common@example.com': "",
        r'disposable.style.email.with+symbol@example.com': "",
        r'other.email-with-hyphen@example.com': "",
        r'fully-qualified-domain@example.com': "",

        r'user.name+tag+sorting@example.com': "may go to user.name@example.com inbox depending on mail server",

        r'x@example.com': "one-letter local-part",
        r'example-indeed@strange-example.com': "local domain name with no TLD, although ICANN highly discourages dotless email addresses[13]",
        r'admin@mailserver1': "",
        r'example@s.example': "",
        r'" "@example.org': "space between the quotes",
        r'"john..doe"@example.org': "quoted double dot",
        r'mailhost!username@example.org': "bangified host route used for uucp mailers",
        r'user%example.com@example.org': "% \escaped mail route to user@example.com via example.org",
    }

    invalid_emails = [
        r'Abc.example.com': "no @ character",
        r'A@b@c@example.com': "only one @ is allowed outside quotation marks",
        r'a"b(c)d, e:f',
        r'g < h > i[j\k]l@example.com': "none of the special characters in this local-part are allowed outside quotation marks",
        r'just"not"right@example.com': "quoted strings must be dot separated or the only element making up the local-part",
        r'this is"not\allowed@example.com': "spaces, quotes, and backslashes may only exist when within quoted strings and preceded by a backslash",
        r'this\ still\"not\\allowed@example.com': "even if escaped(preceded by a backslash), spaces, quotes, and backslashes must still be contained by quotes",
        r'1234567890123456789012345678901234567890123456789012345678901234+x@example.com': "local part is longer than 64 characters",
        "": "Empty email",
    ]

    valid_usernames = [
        "usernameusername": "Username is at max spaces",


        "users": "Min length 5 chars of alphanumeric",
        "user4": "Min length 5 chars of alphanumeric",
        "u2352356235": "Min length 5 chars of alphanumeric",
        "user_user1452": "Can have a single underscore"
    ]

    invalid_usernames = [
        "24553": "Must have at least one letter",
        "1username": "Not allowed to start with number",
        "user?name": "No special characters",
        "user": "Too short",
        "usernameusername1": "Too long",
        "user__name": "When using - or _, cannot include multiple in a row",
        "user-_-name": "When using - or _, cannot include multiple in a row",
        "user---name": "When using - or _, cannot include multiple in a row",
        "user_-name": "When using - or _, cannot include multiple in a row",

        "-user": "No trailing/prefixing -/_",
        "user-": "No trailing/prefixing -/_",
        "_user": "No trailing/prefixing -/_",
        "user_": "No trailing/prefixing -/_",

        "us_ers": "Not 5 letters long",
        "______": "Not 5 letters long",
        "u3r55": "Not 5 letters long",
        "2": "Not 5 letters long",
        "user-": "Not 5 letters long",
        "": "Empty username",
    ]

    valid_first_names = [
        "seran": "",
        "Seran": "",
        "seran": "",
        "Seran Seran": "",
        "Seran-Seran": "",

        " Seran": "User manager should strip spaces prefixed/suffixed spaces",
        "Seran ": "User manager should strip spaces prefixed/suffixed spaces",

        "Seran  Seran": "User manager should replace multiple whitespaces with 1",
        "seranseranseranseranseranseranseran": "Max length (35 chars)",
    ]

    invalid_first_names = [
        "seranseranseranseranseranseranserann": "Too long (36 characters)",
        "seran123seran": "Cannot have numbers in first name",
        "Seran--Seran": "Cannot have multiple hyphens in a row",
        "Seran-": "Cannot have leading/following hyphens",
        "-Seran": "Cannot have leading/following hyphens",
        "": "Empty name",
    ]

    valid_last_names = valid_first_names
    invalid_last_names = invalid_first_names

    valid_create_user_kwargs = {
        "email": self.valid_emails[0],
        "first_name": self.valid_first_names[0],
        "last_name": self.valid_last_names[0],
        "username": self.valid_usernames[0],
    }

    def assert_user_created_for_params(self, create_user_kwargs: Dict[str, str],
                                       key_to_assert: str, values_to_try: List[str]):
        for value in values_to_try:
            create_user_kwargs[key_to_assert] = value
            User.objects.create_user(create_user_kwargs)

    def assert_user_created_error_for_params(self, raises, create_user_kwargs: Dict[str, str],
                                             key_to_assert: str, values_to_try: List[str]):
        for value in values_to_try:
            create_user_kwargs[key_to_assert] = value
            self.assertRaises(
                raises, User.objects.create_user, create_user_kwargs)

    def test_valid_first_names(self):
        self.assert_user_created_for_params(
            self.valid_create_user_kwargs, "first_name", self.valid_first_names)

    def test_invalid_first_names(self):
        self.assert_user_created_error_for_params(
            self, ValueError, self.valid_create_user_kwargs, "first_name", self.valid_first_names)

    def test_valid_last_names(self):
        self.assert_user_created_for_params(
            self.valid_create_user_kwargs, "last_name", self.valid_last_names)

    def test_invalid_last_names(self):
        self.assert_user_created_error_for_params(
            self, ValueError, self.valid_create_user_kwargs, "last_name", self.valid_last_names)

    def test_valid_emails(self):
        self.assert_user_created_for_params(
            self.valid_create_user_kwargs, "last_name", self.valid_emails)

    def test_invalid_emails(self):
        self.assert_user_created_error_for_params(
            self, ValueError, self.valid_create_user_kwargs, "last_name", self.valid_emails)

    def test_valid_usernames(self):
        self.assert_user_created_for_params(
            self.valid_create_user_kwargs, "last_name", self.valid_usernames)

    def test_invalid_usernames(self):
        self.assert_user_created_error_for_params(
            self, ValueError, self.valid_create_user_kwargs, "last_name", self.valid_usernames)

    def test_avatar_resize(self):
        pass


class HomeViewTests(TestCase):
    pass


class UpdateUserViewTests(TestCase):
    pass


class ProfileViewTests(TestCase):
    pass


class UserLoginViewTests(TestCase):
    pass


class UserSignupViewTests(TestCase):
    pass


class UserSignoutViewTests(TestCase):
    pass
