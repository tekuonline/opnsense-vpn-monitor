import requests
import time
import os
import json
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables
API_BASE_URL = os.getenv('API_BASE_URL')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))  # seconds

def is_service_up(service):
    """Check if a service is up: status connected and real_address is a valid IP"""
    status = service.get('status')
    real_address = service.get('real_address', '')
    # Consider up if status is 'connected' and real_address is not empty and not '0.0.0.0'
    return status == 'connected' and real_address and real_address != '0.0.0.0'

def check_and_restart_services():
    """Check OpenVPN services and restart if down"""
    try:
        # Create a session with basic auth
        session = requests.Session()
        session.auth = (API_KEY, API_SECRET)  # Basic auth with key/secret

        # API call to get sessions
        url = f"{API_BASE_URL}/api/openvpn/service/search_sessions"
        response = session.post(url, data='')
        response.raise_for_status()
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Response status: {response.status_code}")
            logging.error(f"Response text: {response.text[:500]}")  # Log first 500 chars
            return

        logging.info(f"Checked {data.get('total', 0)} services")

        for service in data.get('rows', []):
            service_id = service.get('id')
            description = service.get('description', f'ID {service_id}')
            if not is_service_up(service):
                logging.warning(f"Service {description} (ID {service_id}) is down. Restarting...")
                restart_url = f"{API_BASE_URL}/api/openvpn/service/restart_service/{service_id}"
                restart_headers = {
                    'Content-Type': 'text/plain'
                }
                restart_response = session.post(restart_url, headers=restart_headers, data='{}')
                restart_response.raise_for_status()
                try:
                    restart_data = restart_response.json()
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse restart JSON response: {e}")
                    logging.error(f"Restart response status: {restart_response.status_code}")
                    logging.error(f"Restart response text: {restart_response.text[:500]}")
                    continue
                if restart_data.get('result') == 'ok':
                    logging.info(f"Successfully restarted service {description} (ID {service_id})")
                else:
                    logging.error(f"Failed to restart service {description} (ID {service_id}): {restart_data}")
            else:
                logging.info(f"Service {description} (ID {service_id}) is up")

    except requests.RequestException as e:
        logging.error(f"Error during API call: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def main():
    if not all([API_BASE_URL, API_KEY, API_SECRET]):
        logging.error("API_BASE_URL, API_KEY, and API_SECRET must be set in environment variables")
        sys.exit(1)

    logging.info("Starting OPNsense VPN Monitor service")
    logging.info(f"API Base URL: {API_BASE_URL}")
    logging.info(f"Check Interval: {CHECK_INTERVAL} seconds")

    while True:
        check_and_restart_services()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()