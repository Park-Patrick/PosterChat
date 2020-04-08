import copy
import logging
from typing import Dict, List, Optional, Tuple

import requests
from django.core.files.base import ContentFile
from django.test import TestCase, TransactionTestCase
from PIL import Image
from requests.exceptions import HTTPError

from .models import User

logger = logging.getLogger(__name__)


class UserModelTests(TransactionTestCase):
    """Includes tests for UserManager class"""

    # https://en.wikipedia.org/wiki/Email_address#Examples
    emails_to_test = {
        r'simple@example.com':                             {"is_valid": True, "reason": ""},
        r'very.common@example.com':                        {"is_valid": True, "reason": ""},
        r'disposable.style.email.with+symbol@example.com': {"is_valid": True, "reason": ""},
        r'other.email-with-hyphen@example.com':            {"is_valid": True, "reason": ""},
        r'fully-qualified-domain@example.com':             {"is_valid": True, "reason": ""},
        r'user.name+tag+sorting@example.com':              {"is_valid": True, "reason": "may go to user.name@example.com inbox depending on mail server"},
        r'x@example.com':                                  {"is_valid": True, "reason": "one-letter local-part"},
        r'example-indeed@strange-example.com':             {"is_valid": True, "reason": "local domain name with no TLD, although ICANN highly discourages dotless email addresses[13]"},
        r'admin@mailserver1':                              {"is_valid": True, "reason": " "},
        r'example@s.example':                              {"is_valid": True, "reason": " "},
        r'" "@example.org':                                {"is_valid": True, "reason": "space between the quotes "},
        r'"john..doe"@example.org':                        {"is_valid": True, "reason": "quoted double dot "},
        r'mailhost!username@example.org':                  {"is_valid": True, "reason": "bangified host route used for uucp mailers"},
        r'user%example.com@example.org':                   {"is_valid": True, "reason": "% \escaped mail route to user@example.com via example.org"},
        r'Abc.example.com':                                {"is_valid": False, "reason": "no @ character"},
        r'A@b@c@example.com':                              {"is_valid": False, "reason": "only one @ is allowed outside quotation marks"},
        r'a"b(c)d,e,f;g<h>i[j\k]l@example.com':            {"is_valid": False, "reason": "none of the special characters in this local-part are allowed outside quotation marks"},
        r'just"not"right@example.com':                     {"is_valid": False, "reason": "quoted strings must be dot separated or the only element making up the local-part"},
        r'this is"not\allowed@example.com':                {"is_valid": False, "reason": "spaces, quotes, and backslashes may only exist when within quoted strings and preceded by a backslash"},
        r'this\ still\"not\\allowed@example.com':          {"is_valid": False, "reason": "even if escaped(preceded by a backslash), spaces, quotes, and backslashes must still be contained by quotes"},
        r'1234567890123456789012345678901234567890123456789012345678901234+x@example.com': {"is_valid": False, "reason": "local part is longer than 64 characters"},
        r'':                                               {"is_valid": False, "reason": "Empty email"},
    }

    usernames_to_test = {
        "usernameusername": {"is_valid": True, "reason": "Username is at max spaces"},
        "users":            {"is_valid": True, "reason": "Min length 5 chars of alphanumeric"},
        "user4":            {"is_valid": True, "reason": "Min length 5 chars of alphanumeric"},
        "u2352356235":      {"is_valid": True, "reason": "Min length 5 chars of alphanumeric"},
        "user_user1452":    {"is_valid": True, "reason": "Can have a single underscore"},
        "24553":            {"is_valid": False, "reason": "Must have at least one letter"},
        "1username":        {"is_valid": False, "reason": "Not allowed to start with number"},
        "user?name":        {"is_valid": False, "reason": "No special characters"},
        "user":             {"is_valid": False, "reason": "Too short"},
        "usernameusername1": {"is_valid": False, "reason": "Too long"},
        "user__name":       {"is_valid": False, "reason": "Cannot have multiple _ in a row"},
        "user-":            {"is_valid": False, "reason": "No trailing/prefixing _"},
        "_user":            {"is_valid": False, "reason": "No trailing/prefixing _"},
        "user_":            {"is_valid": False, "reason": "No trailing/prefixing _"},
        "us_ers":           {"is_valid": False, "reason": "Not 5 letters long"},
        "______":           {"is_valid": False, "reason": "Not 5 letters long"},
        "u3r55":            {"is_valid": False, "reason": "Not 5 letters long"},
        "2":                {"is_valid": False, "reason": "Not 5 letters long"},
        "":                 {"is_valid": False, "reason": "Empty username"},
    }

    first_names_to_test = {
        "seran":         {"is_valid": True, "reason": ""},
        "Seran":         {"is_valid": True, "reason": ""},
        "seran":         {"is_valid": True, "reason": ""},
        "Seran Seran":   {"is_valid": True, "reason": ""},
        "Seran-Seran":   {"is_valid": True, "reason": ""},
        " Seran":        {"is_valid": True, "reason": "User manager should strip spaces prefixed/suffixed spaces"},
        "Seran ":        {"is_valid": True, "reason": "User manager should strip spaces prefixed/suffixed spaces"},
        "Seran  Seran":  {"is_valid": True, "reason": "User manager should replace multiple whitespaces with 1"},
        "seranseranseranseranseranseran": {"is_valid": True, "reason": "Max length (30 chars)"},
        "seranseranseranseranseranserann": {"is_valid": False, "reason": "Too long {31 characters)"},
        "Seran-":        {"is_valid": False, "reason": "Cannot have leading/following hyphens"},
        "seran123seran": {"is_valid": False, "reason": "Cannot have numbers in first name"},
        "Seran--Seran":  {"is_valid": False, "reason": "Cannot have multiple hyphens in a row"},
        "-Seran":        {"is_valid": False, "reason": "Cannot have leading/following hyphens"},
        "":              {"is_valid": False, "reason": "Empty name"},
    }

    last_names_to_test = first_names_to_test

    valid_emails = [k for k, v in emails_to_test.items() if v["is_valid"]]
    valid_first_names = [
        k for k, v in first_names_to_test.items() if v["is_valid"]]
    valid_last_names = [
        k for k, v in last_names_to_test.items() if v["is_valid"]]
    valid_usernames = [
        k for k, v in usernames_to_test.items() if v["is_valid"]]

    valid_create_user_kwargs = {
        "email": valid_emails[0],
        "first_name": valid_first_names[0],
        "last_name": valid_last_names[0],
        "username": valid_usernames[0],
    }

    LARGE_IMAGE_URL = "https://via.placeholder.com/300"

    created_user: Optional[User] = None

    def tearDown(self):
        """Cleans up after every test execution"""
        self.delete_user()

    def delete_user(self, user: User = None):
        """Deletes a given user or the user specified in :param:user from the DB

        Keyword Arguments:
            user {User} -- The user to delete (default: {self.created_user})
        """
        if isinstance(user, User):
            user.delete()
        elif isinstance(self.created_user, User):
            self.created_user.delete()

    def assert_user_creation(self, kwargs: Dict[str, str], error_msg: str, is_valid: bool):
        """Tests creating a user for given kwargs with DB cleanup and assertions.

        Method attempts to create a user object for the given set of kwargs. If 
        :param:is_valid is True, then it will assert that the user is created.
        Otherwise, it will ensure that an exception is raised.

        Arguments:
            kwargs {Dict[str, str]} -- kwargs to pass to the User.create_user method
            error_msg {str} -- message to display if assertion error occurs
            is_valid {bool} -- True if the user should be successfully be created
        """

        user = None
        try:
            if is_valid:
                user = User.objects.create_user(**kwargs)
                user.full_clean()
            else:
                with self.assertRaises(Exception, msg=error_msg):
                    user = User.objects.create_user(**kwargs)
                    user.full_clean()
        except Exception as e:
            logger.exception(
                f"Exception occured when creating user for {kwargs}: {error_msg}", exc_info=True)
            raise e
        finally:
            self.delete_user(user)

    def test_first_names(self):
        """Tests creating users with first names in UserModelTests.first_names_to_test"""

        # Get a set of valid kwargs
        test_kwargs = copy.deepcopy(self.valid_create_user_kwargs)

        for name, data in self.first_names_to_test.items():

            # replace the arg for "first_name" with the value to test
            test_kwargs["first_name"] = name
            self.assert_user_creation(
                test_kwargs, data["reason"], data["is_valid"])

    # def test_last_names(self):
    #     """Tests creating users with last names in UserModelTests.last_names_to_test"""
    #     test_kwargs = copy.deepcopy(self.valid_create_user_kwargs)

    #     for name, data in self.last_names_to_test.items():
    #         test_kwargs["last_name"] = name
    #         self.assert_user_creation(
    #             test_kwargs, data["reason"], data["is_valid"])

    # def test_emails(self):
    #     """Tests creating users with emails in UserModelTests.emails_to_test"""
    #     test_kwargs = copy.deepcopy(self.valid_create_user_kwargs)

    #     for name, data in self.emails_to_test.items():
    #         test_kwargs["email"] = name
    #         self.assert_user_creation(
    #             test_kwargs, data["reason"], data["is_valid"])

    # def test_usernames(self):
    #     """Tests creating users with usernames in UserModelTests.usernames_to_test"""
    #     test_kwargs = copy.deepcopy(self.valid_create_user_kwargs)

    #     for name, data in self.usernames_to_test.items():
    #         test_kwargs["username"] = name
    #         self.assert_user_creation(
    #             test_kwargs, data["reason"], data["is_valid"])

    def test_user_avatar_resize(self):
        """Tests avatar images are downscaled"""
        # First creates a user with a large image
        response = requests.get(self.LARGE_IMAGE_URL)

        if response.status_code == 200:
            large_img = ContentFile(response.content, name="large_avatar.png")
            self.created_user: User = User.objects.create_user(
                **self.valid_create_user_kwargs, avatar=large_img)
            self.created_user.full_clean()
        else:
            raise HTTPError(
                f"Could not download large image: {response.status_code}")

        # Assert image size
        img = Image.open(self.created_user.avatar.path)
        self.assertLessEqual(
            img.height, 200, "Ensure that avatar height is downscaled")
        self.assertLessEqual(
            img.width, 200, "Ensure that avatar width is downscaled")


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
