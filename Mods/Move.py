import os
import shutil
import random
from pathlib import Path
def move(folder,destination_path):
    for filename in os.listdir(folder):
            augmented_path = os.path.join(folder,filename)
            destination_path=os.path.join(destination_path, filename)
            shutil.move(augmented_path, destination_path)

def random_move(image_folder, text_folder, des_image_path1, des_image_path2, des_image_path3, des_text_path1, des_text_path2, des_text_path3, per1, per2, per3):
    image_folder = Path(image_folder)
    text_folder = Path(text_folder)
    des_image_path1 = Path(des_image_path1)
    des_image_path2 = Path(des_image_path2)
    des_image_path3 = Path(des_image_path3)
    des_text_path1 = Path(des_text_path1)
    des_text_path2 = Path(des_text_path2)
    des_text_path3 = Path(des_text_path3)
    
    # Convert percentage strings to integers
    per1 = int(per1)
    per2 = int(per2)
    per3 = int(per3)
    
    image_paths = list(image_folder.glob('*'))  # Adjust the glob pattern to match your image file extension
    random.shuffle(image_paths)
    total_images = len(image_paths)
    num_images1 = int(total_images * (per1 / 100))
    num_images2 = int(total_images * (per2 / 100))
    num_images3 = total_images - num_images1 - num_images2
    
    for image_path in image_paths[:num_images1]:
        move_files(image_path, text_folder, des_image_path1, des_text_path1)
    for image_path in image_paths[num_images1:num_images1 + num_images2]:
        move_files(image_path, text_folder, des_image_path2, des_text_path2)
    for image_path in image_paths[num_images1 + num_images2:num_images1 + num_images2 + num_images3]:
        move_files(image_path, text_folder, des_image_path3, des_text_path3)

def move_files(image_path, text_folder, des_image_folder, des_text_folder):
    des_image_folder.mkdir(parents=True, exist_ok=True)
    des_text_folder.mkdir(parents=True, exist_ok=True)
    shutil.move(str(image_path), str(des_image_folder / image_path.name))
    
    text_path = text_folder / image_path.with_suffix('.txt').name
    if text_path.exists():
        shutil.move(str(text_path), str(des_text_folder / text_path.name))



