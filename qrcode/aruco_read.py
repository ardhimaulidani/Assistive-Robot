# Aruco Detection Python Class
# By Ardhika Maulidani

import argparse
import imutils
import time
import sys
import cv2
from camera import camera

class aruco(object):
	def __init__(self, device):
		self.device = device
		self.cap = camera(self.device)

		self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
		self.parameters =  cv2.aruco.DetectorParameters()
		self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

	def capture (self):
		while self.cap.is_opened():
			# get frame from camera
			self.frame = self.cap.capture()
			
			# detect ArUco markers in the input frame
			(corners, ids, rejected) = self.detector.detectMarkers(self.frame)

			# verify at least one ArUco marker detected in frame
			if len(corners) > 0:
				# flatten the ArUco IDs list
				ids = ids.flatten()

				# loop over the detected ArUCo corners
				for (markerCorner, markerID) in zip(corners, ids):
					corners = markerCorner.reshape((4, 2))
					(topLeft, topRight, bottomRight, bottomLeft) = corners

					# convert each of the (x, y)-coordinate pairs to integers
					topRight = (int(topRight[0]), int(topRight[1]))
					bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
					bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
					topLeft = (int(topLeft[0]), int(topLeft[1]))

					# draw the bounding box of the ArUCo detection
					cv2.line(self.frame, topLeft, topRight, (0, 255, 0), 2)
					cv2.line(self.frame, topRight, bottomRight, (0, 255, 0), 2)
					cv2.line(self.frame, bottomRight, bottomLeft, (0, 255, 0), 2)
					cv2.line(self.frame, bottomLeft, topLeft, (0, 255, 0), 2)

					# compute and draw the center (x, y)-coordinates of the
					# ArUco marker
					cX = int((topLeft[0] + bottomRight[0]) / 2.0)
					cY = int((topLeft[1] + bottomRight[1]) / 2.0)
					cv2.circle(self.frame, (cX, cY), 4, (0, 0, 255), -1)

					# draw the ArUco marker ID on the frame
					cv2.putText(self.frame, str(markerID),
						(topLeft[0], topLeft[1] - 15),
						cv2.FONT_HERSHEY_SIMPLEX,
						0.5, (0, 255, 0), 2)			
			
			cv2.imshow("DEBUG", self.frame)
			key = cv2.waitKey(1) & 0xFF			
			if key == ord("q"):
					break
		cv2.destroyAllWindows()
		self.cap.close()

if __name__ == "__main__":
	vision = aruco(0)
	vision.capture()