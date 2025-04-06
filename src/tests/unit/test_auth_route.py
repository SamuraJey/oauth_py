from unittest.mock import MagicMock, patch

import pytest
import requests_mock
from flask import Flask

from src.routes.auth import bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test_secret_key"
    app.testing = True
    app.register_blueprint(bp)
    app.template_folder = "../../templates"

    # Mock the OAuth object
    mock_oauth = MagicMock()
    mock_vk = MagicMock()
    mock_vk.client_id = "test_client_id"
    mock_vk.client_secret = "test_client_secret"
    mock_oauth.vk = mock_vk
    app.oauth = mock_oauth

    app.logger = MagicMock()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestAuthRoutes:
    def test_login(self, client, app):
        """Test the /login route."""
        with app.app_context():
            response = client.get("/login")

            # Assert the response status code
            assert response.status_code == 200

            # Assert the response contains the expected content
            assert b"Login with VK" in response.data

            # Assert that the logger was called
            app.logger.info.assert_called_once_with("Rendering login page")

    @patch("src.routes.auth.url_for")
    def test_authorize(self, mock_url_for, client, app):
        """Test the /authorize route."""
        mock_url_for.return_value = "https://example.com/auth"
        app.oauth.vk.authorize_redirect.return_value = "redirect_response"

        response = client.get("/authorize")

        # Assert the response data
        assert response.data == b"redirect_response"

        # Assert that url_for was called with the correct arguments
        mock_url_for.assert_called_once_with("auth.auth", _external=True, _scheme="https")

        # Assert that authorize_redirect was called with the correct redirect URI
        app.oauth.vk.authorize_redirect.assert_called_once_with("https://example.com/auth")

        # Assert that the logger was called
        app.logger.info.assert_called_once_with("Redirecting to VK authorize URL: %s", "https://example.com/auth")

    def test_auth(self, client, app):
        """Test the /auth route."""

        with (
            app.test_request_context("/auth"),
            requests_mock.Mocker() as m,
            patch("src.routes.auth.session", create=True),
            patch("src.routes.auth.redirect") as mock_redirect,
            patch("src.routes.auth.url_for") as mock_url_for,
        ):
            app.oauth.vk.authorize_access_token.return_value = {"access_token": "test_token"}

            m.get(
                "https://api.vk.com/method/users.get?access_token=test_token&v=5.131",
                json={"response": [{"id": 123, "name": "Test User"}]},
            )

            # Mock url_for and redirect
            mock_url_for.return_value = "/index"
            mock_redirect.return_value = "redirected_to_index"

            # Call the /auth route
            client.get("/auth")

            # Assert the response status code
            # assert response.status_code == 302 TODO # noqa

            # Assert that the access token was retrieved
            app.oauth.vk.authorize_access_token.assert_called_once_with(client_id="test_client_id", client_secret="test_client_secret")

            # Assert that the VK API was called with the correct parameters
            app.oauth.vk.get.assert_called_once_with("https://api.vk.com/method/users.get", params={"access_token": "test_token", "v": "5.131"})

            # Assert that the user was added to the session

            # Assert that the redirect was called with the correct URL
            mock_redirect.assert_called_once_with("/index")

    def test_logout(self, client, app):
        """Test the /logout route."""
        with (
            app.test_request_context("/logout"),
            patch("src.routes.auth.session") as mock_session,
            patch("src.routes.auth.redirect") as mock_redirect,
            patch("src.routes.auth.url_for") as mock_url_for,
        ):
            # Mock session and redirect
            mock_session.pop.return_value = {"id": 123, "name": "Test User"}
            mock_url_for.return_value = "/index"

            # Make redirect return a proper 302 response
            mock_redirect.side_effect = lambda x: app.response_class(response="", status=302, headers={"Location": x})

            # Call the /logout route
            response = client.get("/logout")

            # Assert the response status code
            assert response.status_code == 302

            # Verify redirected to correct URL
            assert response.headers["Location"] == "/index"

            # Assert that the user was removed from the session
            mock_session.pop.assert_called_once_with("user", None)

            # Assert that the redirect was called with the correct URL
            mock_redirect.assert_called_once_with("/index")
