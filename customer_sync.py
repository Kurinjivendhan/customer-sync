import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from database  import save_customers

API_URL = "https://jsonplaceholder.typicode.com/users"

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def create_session():
    retry_policy = Retry(
        total = 3,
        connect = 3,
        red = 3,
        status = 3,
        backoff_factor=0.5,
        status_forcelist=[429,500,502,503,504],
        allowed_methods = {"GET}"},
        respect_retry_after_header = True,
    )

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_policy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def validate_customer(customer):
    if not isinstance(customer, dict):
        return False

    customer_id = customer.get("id")
    name = customer.get("name")
    email = customer.get("email")

    if not isinstance(customer_id, int) or isinstance(customer_id, bool):
        return False

    if customer_id <= 0:
        return False

    if not isinstance(name, str) or not name.strip():
        return False

    if not isinstance(email, str) or "@" not in email:
        return False

    return True


def get_valid_customers(records):
    valid_customers = []
    seen_ids = set()

    for record in records:
        if not validate_customer(record):
            logger.warning("Skipping an invalid customer record")
            continue

        customer_id = record["id"]

        if customer_id in seen_ids:
            logger.warning("Skipping duplicate customer ID %s", customer_id)
            continue

        seen_ids.add(customer_id)

        valid_customers.append({
            "id": customer_id,
            "name": record["name"].strip(),
            "email": record["email"].strip(),
        })

    return valid_customers


def sync_customers():
    session = create_session()

    try:
        logger.info("Customer sync started")

        response = session.get(API_URL, timeout=(3, 10))
        response.raise_for_status()

        try:
            records = response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error("The API returned malformed JSON")
            return

        if not isinstance(records, list):
            logger.error("Unexpected API response structure")
            return

        customers = get_valid_customers(records)

        saved_count = save_customers(customers)

        logger.info(
            "Customer sync completed: received=%d valid=%d processed=%d",
            len(records),
            len(customers),
            saved_count,
        )

    except requests.exceptions.Timeout:
        logger.error("The API request timed out")

    except requests.exceptions.HTTPError as error:
        logger.error("API HTTP request failed: %s", error)

    except requests.exceptions.RequestException as error:
        logger.error("API request failed: %s", error)

    except Exception:
        logger.exception("Customer sync failed")

    finally:
        session.close()


if __name__ == "__main__":
    sync_customers()