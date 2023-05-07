import cv2
import threading


class CameraThread(threading.Thread):
    def __init__(self, camera_id, func):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.func = func
        self.running = False

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.camera_id)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Обработка кадра
                pass
        cap.release()

    def stop(self):
        self.running = False


camera_thread = CameraThread(0, ...)
camera_thread.start()
