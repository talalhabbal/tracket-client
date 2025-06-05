import asyncio
from BLEHandler import BLEHandler
from helpers import find_device
from FileHandler import FileHandler

DEVICE_NAME =           "Nano33BLE"
DATA_FILENAME =         "Data.csv"
FILE_BUFFER_SIZE =      10

async def input_handler(handler1: BLEHandler, handler2: BLEHandler):
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
            await handler1.start_reading()
            await handler2.start_reading()
        elif command == "stop":
            await handler1.stop_reading()
            await handler2.stop_reading()
        elif command == "exit":
            await handler1.stop_reading()
            await handler2.stop_reading()
            await handler1.disconnect()
            await handler2.disconnect()
            print("Exiting Program...")
            break

async def main():
    file_handler1 = FileHandler(DATA_FILENAME, FILE_BUFFER_SIZE)
    address1 = await find_device(DEVICE_NAME)
    if not address1:
        return
    ble_handler1 = BLEHandler(address1, file_handler=file_handler1)
    await ble_handler1.connect()

    file_handler2 = FileHandler(DATA_FILENAME, FILE_BUFFER_SIZE)
    address2 = await find_device(DEVICE_NAME + "2")
    if not address2:
        return
    ble_handler2 = BLEHandler(address2, file_handler=file_handler2)
    await ble_handler2.connect()


    asyncio.create_task(ble_handler1.monitor_connection())
    asyncio.create_task(ble_handler2.monitor_connection())
    await input_handler(ble_handler1, ble_handler2)
    
if __name__ == "__main__":
    asyncio.run(main())
    
