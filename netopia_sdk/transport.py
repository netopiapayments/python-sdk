import json
import requests
from typing import Type, TypeVar, Any
from .logger import logger

T = TypeVar("T")


class Transport:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def send_request(self, endpoint: str, payload: Any, response_class: Type[T]) -> T:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

        json_payload = json.dumps(payload, default=lambda o: o.__dict__)
        logger.debug(f"Sending POST request to {url} with payload: {json_payload}")

        try:
            response = requests.post(url, headers=headers, data=json_payload, timeout=30)
            logger.debug(f"Received response code: {response.status_code}, body: {response.text}")

            response.raise_for_status()
            response_data = json.loads(response.text)

            return response_class(**response_data)
        except requests.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to parse response into {response_class.__name__}: {e}")
            raise
