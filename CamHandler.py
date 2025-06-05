import asyncio
import os
import cv2
import time

class CamHandler:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.camera_index = 1
        self.target_fps = 60
        self.warmup = 5
        self.running = asyncio.Event()
        self.out = None
        self.cap = None
        

    def initialize_camera(self):
        # Set which camera to use and what fps to record at
        cap = cv2.VideoCapture(self.camera_index)
        cap.set(cv2.CAP_PROP_FPS, self.target_fps)
        
        if not cap.isOpened():
            raise RuntimeError(f"Could not open camera index {self.camera_index}")
        
        # Warm up the camera so it focuses correctly
        print(f"[Camera] Warming up for {self.warmup}s")
        end_time = time.time() + self.warmup
        
        while time.time() < end_time:
            cap.read()
        
        print(f"[Camera] Warmed up")
        return cap
    
    async def start_recording(self, file_name):
        #Make directory for the file
        os.makedirs(self.output_folder, exist_ok=True)
        ret, frame = await asyncio.to_thread(self.cap.read)
        if not ret:
            raise RuntimeError("Could not grab initial frame")
        # get the resolution being recorded
        h, w = frame.shape[:2]
        # Set path for output
        path = f"{self.output_folder}/{file_name}.mp4"
        # Set video playback type
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter(path, fourcc, self.target_fps, (w, h))
        if not self.out.isOpened():
            raise RuntimeError(f"VideoWriter failed for {path} at {w}x{h}@{self.target_fps:.2f}fps")
        
        print(f"[Recorder] Writing -> {path} ({w}x{h}@{self.target_fps:.2f}fps)")
        self.running.set()
        await asyncio.to_thread(self.out.write, frame)
        
        # Capture frames
        while self.running.is_set():
            ret, frame = await asyncio.to_thread(self.cap.read)
            if not ret:
                print("Failed to grab frame")
                break
            await asyncio.to_thread(self.out.write, frame)
            cv2.imshow("Capture", frame)
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
            print("Recorder Stop requested")
            self.running.clear()
            
    async def warm_up(self):
        self.cap = await asyncio.to_thread(self.initialize_camera)