# Aruco Detection Python Class
# By Ardhika Maulidani

import cv2
from camera import camera

class aruco(object):
	def __init__(self, device):
		# Init Camera
		self.device = device
		self.cap = camera(self.device, 24, 320, 240)

		# Init FPS Variable
		self.prev_time = 0
		self.curr_time = 0

		# Init ArUco Parameter
		self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
		self.parameters =  cv2.aruco.DetectorParameters()
		self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

	def capture(self):
		# Get Camera Frame
		self.frame = self.cap.capture()

		# Detect ArUco Markers in the Input Frame
		(corners, ids, rejected) = self.detector.detectMarkers(self.frame)

		# Verify at Least One ArUco Marker Detected
		if len(corners) > 0:
			# Flatten the ArUco IDs List
			ids = ids.flatten()

			# Loop Over the Detected ArUCo Corners
			for (markerCorner, markerID) in zip(corners, ids):
				corners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = corners

				# Convert (x, y)-Coordinate Pairs to Integers
				topRight = (int(topRight[0]), int(topRight[1]))
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				# Draw the Bounding Box of the ArUCo Detection
				cv2.line(self.frame, topLeft, topRight, (0, 255, 0), 2)
				cv2.line(self.frame, topRight, bottomRight, (0, 255, 0), 2)
				cv2.line(self.frame, bottomRight, bottomLeft, (0, 255, 0), 2)
				cv2.line(self.frame, bottomLeft, topLeft, (0, 255, 0), 2)

				# Compute and Draw the Center (x, y)-Coordinates of the ArUco Marker
				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				cv2.circle(self.frame, (cX, cY), 4, (0, 0, 255), -1)

				# Draw the ArUco Marker ID on the Frame
				cv2.putText(self.frame, str(markerID),
					(topLeft[0], topLeft[1] - 15),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.5, (0, 255, 0), 2)			

		# # Get FPS
		# self.curr_time = time.time()
		# fps = 1/(self.curr_time-self.prev_time)
		# self.prev_time = self.curr_time
		# print(fps)
		
		return(self.frame, ids)
	
	def destructor(self):
		self.cap.close()
		cv2.destroyAllWindows()
