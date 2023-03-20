# Camera Python Class
# By Ardhika Maulidani
'''
    Usage :
    This is Camera Python Class for handling physical camera on mobile robot
    <> Operation
        - is_opened() : Verify if camera can be opened (Return -> bool)
        - capture() : Get frame from camera (Return -> mat:frame)
        - close() : Close used camera resources
        - get_resolution() : Get currently used camera resolution value (Return -> int:widht,int:height)
        - set_resolution(Param -> int:width, int:height) : Change camera resolution value
        - get_fps() : Get currently used camera frame rate value (Return -> enum:fps)
        - set_fps() (Param -> enum:fps): Change camera frame rate value
        - set_fov(Param -> float:h_fov. float:v_fov): Change camera FOV value
'''

import cv2 as cv

class camera(object):

    def __init__(self, device, fps=24, width=640, height=480):
        self.device = device
        self.camera = cv.VideoCapture(self.device)
        self.set_resolution(width, height)
        self.set_fps(fps)

    def is_opened(self):
        if self.camera and self.camera.isOpened() :
            return True
        return False

    def capture(self):
        if not self.is_opened():
            return
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame

    def close(self):
        if not self.is_opened():
            return
        else:	
            self.camera.release()

    def get_resolution(self):
        width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def set_resolution(self, width, height):
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    def get_fps(self):
        return self.camera.get(cv.CAP_PROP_FPS)

    def set_fps(self, fps):
        self.camera.set(cv.CAP_PROP_FPS, fps)

    def set_fov(self,h_fov,v_fov):
        self.h_fov  = h_fov
        self.v_fov  = v_fov

if __name__ == "__main__":
    cap = camera(0)
    while True:
        frame = cap.capture()

        cv.imshow("DEBUG", frame)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break

    cv.destroyAllWindows()
    self.camera.close()