from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar import pyzbar
import cv2
import time


def draw_barcode(decoded, image):
    """draw a box around a given barcode in an image"""
    image = cv2.rectangle(
        image,
        (decoded.rect.left, decoded.rect.top),
        (
            decoded.rect.left + decoded.rect.width,
            decoded.rect.top + decoded.rect.height,
        ),
        color=(0, 255, 0),
        thickness=5,
    )
    return image


def decode(image):
    """decodes all barcodes from an image"""
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data)
        print()

    return image


def picam_setup():
    """Initialize the pi camera."""
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(cam, size=())
    time.sleep(0.1)
    return camera


if __name__ == "__main__":

    camera = picam_setup()
    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True
    ):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # show the frame
        cv2.imshow("Frame", image)

        # decode detected barcodes & get the image
        # that is drawn
        drawn_image, decoded_objects = decode(image)
        # show the image in the window
        cv2.imshow("Frame", drawn_image)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        if cv2.waitKey(1) == ord("q"):
            break
