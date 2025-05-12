import asyncio
import os
import time
import cv2

class CameraHandler:
    def __init__(self, warmup=5.0):
        
        self.camera_index = 1 # Camera at index 1. (0 = built-in, 1 = First connected camera)
        self.target_fps = 60 # target fps to capture video at
        self.desired_res = (1920, 1080) # target resoltuion to capture video at
        self.warmup = warmup # Time to allow camera to auto focus/start up
        self.cap, self.fps, self.desired_res = self.initialize_camera()
        self.running = asyncio.Event()
        self.out = None
        
    def initialize_camera(self):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open camera index at {self.camera_index}")
        
        w_desired, h_desired = self.desired_res # Desired res = 1920x1080
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_desired)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_desired)
        
        cap.set(cv2.CAP_PROP_FPS, self.target_fps) # Set target_fps for recording
        
        # Check what the camera is actually recording at Resolution@fps
        w_actual = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_actual = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        real_fps = cap.get(cv2.CAP_PROP_FPS) or self.target_fps
        
        print(f"[Camera] index = {self.camera_index}, "
              f"Requested {w_desired}x{h_desired}@{self.target_fps}fps,"
              f"got {w_actual}x{h_actual}@{real_fps:.1f}fps")
        
        if (w_actual, h_actual) != (w_desired, h_desired):
            print("Camera ignored requested resolution.")
            
        print(f"[Camera] warming up for {self.warmup}s...")
        end_time = time.time() + self.warmup
        while time.time() < end_time:
            cap.read()
        print(f"[Camera] warmed up")
        
        return cap, real_fps, (w_actual, h_actual)
    
    async def start_recording(self, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)
        w, h = self.desired_res
        path = f"{output_folder}/{file_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter(path, fourcc, self.fps, (w, h))
        if not self.out.isOpened():
            raise RuntimeError(f"VideoWriter failed for {path}")
        print(f"[Recorder] Recording -> {path} ({w}x{h}@{self.fps:.1f}fps)")
        
        self.running.set()
        
        ret, frame = await asyncio.to_thread(self.cap.read)
        if ret:
            await asyncio.to_thread(self.out.write, frame)
        
        while self.running.is_set():
            ret, frame = await asyncio.to_thread(self.cap.read)
            if not ret:
                print("Failed to grab frame")
                break
            await asyncio.to_thread(self.out.write, frame)
            cv2.imshow("Video Output", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running.clear()
                break
            
            await asyncio.sleep(0)
            
        print("[Recorder] Finalizing...")
        self.out.release()
        self.out = None
        cv2.destroyAllWindows()
        print("[Recorder] Done.")
        
    async def stop_recording(self):
        if self.running.is_set():
            print("[Recorder] Stopping recording...")
            self.running.clear()