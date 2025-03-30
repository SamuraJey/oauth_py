from unittest.mock import MagicMock, patch

import pytest

from src.app.config.dotenv_load import SiteSettings
from src.db.database import add_design_document


@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=SiteSettings)
    settings.couchdb_user = MagicMock()  # Mock couchdb_user
    settings.couchdb_user.get_secret_value.return_value = "test_user"
    settings.couchdb_password = MagicMock()  # Mock couchdb_password
    settings.couchdb_password.get_secret_value.return_value = "test_password"
    settings.couchdb_url = "test_url"
    settings.couchdb_port = "1234"
    return settings


class TestAddDesignDocument:
    @patch("requests.put")
    def test_add_design_document_success(self, mock_put, mock_settings):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_put.return_value = mock_response

        add_design_document(mock_settings, "test_db")

        mock_put.assert_called_once()

    @patch("requests.put")
    def test_add_design_document_already_exists(self, mock_put, mock_settings):
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_put.return_value = mock_response

        add_design_document(mock_settings, "test_db")

        mock_put.assert_called_once()

    @patch("requests.put")
    def test_add_design_document_failure(self, mock_put, mock_settings):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_put.return_value = mock_response

        add_design_document(mock_settings, "test_db")

        mock_put.assert_called_once()
