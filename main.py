import asyncio
from BLEHandler import BLEHandler
from helpers import find_device, input_handler
from FileHandler import FileHandler

DEVICE_NAME =           "Nano33BLE"
DATA_FILENAME =         "Data.csv"
FILE_BUFFER_SIZE =      10

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
    asyncio.create_task(input_handler(BLE_Handler=ble_handler1))
    asyncio.create_task(ble_handler2.monitor_connection())
    asyncio.create_task(input_handler(BLE_Handler=ble_handler2))
    
if __name__ == "__main__":
    asyncio.run(main())
    
