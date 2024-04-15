import os
import uuid
import json
from datetime import datetime, timezone

class IoTDevice:
    def __init__(self, product_code):
        self.product_code = product_code
        self.uuid = str(uuid.uuid4())  # Convert UUID to string
        self.timestamp = datetime.now(timezone.utc).isoformat()  # Get current UTC timestamp

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    product_code = config['product_code']

# Generate devices
devices = []
uuid_set = set()  # Set to store generated UUIDs
package_number = 1
devices_per_package = 1000000  # Set the number of devices per package
package_number_index = 0
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
                "used":0
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
    index=0
    if package_number_index > package_number:
        break

print("All packages generated.")
