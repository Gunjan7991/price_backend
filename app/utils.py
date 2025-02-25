import requests
import time
import logging
from passlib.context import CryptContext

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_heating_oil(product_id: str = "426", contract_number: int = 1, timeout: int = 10) -> float:
    """
    Fetches the latest heating oil price from the CME Group API.

    :param product_id: ID of the product (default: "426" for Heating Oil).
    :param contract_number: Contract number to fetch (default: 1).
    :param timeout: Timeout in seconds for the request (default: 10).
    :return: The latest heating oil price as a float.
    """
    # Generate dynamic timestamp
    timestamp = int(time.time() * 1000)
    xhr_url = f"https://www.cmegroup.com/CmeWS/mvc/quotes/v2/contracts-by-number?isProtected&_t={timestamp}"

    # Headers copied from cURL
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.cmegroup.com",
        "referer": "https://www.cmegroup.com/markets/energy/refined-products/heating-oil.html",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "cookie": "YOUR_SESSION_COOKIE_HERE"  # Update this with a fresh session cookie if needed
    }

    # Data payload
    payload = {
        "productIds": [product_id],
        "contractsNumber": [contract_number],
        "type": "VOLUME",
        "showQuarterly": [0]
    }

    try:
        # Send the request
        response = requests.post(xhr_url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse JSON response
        data = response.json()

        # Extract the latest price
        if isinstance(data, list) and len(data) > 0:
            heating_oil_price = data[0].get("last", "N/A")
            return float(heating_oil_price)
        else:
            logging.warning("⚠️ No price data found in response.")
            return 0.0

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to fetch data: {e}")
        return 0.0
    except ValueError as e:
        logging.error(f"❌ JSON Parsing Error: {e}")
        return 0.0


