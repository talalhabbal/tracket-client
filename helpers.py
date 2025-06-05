import asyncio
from bleak import BleakScanner


async def input_handler(BLE_Handler, cam_handler):
    """
    Handles User input to control starting and stopping readings from connected device.
    Args:
        BLE_Handler: :class:`BLEHandler` class to call functions from within it based on user input.
    Returns:
        None
    """
    loop = asyncio.get_running_loop()
    while True:
        command = await loop.run_in_executor(None, input, "Enter 'start', 'stop', or 'exit': ")
        command = command.strip().lower()
        if command == "start":
            # asyncio.create_task(BLE)
            await BLE_Handler.start_reading()
        elif command == "stop":
            await BLE_Handler.stop_reading()
        elif command == "exit":
            await BLE_Handler.stop_reading()
            await BLE_Handler.disconnect()
            print("Exiting Program...")
            break


async def find_device(device_name):
    """
    Discovers devices using :class:`BleakScanner.discover()` and looks for the device with the specified name.
    Returns:
        Device's `address` if the device was found. `None` if the device was not found.
    """
    print("Scanning for nearby BLE devices")
    device_list = await BleakScanner.discover(timeout=10) # Returns a list of devices that it discovered while scanning
    for device in device_list:
        print(f"Found device: {device.name} - {device.address}")
        if device.name and device_name in device.name: # If DEVICE_NAME is in the name of the device then it found the device
            print(f"Found target device with name {device.name} with address {device.address}")
            return device.address
    print("Device not found!")
    return None