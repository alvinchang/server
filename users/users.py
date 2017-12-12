from enum import Enum


class UserJsonKeys(Enum):
    USERS = "users"
    USER_NAME = "user_name"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"


class User:

    def __init__(self, user_name, first_name, last_name, email):
        self._user_name = user_name
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    @classmethod
    def from_json(cls, json_):
        user_name = json_.get(UserJsonKeys.USER_NAME.value, None)
        first_name = json_.get(UserJsonKeys.FIRST_NAME.value, None)
        last_name = json_.get(UserJsonKeys.LAST_NAME.value, None)
        email = json_.get(UserJsonKeys.EMAIL.value, None)
        if user_name is not None:
            return cls(
                user_name=user_name,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        else:
            return cls.from_general_username(first_name, last_name)

    @classmethod
    def from_general_username(cls, first_name, last_name):
        return cls(
            user_name=first_name+last_name,
            first_name=first_name,
            last_name=last_name,
            email="{}.{}.email.com".format(first_name, last_name)
        )

    @property
    def user_name(self):
        return self._user_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

