from uds_connect import initialize_uds,send_with_retry




def main():
    # User can set the driver type, request ID, and response ID here
    driver_type = "vector"  # Change to 'kvaser' or 'vector' as needed
    request_id = 0x7D2
    response_id = 0x7D3
    # Additional kwargs based on driver type
    # additional_params = {
    #     # "device": "PCAN_USBBUS1",  # For 'peak' driver
    #     "channel": 0,            # For 'kvaser' or 'vector' drivers
    #     "bitrate": 500000,       # For 'kvaser' driver
    #     # "app_name": "BALCAN"     # For 'vector' driver
    # }

    additional_params = {
    # "device": "PCAN_USBBUS1"  # For 'peak' driver
    "channel": 0,            # For 'kvaser' or 'vector' drivers
    # "bitrate": 500000,       # For 'kvaser' driver
    "app_name": "BALCAN"     # For 'vector' driver
}


    # Instantiate the UDS instance with specified configuration
    uds_instance = initialize_uds(driver_type, request_id, response_id, **additional_params)

    # UDS requests
    vin_number = send_with_retry(uds_instance, [0x22, 0xF1, 0x90])
    hex_file = send_with_retry(uds_instance, [0x22, 0xF1, 0x11])
    assembly_part_num = send_with_retry(uds_instance, [0x22, 0xF1, 0x87])
    hw_serial_number = send_with_retry(uds_instance, [0x22, 0xF1, 0x8C])

    # Formatting responses
    formatted_vin = vin_number[3:]
    formatted_hex = hex_file[3:]
    formatted_assembly_num = assembly_part_num[3:]
    formatted_hw_serial_num = hw_serial_number[3:]

    # Converting byte data to string
    result_vin = ''.join(chr(num) for num in formatted_vin)
    result_hex = ''.join(chr(num) for num in formatted_hex)
    result_assembly_num = ''.join(chr(num) for num in formatted_assembly_num)
    result_serial_num = ''.join(chr(num) for num in formatted_hw_serial_num)

    # Collect vehicle data
    vehicle_data = {
        'vin_number': result_vin,
        'hex_file_name': result_hex,
        'assembly_part_number': result_assembly_num,
        'hw_serial_number': result_serial_num
    }

    print(vehicle_data)


if __name__=="__main__":
    main()