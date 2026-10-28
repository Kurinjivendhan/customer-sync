
import logging
import requests


from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from database import save_customers

API_URL = "https://jsonplaceholder.typicode.com/users"


def create_session():
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)

    return session


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


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
            logger.warning("Skipping invalid customer record")
            continue

        customer_id = record["id"]

        if customer_id in seen_ids:
            logger.warning("Skipping duplicate ID %s", customer_id)
            continue

        seen_ids.add(customer_id)

        valid_customers.append({
            "id": customer_id,
            "name": record["name"].strip(),
            "email": record["email"].strip(),
        })

    return valid_customers


def sync_customers():
    try:
        logger.info("Customer sync started")

        session = create_session()
        response = session.get(API_URL, timeout=(3, 10))
        response.raise_for_status()

        try:
            records = response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error("API returned malformed JSON")
            return

        if not isinstance(records, list):
            logger.error("Unexpected API response structure")
            return

        customers = get_valid_customers(records)
        saved_count = save_customers(customers)

        logger.info(
            "Sync completed: received=%d valid=%d processed=%d",
            len(records),
            len(customers),
            saved_count,
        )

    except requests.exceptions.RequestException:
        logger.exception("External API request failed")

    except Exception:
        logger.exception("Customer sync failed")


if __name__ == "__main__":
    sync_customers()
