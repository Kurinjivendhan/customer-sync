
import unittest
from unittest.mock import patch

from customer_sync import validate_customer, get_valid_customers


class TestCustomerSync(unittest.TestCase):

    def test_valid_customer(self):
        customer = {
            "id": 101,
            "name": "Arun",
            "email": "arun@example.com",
        }

        self.assertTrue(validate_customer(customer))

    def test_empty_name_is_invalid(self):
        customer = {
            "id": 102,
            "name": " ",
            "email": "priya@example.com",
        }

        self.assertFalse(validate_customer(customer))

    def test_invalid_email_is_rejected(self):
        customer = {
            "id": 103,
            "name": "Kumar",
            "email": "invalid-email",
        }

        self.assertFalse(validate_customer(customer))

    def test_duplicate_ids_are_removed(self):
        records = [
            {"id": 101, "name": "Arun", "email": "arun@example.com"},
            {"id": 101, "name": "Arun", "email": "arun@example.com"},
            {"id": 102, "name": "Priya", "email": "priya@example.com"},
        ]

        result = get_valid_customers(records)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 101)
        self.assertEqual(result[1]["id"], 102)


if __name__ == "__main__":
    unittest.main()
