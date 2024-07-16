"""
----------
Date:2024/7/8
Goal:Integrate Code
Now:Writing Modules
----------
"""
import os
import PIL
from PIL import Image,ExifTags

def correct_orientation(image):
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = image._getexif()
    if exif is not None:
        orientation = exif.get(orientation)
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)
    return image

def downsize(path,path2,downsize_scale):
    try:
        for filename in os.listdir(path):
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') :
                filename_path=os.path.join(path,filename)
                destination_path=os.path.join(path2,filename)
                img=PIL.Image.open(filename_path)
                wid,hgt=img.size
                with Image.open(filename_path) as image:
                    image=correct_orientation(image)
                    resized_img=image.resize((int(wid/downsize_scale),int(hgt/downsize_scale)))
                    resized_img.save(destination_path)
    except IndexError:
        pass

