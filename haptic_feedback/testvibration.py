import asyncio
from bleak import BleakClient

# Replace with your Amazfit's Bluetooth MAC address
DEVICE_MAC_ADDRESS = "F9:77:1C:2C:91:42"
VIBRATION_CHARACTERISTIC_UUID = "00002A46-0000-1000-8000-00805f9b34fb"  # Replace with your vibration characteristic's UUID

async def vibrate():
    async with BleakClient(DEVICE_MAC_ADDRESS) as client:
        print("Connected to Amazfit GTR")

        try:
            # Sending the vibration command
            vibration_command = b'\x01\x00\x19\x00\x01'  # Adjust this if necessary
            await client.write_gatt_char(VIBRATION_CHARACTERISTIC_UUID, vibration_command)
            print("Vibration command sent.")
            await asyncio.sleep(1)  # Wait for 1 second to allow the vibration to complete
        except Exception as e:
            print(f"Failed to send vibration command: {e}")

# Run the main function
asyncio.run(vibrate())
