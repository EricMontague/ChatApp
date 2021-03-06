"""This file contains fixtures to be used in tests for the helper functions."""


import pytest
from marshmallow import ValidationError
from app import create_app


class FakeValidationError(ValidationError):

    def __init__(self, message, field_name):
        self.message = message
        super().__init__(self.message)
        self.messages = {field_name: self.message}


class FakeErrorSchema:
    """Fake marshmallow schema whose methods raise ValidationErrors."""

    def __init__(self, field_name="_schema"):
        self.validation_error = FakeValidationError("Error successfully raised", field_name)

    def load(self, data):
        raise self.validation_error
       
    def dump(self, model):
        raise self.validation_error


class FakeDataSchema:
    """Fake marshmallow schema whose methods return dictionaries."""

    RESOURCE_NAME = "User"
    COLLECTION_NAME = "Users"

    def __init__(self):
        self.user_data = {
            "id": 2,
            "username": "Brad12",
            "password": "test_password",
            "location": {
                "state": "New York",
                "city": "New York",
                "country": "US"
            }
        }

    def load(self, data):
        return data

    def dump(self, model):
        return self.user_data


class FakeHeaders(dict):
    """Class that mimics the necessary methods and attributes of a Werkzeug Headers object."""

    def __init__(self):
        super().__init__()

    def extend(self, extra_headers):
        """Add extra headers to the FakeHeaders object."""
        self.update(extra_headers)


class FakeResponse:
    """Class that mimics the necessary methods an attributes of a Flask Response
    object.
    """

    def __init__(self):
        self.headers = FakeHeaders()
        self.status_code = 200
        self.data = "Fake Flask response!"


@pytest.fixture
def flask_app():
    """Create an instance of the application and push an application
    context.
    """
    app = create_app(config_name="testing")
    app.config["SERVER_NAME"] = "http://localhost:5000"
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture
def fake_error_schema_class():
    """Return a fake marshmallow schema that only throws errors"""
    return FakeErrorSchema


@pytest.fixture
def fake_data_schema():
    """Return a fake marshmallow schema whose methods returns data."""
    return FakeDataSchema()


@pytest.fixture
def fake_response():
    """Return an instance of a FakeResponse object."""
    return FakeResponse()
