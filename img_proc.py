import cv2
import picamera
import numpy as np
import time
import datetime

# Red has two color ranges
LOW_COLOR1 = np.array([0, 100, 100])
HIGH_COLOR1 = np.array([10, 255, 255])
LOW_COLOR2 = np.array([170, 100, 100])
HIGH_COLOR2 = np.array([180, 255, 255])
"""
Hue : Tint. Red is 0 degrees and changes in order of rainbow colors up to 360 degrees.
Saturation : Vividness of color. 100% is a pure color and the lower the color, the whiter it gets.
Value Brightness : Brightness of color. 100% is a pure color and the lower the color, the darker it gets.

H : 0-360[degrees] => 0-180
S : 0-100[%]       => 0-255
V : 0-100[%]       => 0-255

Mutual conversion between RGB and HSV
https://www.petitmonte.com/javascript/rgb_hsv_convert.html
"""

def take_picture():
    now = datetime.datetime.now()
    img_name = 'img/' + now.strftime('%Y%m%d_%H%M%S') + '_img.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(1.5)
        camera.capture(img_name)
    return img_name

def detect_cone(img_name):
    img = cv2.imread(img_name)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    H, W, C = img.shape
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    # Apply blur filter
    img_blur = cv2.blur(img, (15, 15))
    # BGR => HSV
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
    # Specify the range of HSV and binarize
    bin_img1 = cv2.inRange(hsv, LOW_COLOR1, HIGH_COLOR1)
    bin_img2 = cv2.inRange(hsv, LOW_COLOR2, HIGH_COLOR2)
    # Apply a mask to the original image -> Only the color of the masked part remains
    mask = bin_img1 + bin_img2
    masked_img = cv2.bitwise_and(img_blur, img_blur, mask= mask)
    out_img = masked_img
    # Labeling
    num_labels, label_img, stats, center = cv2.connectedComponentsWithStats(mask)
    # Remove the black-filled background color of the largest label
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0) # Arrays with label information
    center = np.delete(center, 0, 0)
    
    if num_labels >= 1:
        # Get index of maximum area
        max_index = np.argmax(stats[:, 4])
        x = stats[max_index][0]
        y = stats[max_index][1]
        w = stats[max_index][2]
        h = stats[max_index][3]
        s = stats[max_index][4]
        p = s / (H * W) # Percentage of cone in image
        mx = int(center[max_index][0])
        my = int(center[max_index][1])
        # Draw a bounding box around the label
        cv2.rectangle(out_img, (x, y), (x+w, y+h), (255, 0, 255))
        # Display center and area
        cv2.putText(out_img, "%d,%d"%(mx, my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
        cv2.putText(out_img, "%d"%(s), (x, y+h+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
        now = datetime.datetime.now()
        img_name = 'proc_img/' + now.strftime('%Y%m%d_%H%M%S') + '_proc_img.jpg'
        cv2.imwrite(img_name, out_img)
        if mx > W / 3 * 2:
            print("Right")
            return "Right", img_name, p
        elif mx < W / 3:
            print("Left")
            return "Left", img_name, p
        else:
            print("Front")
            return "Front", img_name, p
    else:
        now = datetime.datetime.now()
        img_name = 'proc_img/' + now.strftime('%Y%m%d_%H%M%S') + '_proc_img.jpg'
        cv2.imwrite(img_name, out_img)
        print("Not Found")
        return "Not Found", img_name, 0


if __name__ == '__main__':
    img_name = take_picture()
    cone_location, out_img, p = detect_cone(img_name)
    print(p)
