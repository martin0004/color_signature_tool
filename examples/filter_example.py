import cv2
import matplotlib.pyplot as plt
import numpy as np

# BGR and HSV images
bgr = cv2.imread("../images/duckies_and_tomatoes.jpg")
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
# Matplotlib needs RGB image
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

h_min = 15
h_max = 35
s_min = 65
s_max = 180
v_min = 210
v_max = 255

lower = np.array([h_min, s_min, v_min])
upper = np.array([h_max, s_max, v_max])

mask = cv2.inRange(hsv, lower, upper)

rgb_masked = np.copy(rgb)
rgb_masked[mask == 0] = [0,0,0]

plt.imshow(rgb_masked)
plt.show()
