from uds.Uds import Uds
import time

# Constants
MAX_RETRIES = 10  # Number of retries
RETRY_DELAY = 0.5  # Delay between retries in seconds

def send_with_retry(uds_instance, request):
    for attempt in range(MAX_RETRIES):
        try:
            response = uds_instance.send(request)
            return response  # Return the successful response
        except Exception as e:
            if "Timeout in waiting for message" in str(e):
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(RETRY_DELAY)  # Wait before retrying
            else:
                raise  # Re-raise other exceptions immediately
    raise Exception("Max retries reached. Communication failed.")

def initialize_uds(driver_type, request_id, response_id, **kwargs):
    """
    Initialize the UDS instance based on driver type and user inputs.

    Parameters:
    - driver_type (str): The type of driver to use ('kvaser', 'peak', or 'vector').
    - request_id (int): The request ID.
    - response_id (int): The response ID.
    - **kwargs: Additional parameters based on the driver type.

    Returns:
    - Uds instance
    """
    if driver_type == "peak":
        return Uds(reqId=request_id, resId=response_id, interface="peak", device=kwargs.get("device", "PCAN_USBBUS1"))
    elif driver_type == "kvaser":
        return Uds(reqId=request_id, resId=response_id, transportProtocol="CAN", interface="kvaser", channel=kwargs.get("channel", 0), bitrate=kwargs.get("bitrate", 500000))
    elif driver_type == "vector":
        return Uds(reqId=request_id, resId=response_id, transportProtocol="CAN", interface="vector", channel=kwargs.get("channel", 0), app_name=kwargs.get("app_name", "BALCAN"))
    else:
        raise ValueError("Unsupported driver type. Please select 'kvaser', 'peak', or 'vector'.")



