import asyncio
import os
import cv2

class CamHandler:
    def __init__(self, camera_index=1, target_fps=60):
        """
        camera_index: which device to open (0, 1, 2, …). 
        On most laptops, 0 = built-in, 1 = first external USB camera.
        """
        self.camera_index = camera_index
        self.target_fps = target_fps

        # open camera with the given index
        self.cap = self._init_camera()
        self.running = asyncio.Event()
        self.out = None

    def _init_camera(self):
        cap = cv2.VideoCapture(self.camera_index)
        cap.set(cv2.CAP_PROP_FPS, self.target_fps)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open camera index {self.camera_index}")

        real_fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"[Camera] Index={self.camera_index}, requested {self.target_fps} fps → got {real_fps:.2f} fps")
        self.fps = real_fps if real_fps > 0 else self.target_fps
        return cap

    async def start_recording(self, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)

        # grab one frame for size
        ret, frame = await asyncio.to_thread(self.cap.read)
        if not ret:
            raise RuntimeError("Could not grab initial frame")

        h, w = frame.shape[:2]
        path = f"{output_folder}/{file_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter(path, fourcc, self.fps, (w, h))
        if not self.out.isOpened():
            raise RuntimeError(f"VideoWriter failed for {path} at {w}×{h}@{self.fps:.2f}fps")

        print(f"[Recorder] Writing → {path} ({w}×{h}@{self.fps:.2f}fps)")
        self.running.set()
        await asyncio.to_thread(self.out.write, frame)

        while self.running.is_set():
            ret, frame = await asyncio.to_thread(self.cap.read)
            if not ret:
                print("⛔ Failed to grab frame")
                break
            await asyncio.to_thread(self.out.write, frame)
            cv2.imshow("Recording", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running.clear()
                break

            await asyncio.sleep(0)

        # cleanup
        print("[Recorder] Finalizing...")
        self.out.release()
        self.out = None
        cv2.destroyAllWindows()
        print("[Recorder] Done.")

    async def stop_recording(self):
        if self.running.is_set():
            print("[Recorder] Stop requested")
            self.running.clear()
