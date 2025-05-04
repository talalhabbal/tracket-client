import cv2
import asyncio

class CamHandler():
    def __init__(self):
        self.fps=60
        self.resolution=(1920,1080)
        self.cap=self.init_camera()
        self.running=asyncio.Event()
        self.out=None


    def init_camera(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        if not cap.isOpened():
            raise Exception("Could not open camera")
        return cap

    async def start_recording(self,output_folder,file_name):
        print("Camera Recording")
        self.running.set()

        self.out = cv2.VideoWriter(
            f'{output_folder}/{file_name}.avi',
            cv2.VideoWriter_fourcc(*'XVID'),
            self.fps,
            self.resolution
        )

        while self.running.is_set():
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            self.out.write(frame)
            cv2.imshow('Recording', frame)

            await asyncio.sleep(0)

    async def stop_recording(self):
        print('Stop Camera Recording')
        
        self.running.clear()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()
            