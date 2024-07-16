downsize_dir=r"D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training/Downsize_Images"
augmented_dir=r"D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training/Augmented_Images"
downsize_templates__dir=r"D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training/Downsize_Template_Images"
processed_labels_dir=r"D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training/Processed/labels"
processed_images_dir=r"D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training/Processed/images"
Root_dir=r'D:/Max/YOLO_Labelling+Training/YOLO_Labelling+Training'
import os
for src_dir in [downsize_dir, augmented_dir,
                downsize_templates__dir,processed_images_dir,processed_labels_dir]:
    src_dir_name = os.path.basename(src_dir)
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        os.remove(src_item)
print("All files Dumped!")