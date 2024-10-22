import customtkinter 
from tkinter import messagebox
from tkinter  import *
from tkcalendar import DateEntry
import pandas as pd
import requests
import os

ss_source=[]
ss_description=[]
missing_source=[]
video_ids = []

# GUI Design
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root =customtkinter.CTk()
root.geometry('1000x700+300+30')
root.resizable(False, False)
root.title("Videos Status By Pranjal Goyal")
root.attributes('-alpha',0.85)

root_dir = r"C:\video_status"
brand_list=['youtube','Facebook']
category_list=['Video_unavailable','Keywords']

brand=StringVar()
info=StringVar()
category=StringVar()
brand.set(brand_list[0])
category.set(category_list[0])
missing_video_id=[]
# api_key = 'AIzaSyB8MhhbMmXKaydWXDtvdvPC2F8vt3pOvF0'
f_path = r"C:\yt_pranjal_scrapper"
output_sheet=r"C:\yt_pranjal_scrapper\yt_output.xlsx"
def get_video_status():
    data = []
    v_id=[]
    result=[]
  
    missing_data=[]
    print(video_ids)
    chunks = [video_ids[i:i + 50] for i in range(0, len(video_ids), 50)]
    for chunk in chunks:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={','.join(chunk)}&key={api_key}")
        if response.status_code == 200:
            video_data = response.json()
            print(video_data)
            for item in video_data['items']:
                channel_id = item['snippet']['channelId']
                channel_name = item['snippet']['channelTitle']
                v_id.append(item['id'])
                v_url="www.youtube.com/video/"+item['id']
                data.append([v_url, channel_id, channel_name])

            result=(list(set(chunk) -set(v_id)))
            for i in result:
                missing_video_id.append("www.youtube.com/video/"+i)
                missing_data.append(["www.youtube.com/video/"+i,'video unavailable'])
                
            res=unique_values(data)
         
            df1= pd.DataFrame(data, columns=['v_url', 'channel_id', 'channel_name'])
            df2=pd.DataFrame(missing_data,columns=['v_url','status'])
                 
           
    with pd.ExcelWriter(output_sheet) as writer:
        df1.to_excel(writer, index=False, sheet_name='Channel_data')
        df2.to_excel(writer ,index=False,sheet_name='video_unavailable')
      


def unique_values(lst):
    unique_values = []
    for sublist in lst:
        if sublist not in unique_values:
            unique_values.append(sublist)
    return [value for value in unique_values]


def get_data():
    global api_key,missing_source 
    missing_source = []
    missing_text.delete("1.0", "end")

    source_urls=source_text.get("1.0", "end-1c").split("\n") 
    for url in source_urls:
            if("video/" in url ):       
                video_ids.append(url.split("video/")[1]) 
    
    api_key=txt_API.get()
    brand_name =brand.get()
    category_name=category.get()

    
    if len(source_urls) == 0:
        messagebox.askokcancel("source url is  blank !!"," the source url !!")
    else:
        res= messagebox.askokcancel("Confirmation",f"Do you want to continue with {len(source_urls)} videos")

        if res==True:
            if not os.path.exists(f_path):
                os.mkdir(f_path)
            try:
                get_video_status()
            except Exception as e:
                 print(e)
            finally:
                info_lbl.configure(text=f" available videos are :{len(source_urls)-len(missing_video_id)}")
                missing_lbl.configure(text=f"Total unavailable videos are : {len(missing_video_id)}")
                missing_text.insert(END, "\n".join(missing_video_id))
                

title=customtkinter.CTkLabel(master=root,text="Video Status", font=("Georgia",25,"italic","bold"))
title.pack(padx=40,pady=(10,5))

frame=customtkinter.CTkFrame(master=root,width=600,height=200)
frame.pack(padx=20,fill='both',expand=True)


source_lbl=customtkinter.CTkLabel(master=frame,text="Source URL's",font=(" Verdana",18,"bold"))
source_lbl.place(x=600,y=20)

source_text=customtkinter.CTkTextbox(master=frame,width=540,height=230,font=customtkinter.CTkFont('Verdana',18))
source_text.place(x=420,y=68)

name_det_lbl=customtkinter.CTkLabel(master=frame,text="Naming Details",font=(" Verdana",18,"bold"))
name_det_lbl.place(x=180,y=20)


lbl_bName=customtkinter.CTkLabel(frame,text=" Brand Name ",font=customtkinter.CTkFont('san-serif',20))
lbl_bName.place(x=40,y=80)

lbl_API_key=customtkinter.CTkLabel(frame,text=" API_key",font=customtkinter.CTkFont('Verdana',20))
lbl_API_key.place(x=40,y=130)

lbl_category=customtkinter.CTkLabel(frame,text=" Category ",font=customtkinter.CTkFont('Verdana',20))
lbl_category.place(x=40,y=190)                      


brand_Opt=customtkinter.CTkOptionMenu(frame,width=160,font=customtkinter.CTkFont('Verdana',15),values=brand_list,variable=brand)
brand_Opt.place(x=220,y=80)

txt_API=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',15))
txt_API.place(x=220,y=130)
txt_API.insert(END,'AIzaSyB8MhhbMmXKaydWXDtvdvPC2F8vt3pOvF0')

category_Opt=customtkinter.CTkOptionMenu(frame,width=120,font=customtkinter.CTkFont('Verdana',14),values=category_list,variable=category)
category_Opt.place(x=220,y=190)

btn=customtkinter.CTkButton(frame,text="Submit",width=350,height=40,font=customtkinter.CTkFont('Verdana',25),command=get_data)
btn.place(x=40,y=250)


title=customtkinter.CTkLabel(master=root,text=" Info Details", font=(" Verdana",24,"bold","italic"))
title.pack(padx=40,pady=(10,5))

frame_02=customtkinter.CTkFrame(root,width=100 ,height=150)
frame_02.pack(padx=20,pady=10,fill='both',expand=True)

source_lbl=customtkinter.CTkLabel(master=frame_02,text="Unavailable Source URL's",font=(" Verdana",18,"bold"))
source_lbl.place(x=620,y=20)


info_lbl=customtkinter.CTkLabel(frame_02,text="Total length of source : ",font=customtkinter.CTkFont('Verdana',17))
info_lbl.place(x=20,y=60)

missing_text=customtkinter.CTkTextbox(frame_02,width=550,font=customtkinter.CTkFont('Verdana',17))
missing_text.place(x=400,y=50)

missing_lbl=customtkinter.CTkLabel(frame_02,text="Total Missing  source url's is : ",font=customtkinter.CTkFont('Verdana',17))
missing_lbl.place(x=20,y=100)


root.mainloop()