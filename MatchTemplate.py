#import required modules
import mtm
from mtm import matchTemplates
import cv2
import shutil
import os
import sys
import numpy as np
from Mods import Downsize
import PIL
from PIL import Image
from Mods import XYWH
from Mods import Augment
import pandas as pd
from Mods import Move
original_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Original_Images"
downsize_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Downsize_Images"
augmented_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Augmented_Images"
templates_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Template_Images"
downsize_templates__dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Downsize_Template_Images"
processed_labels_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Processed/labels"
processed_images_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Processed/images"
training_data_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images"
training_label_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/labels"
val_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images/val"
train_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images/train"
test_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/images/test"
label_val_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/labels/val"
label_train_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/labels/train"
label_test_dir=r"C:/YOLO_Labelling+Training/YOLO_Labelling+Training/Training_Data/labels/test"
count_augmented=0
templates_dir_list=[]
listTemplate=[]


count=0
def CheckEmpty(Path):
    if len(os.listdir(Path))==0:
        return True
    else:
        return False
def MatchTemplates(Image_path):
    Cnt=0
    BigLIST=[]
    nohitlist=[]
    LIST=[]
    for filename in os.listdir(Image_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print("Processing " + str(filename)) 
            img_path=os.path.join(Image_path,filename)
            img=cv2.imread(img_path)
            image_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            listHits=matchTemplates(listTemplate,image_rgb,score_threshold=0.5,method=cv2.TM_CCOEFF_NORMED,maxOverlap=0)
            img=PIL.Image.open(img_path)
            wid,hgt=img.size
            TempLIST=[]
            BT=[]
            if len(listHits)!=0:
                for hits in listHits:
                    if Cnt==len(listHits):
                        break
                    X=listHits[Cnt][1][0]
                    Y=listHits[Cnt][1][1]
                    W=listHits[Cnt][1][2]
                    H=listHits[Cnt][1][3]
                    TempLIST.append(X)
                    TempLIST.append(Y)
                    TempLIST.append(W)
                    TempLIST.append(H)
                    cv2.rectangle(image_rgb,(X,Y),(X+W,Y+H),(0,0,255),3)
                    cv2.imwrite(os.path.join(processed_images_dir,filename),image_rgb)
                    XYWH.Convert(TempLIST,wid,hgt)
                    LIST.append(str(templates_dir_list.index(listHits[Cnt][0]))+" "+str(TempLIST[0])+" "+str(TempLIST[1])+" "+str(TempLIST[2])+" "+str(TempLIST[3]))
                    Cnt+=1
                    TempLIST=[]
                    BigLIST.append(LIST)
                    LIST=[]
                    os.chdir(processed_labels_dir)
                    OUTPUT=str(filename).replace(".jpg",".txt") 
                with open(OUTPUT,'w') as f:
                    for line in BigLIST :
                        f.write(str(line[0]))
                        f.write("\n") 
                    BigLIST=[]
                Cnt=0
            if len(listHits)==0:
                nohitlist.append(filename)
    if len(nohitlist) != 0 :
        print(nohitlist)
        re=input("These images have no hits. Do you want to recrop it? or do you want to continue(Y for continue, N for exit)")
        if re.lower()=='n':
            sys.exit()

if CheckEmpty(original_dir)==True:
    print("Your Original Images are not in the Original_Images folder")
    sys.exit()
if CheckEmpty(templates_dir)==True:
    print("Your Template Images are not in the Templates_Images folder")
    sys.exit()

tmpdwsz=input("Do you Want to Downsize your image(downsizing image would increase speed drastically)(y/n)").lower()

if tmpdwsz=="y":
    tmp=input("Please Enter Your Downsize Scale : ")
    print("Image Downsizing......")
    Downsize.downsize(original_dir,downsize_dir,int(tmp))
    Downsize.downsize(templates_dir,downsize_templates__dir,int(tmp))
    print("Image Downsizing has been completed") 

#process template
#**************************************************************************************************


if tmpdwsz == "y":
    for filename in os.listdir(downsize_templates__dir):
        templates_dir_list.append(str(filename))
        template_img=cv2.imread(os.path.join(downsize_templates__dir,filename))
        template_rgb=cv2.cvtColor(template_img,cv2.COLOR_BGR2RGB)
        Tmp = (filename,template_rgb)
        listTemplate.append(Tmp)
    MatchTemplates(downsize_dir)
else:
    for filename in os.listdir(templates_dir):
        templates_dir_list.append(str(filename))
        template_img=cv2.imread(os.path.join(templates_dir,filename))
        template_rgb=cv2.cvtColor(template_img,cv2.COLOR_BGR2RGB)
        Tmp = (filename,template_rgb)
        listTemplate.append(Tmp)
    MatchTemplates(original_dir)
#***************************************************************************************************

ipt=input("Do you want to augment your images. (Y/N) : ")
if ipt.lower() == "y" and tmpdwsz=="y":
    intipt=input("How many times do you want to augment? : ")
    max_brightness=int(input("Please enter you delta max brightness : "))
    max_blur=int(input("Please enter you delta max blur : "))
    r_threshold=int(input("Please enter you r_threshold : "))
    g_threshold=int(input("Please enter you g_threshold : "))
    b_threshold=int(input("Please enter you b_threshold : "))
    Augment.augment(downsize_dir,augmented_dir,max_brightness,max_blur,r_threshold,g_threshold,b_threshold,int(intipt))
    print("Continure Matching Template......")
    MatchTemplates(augmented_dir)
    print("Please check processed folder to check the results.")
    train=input("what percent of data would you like to train? :")
    val=input("What percent of data would you like to validate? :")
    print("The rest " + str(100-int(train)-int(val))+" percent of data would be stored for futher testing")
    print("Moving labels and files to Training Data")
    Move.random_move(augmented_dir,processed_labels_dir,train_dir,val_dir,test_dir,label_train_dir,label_val_dir,label_test_dir,int(train),int(val),100-int(train)-int(val))
elif ipt.lower() == "y" and tmpdwsz=="n":
    intipt=input("How many times do you want to augment? : ")
    max_brightness=int(input("Please enter you delta max brightness : "))
    max_blur=int(input("Please enter you delta max blur : "))
    r_threshold=int(input("Please enter you r_threshold : "))
    g_threshold=int(input("Please enter you g_threshold : "))
    b_threshold=int(input("Please enter you b_threshold : "))
    Augment.augment(original_dir,augmented_dir,max_brightness,max_blur,r_threshold,g_threshold,b_threshold,int(intipt))
    print("Continure Matching Template......")
    MatchTemplates(original_dir)
    print("Please check processed folder to check the results.")
    train=input("what percent of data would you like to train? :")
    val=input("What percent of data would you like to validate? :")
    print("The rest " + str(100-int(train)-int(val))+" percent of data would be stored for futher testing")
    print("Moving labels and files to Training Data")
    Move.random_move(augmented_dir,processed_labels_dir,train_dir,val_dir,test_dir,label_train_dir,label_val_dir,label_test_dir,int(train),int(val),100-int(train)-int(val))
    
else:
    print("Please check processed folder to check the results.")
    print("Moving labels and files to Training Data")
    train=input("what percent of data would you like to train? :")
    val=input("What percent of data would you like to validate? :")
    print("The rest " + str(100-int(train)-int(val))+" percent of data would be stored for futher testing")
    print("Moving labels and files to Training Data")
    Move.random_move(original_dir,processed_images_dir,train_dir,val_dir,test_dir,label_train_dir,label_val_dir,label_test_dir,int(train),int(val),100-int(train)-int(val))
