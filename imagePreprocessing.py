# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# This is a sample Python script.
import cv2
import numpy as np


def colourThreshold(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # The bitwise and of the frame and mask is done so
    # that only the blue coloured objects are highlighted
    # and stored in res
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res


def thresholdOverlay(mask, frame):
    oppMask = cv2.bitwise_not(mask)
    overlay = cv2.bitwise_and(frame, oppMask)
    return overlay


def backgroundSubtraction(img):
    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                        param2=30, minRadius=200, maxRadius=300)

    height = img.shape[0]
    width = img.shape[1]
    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            centerX, centerY, radius = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            circularMask = np.zeros_like(img)
            circularMask = cv2.circle(circularMask, (centerX, centerY), radius, (255, 255, 255), -1)

            result = cv2.bitwise_and(img, circularMask)
            return result


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cap = cv2.VideoCapture("data/input.gif")
    ret, image = cap.read()
    cap.release()
    if ret:
        imageWithoutBackground = backgroundSubtraction(image)
        cv2.imshow("imageWithoutBackground", imageWithoutBackground)
        imageColourThreshold = colourThreshold(imageWithoutBackground)
        cv2.imshow("imageColourThreshold", imageColourThreshold)
        imageMaskOverlay = thresholdOverlay(imageColourThreshold, image)
        cv2.imshow("imageMaskOverlay", imageMaskOverlay)
        cv2.imwrite("data/ImageOverlayOutput.png", imageMaskOverlay)

        cv2.waitKey(0)