import asyncio
from BLEHandler import BLEHandler
from helpers import find_device, input_handler
from FileHandler import FileHandler

DEVICE_NAME =           "Nano33BLE"
DATA_FILENAME =         "Data.csv"
FILE_BUFFER_SIZE =      100 # 100 rows are saved before 

async def main():
    file_handler = FileHandler(DATA_FILENAME, FILE_BUFFER_SIZE)
    address = await find_device(DEVICE_NAME)
    if not address:
        return
    ble_handler = BLEHandler(address, file_handler=file_handler)
    await ble_handler.connect()
    asyncio.create_task(ble_handler.monitor_connection())
    await input_handler(BLE_Handler=ble_handler)
    
if __name__ == "__main__":
    asyncio.run(main())
    