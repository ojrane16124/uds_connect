# uds_connect

`uds_connect` is a Python package for interacting with UDS (Unified Diagnostic Services) over various CAN interfaces, such as `peak`, `kvaser`, and `vector`.

## Installation

```bash
pip install uds_connect
```

## Example Usage
```
from uds_connect import initialize_uds, send_with_retry

# Define the driver type, request ID, and response ID
driver_type = "kvaser"  # Options: 'peak', 'kvaser', 'vector'
request_id = 0x7D2
response_id = 0x7D3

# Additional parameters based on the driver type
additional_params = {
    # "device": "PCAN_USBBUS1",  # For 'peak' driver
    "channel": 0,               # For 'kvaser' or 'vector' drivers
    "bitrate": 500000,          # For 'kvaser' driver
    # "app_name": "BALCAN"       # For 'vector' driver
}

# Initialize the UDS instance with the specified configuration
uds_instance = initialize_uds(driver_type, request_id, response_id, **additional_params)

# UDS requests
vin_number = send_with_retry(uds_instance, [0x22, 0xF1, 0x90])
hex_file = send_with_retry(uds_instance, [0x22, 0xF1, 0x11])
assembly_part_num = send_with_retry(uds_instance, [0x22, 0xF1, 0x87])
hw_serial_number = send_with_retry(uds_instance, [0x22, 0xF1, 0x8C])

# Format responses by removing the first three bytes (header)
formatted_vin = vin_number[3:]
formatted_hex = hex_file[3:]
formatted_assembly_num = assembly_part_num[3:]
formatted_hw_serial_num = hw_serial_number[3:]

# Convert byte data to a readable string format
result_vin = ''.join(chr(num) for num in formatted_vin)
result_hex = ''.join(chr(num) for num in formatted_hex)
result_assembly_num = ''.join(chr(num) for num in formatted_assembly_num)
result_serial_num = ''.join(chr(num) for num in formatted_hw_serial_num)

# Collect vehicle data in a dictionary
vehicle_data = {
    'vin_number': result_vin,
    'hex_file_name': result_hex,
    'assembly_part_number': result_assembly_num,
    'hw_serial_number': result_serial_num
}

print(vehicle_data)
```