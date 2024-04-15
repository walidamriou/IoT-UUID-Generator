import os
import uuid
import json
from datetime import datetime, timezone

class IoTDevice:
    def __init__(self, product_code):
        self.product_code = product_code
        self.uuid = str(uuid.uuid4())  # Convert UUID to string
        self.timestamp = datetime.now(timezone.utc).isoformat()  # Get current UTC timestamp

def generate_devices(package_number, devices_per_package, product_code):
    devices = []
    uuid_set = set()  # Set to store generated UUIDs
    package_number_index = 1
    index = 1  # Initialize index for the devices
    while len(devices) < package_number * devices_per_package:  # Generate devices for xpackage_number
        package_devices = []  # Devices for the current package
        for _ in range(devices_per_package):  # Generate devices for the current package
            device = IoTDevice(product_code)
            if device.uuid not in uuid_set:  # Check for duplicate UUIDs
                package_devices.append({
                    "package": package_number_index,
                    "index": index,
                    "product_code": device.product_code,
                    "uuid": device.uuid,
                    "timestamp": device.timestamp,
                    "used": 0
                })
                uuid_set.add(device.uuid)
                index += 1  # Increment index for each device
        # Write devices to JSON file for the current package
        package_dir = f"package_{package_number_index}"
        os.makedirs(package_dir, exist_ok=True)  # Create package directory if it doesn't exist
        with open(os.path.join(package_dir, 'devices.json'), 'w') as devices_file:
            json.dump(package_devices, devices_file, indent=4)
        print(f"Package {package_number_index}: Devices written to {package_dir}/devices.json file.")
        package_number_index += 1
        index = 0
        if package_number_index > package_number:
            break

def get_user_input():
    try:
        package_number = int(input("Enter the number of packages: "))
        devices_per_package = int(input("Enter the number of devices per package: "))
        product_code = input("Enter the product code: ")
    except ValueError:
        print("Error: Please enter valid integer values.")
        return None, None, None
    return package_number, devices_per_package, product_code

if __name__ == "__main__":
    print("--------------------------------------------------------------------------------")
    print(" IoT UUID Generator Tool")
    print("--------------------------------------------------------------------------------")
    print(" version: dev-0.0.1.2")
    print(" last update: 15/04/2024")
    print(" Authors: . Walid Amriou ")
    print("--------------------------------------------------------------------------------\n")

    package_number, devices_per_package, product_code = get_user_input()
    if package_number is not None and devices_per_package is not None and product_code:
        generate_devices(package_number, devices_per_package, product_code)
        print("--------------------------------------------------------------------------------")
        print(" Done.")
        print("--------------------------------------------------------------------------------")
        exit()
    else:
        print("Exiting due to invalid input.")
        exit()
