import sys
sys.coinit_flags=0
try:
    from bleak.backends.winrt.util import allow_sta
    allow_sta()
except ImportError:
    pass
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
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
    file_handler = FileHandler(DATA_FILENAME, FILE_BUFFER_SIZE)
    cam_handler = CamHandler(CAM_OUTPUT_FOLDER)
    asyncio.create_task(cam_handler.warm_up())
    ble_handler = BLEHandler(address, file_handler=file_handler, cam_handler=cam_handler)
    await ble_handler.connect()
    asyncio.create_task(ble_handler.monitor_connection())
    await input_handler(BLE_Handler=ble_handler, cam_handler=cam_handler)
    

    
if __name__ == "__main__":
    asyncio.run(main())
    