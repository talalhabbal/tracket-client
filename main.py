import asyncio
from BLEHandler import BLEHandler
from helpers import find_device, input_handler

async def main():
    address = await find_device()
    if not address:
        return
    handler = BLEHandler(address)
    await handler.connect()
    asyncio.create_task(handler.monitor_connection())
    await input_handler(BLE_Handler=handler)
    
if __name__ == "__main__":
    asyncio.run(main())
    