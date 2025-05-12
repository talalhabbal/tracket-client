import asyncio
from CameraHandler import CameraHandler
from camera import CamHandler
async def main():
    # cam = CameraHandler()
    cam = CamHandler()
    record_task = asyncio.create_task(cam.start_recording("cam_output", "auto5s"))
    await asyncio.sleep(20)
    await cam.stop_recording()
    await record_task
    print("5 second clip saved")
    
    # print("Commands: start | stop | exit")
    # while True:
    #     cmd = await asyncio.to_thread(input, "> ")
    #     cmd = cmd.strip().lower()

    #     if cmd == "start":
    #         if record_task and not record_task.done():
    #             print("⚠️ Already recording!")
    #         else:
    #             fname = f"session{session}"
    #             record_task = asyncio.create_task(
    #                 cam.start_recording("cam_output", fname)
    #             )
    #             session += 1

    #     elif cmd == "stop":
    #         if record_task and not record_task.done():
    #             # signal stop, then await the task to finish cleanup
    #             await cam.stop_recording()
    #             await record_task
    #         else:
    #             print("⚠️ Not currently recording.")

    #     elif cmd == "exit":
    #         if record_task and not record_task.done():
    #             await cam.stop_recording()
    #             await record_task
    #         print("Exiting.")
    #         break

    #     else:
    #         print("Unknown command. Use start, stop, or exit.")

if __name__ == "__main__":
    asyncio.run(main())
