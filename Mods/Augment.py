import numpy as np
import cv2
import os
import random
import shutil
from PIL import Image

"""
0 Brightness
1 Blur
2 Flip
3 Rotate
4 RGB shift
"""

def random_brightness(image, max_brightness):
    if max_brightness !=0:
        delta = random.randint(-max_brightness, max_brightness)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v.astype(int) + delta, 0, 255).astype(np.uint8)
        hsv = cv2.merge((h, s, v))
        adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted_image

def random_gaussian_blur(image, max_blur):
    if max_blur!=0:
        kernel_size = random.randint(1, max_blur) * 2 + 1
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred_image

def flip(image):
    flip_type = random.randint(-1, 1)
    flipped_image = cv2.flip(image, flip_type)
    return flipped_image

def rotate(image):
    deg = random.randint(0, 360)
    rotated_image = image.rotate(deg, expand=True)
    return rotated_image

def rgb_shift(image, r_threshold, g_threshold, b_threshold):
    r, g, b = image.split()
    r_shift = random.randint(-r_threshold, r_threshold)
    g_shift = random.randint(-g_threshold, g_threshold)
    b_shift = random.randint(-b_threshold, b_threshold)
    r = r.point(lambda i: i + r_shift)
    g = g.point(lambda i: i + g_shift)
    b = b.point(lambda i: i + b_shift)
    shifted_image = Image.merge("RGB", (r, g, b))
    return shifted_image

def augment(image_folder_path, augment_image_folder_path, max_brightness, max_blur, r_threshold, g_threshold, b_threshold, num):
    k=input("Does your image want to flip?(Y/N) : ")
    j=input("Does your image want to rotate?(Y/N) : ")
    for i in range(num):
        for filename in os.listdir(image_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                print("Augmenting " + str(filename))
                image_path = os.path.join(image_folder_path, filename)
                file_name, file_ext = os.path.splitext(filename)
                
                # Load image using OpenCV
                image = cv2.imread(image_path)
                if image is None:
                    continue

                # Apply augmentations
                image = random_brightness(image, max_brightness)
                image = random_gaussian_blur(image, max_blur)
                if k=="y":
                    image = flip(image)

                # Convert to PIL Image for other augmentations
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if j=="y":
                    image = rotate(image)
                image = rgb_shift(image, r_threshold, g_threshold, b_threshold)

                # Convert back to OpenCV format for saving
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Save the augmented image
                new_filename = f"{file_name}_{str(i)}{file_ext}"
                save_path = os.path.join(augment_image_folder_path, new_filename)
                cv2.imwrite(save_path, image)
    print("Augmentation process has completed.")   