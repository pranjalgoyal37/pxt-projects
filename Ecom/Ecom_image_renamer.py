import os
import openpyxl as op
import pandas as pd
excel_path=r"D:\Amazon Associates twitter\Ecom_ss.xlsx"
root_path=r"D:\Ecom_screenshots"

excel_img_name=[]
folder_img_name=[]

def read_data():
    global excel_img_name
    row=2
    # wb=op.load_workbook(excel_path)
    # sh1=wb['Sheet1']


    df =pd.read_excel(excel_path)
    excel_img_name=list(df['name'])
read_data()

print(f"Total Number of images  is {len(excel_img_name)} in given exel file.")
print(f"Total no of folder is:{len(os.listdir(root_path))}")

def img_rename():
    img_no=0
    for sub_folder in (os.scandir(root_path)):
        sub_folder_path=os.path.join(root_path,sub_folder)
        
        j=1
      
        for files in os.listdir(sub_folder_path):

            # global img_no
            my_dest=sub_folder_path+"//"+str(excel_img_name[img_no])+".jpg"
            my_source  = os.path.join(root_path,sub_folder,files)
            img_no+=1

            os.rename(my_source,my_dest)
            j+=1
            print(files)    

img_rename()