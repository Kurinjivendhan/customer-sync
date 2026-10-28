
from customer_sync import validate_customer, get_valid_customers


def test_validate_customer_with_valid_data():
    customer = {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com",
    }

    assert validate_customer(customer) is True


def test_validate_customer_with_invalid_email():
    customer = {
        "id": 1,
        "name": "John Smith",
        "email": "invalid-email",
    }

    assert validate_customer(customer) is False


def test_get_valid_customers_removes_duplicate_ids():
    records = [
        {"id": 1, "name": "John", "email": "john@example.com"},
        {"id": 1, "name": "John Again", "email": "john2@example.com"},
        {"id": 2, "name": "Mary", "email": "mary@example.com"},
    ]

    result = get_valid_customers(records)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2



from unittest.mock import Mock, patch
import requests
import customer_sync


@patch("customer_sync.save_customers")
@patch("customer_sync.create_session")
def test_api_server_error_does_not_save_data(mock_create_session, mock_save):
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )

    mock_create_session.return_value.get.return_value = response

    customer_sync.sync_customers()

    mock_save.assert_not_called()


@patch("customer_sync.save_customers")
@patch("customer_sync.create_session")
def test_malformed_json_does_not_save_data(mock_create_session, mock_save):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Invalid JSON", "{invalid", 1
    )

    mock_create_session.return_value.get.return_value = response

    customer_sync.sync_customers()

    mock_save.assert_not_called()


@patch("customer_sync.save_customers")
@patch("customer_sync.create_session")
def test_unexpected_response_structure_does_not_save_data(
    mock_create_session, mock_save
):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"users": "not-a-list"}

    mock_create_session.return_value.get.return_value = response

    customer_sync.sync_customers()

    mock_save.assert_not_called()
