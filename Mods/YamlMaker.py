import yaml
import os
import shutil
count=0
downsize_templates__dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Downsize_Template_Images"
predcit_items_list=[]

for filename in os.listdir(downsize_templates__dir):
        predcit_items_list.append(str(filename))
        count+=1
os.chdir("C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Mods")
yaml_data = {
    'path': r'C:/YOLO_Labelling+Training/YOLO_Labelling+Training',
    'train': r'C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images/train',
    'val': r'C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images/val',
    'nc': count,
    'names': predcit_items_list
}
yaml_file_path = 'yolo_config.yaml'

with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)
shutil.move("C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Mods/yolo_config.yaml","C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Data.yaml")

print(f"YAML file '{yaml_file_path}' has been created successfully.")