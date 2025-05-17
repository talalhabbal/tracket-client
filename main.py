import sys
sys.coinit_flags = 0
from bleak.backends.winrt.util import uninitialize_sta
import asyncio
from BLEHandler import BLEHandler
from helpers import find_device, input_handler
from FileHandler import FileHandler
from CamHandler import CamHandler

DEVICE_NAME =           "Nano33BLE"
DATA_FILENAME =         "Data.csv"
CAM_OUTPUT_FOLDER =     "cam_output"
FILE_BUFFER_SIZE =      10

async def main():
    address = await find_device(DEVICE_NAME)
    if not address:
        return
    cam_handler = CamHandler(CAM_OUTPUT_FOLDER)
    file_handler = FileHandler(DATA_FILENAME, FILE_BUFFER_SIZE)
    ble_handler = BLEHandler(address, file_handler=file_handler, cam_handler=cam_handler)
    await ble_handler.connect()
    asyncio.create_task(ble_handler.monitor_connection())
    await input_handler(BLE_Handler=ble_handler)
    
if __name__ == "__main__":
    uninitialize_sta()
    asyncio.run(main())
    