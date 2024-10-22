from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import customtkinter 
from tkinter import messagebox
from tkinter  import *
from tkcalendar import DateEntry

from PIL import Image
import time
import os
import random
import pyautogui as py


source_urls=[]
text ='Your screenshots are saved in "Instagram_Screenshot_RoboPG," which is on the C drive.'
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root =customtkinter.CTk()
root.geometry('1000x600+300+30')
root.resizable(False, False)
root.title("Screenshot Taker")
root.attributes('-alpha',0.95)

date=datetime.now()
c_date = date.strftime('_%d%m%y.jpg')
brand_list=['Instagram','Twitter','Facebook','LinkedIn','Youtube','Other']
brand=StringVar()
brand.set(brand_list[0])
saved ="Your screenshots are saved in 'Instagram_Screenshot_RoboPG folder ' which is on the C drive."
root_dir = r"C:\Instagram_Screenshot_RoboPG"
ss_path = os.path.join(root_dir,date.strftime('%d-%m-%Y'))
#  take screenshot code 

def create_root_dir():

    os.chdir('C:/')
    if not os.path.exists('Instagram_Screenshot_RoboPG'):
        os.mkdir('C:/'+'Instagram_Screenshot_RoboPG')
    os.chdir(root_dir)

def instagram_login(driver,source_urls,username,password):
    
    driver.get("https://www.instagram.com/accounts/login")
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(username)
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    # time.sleep(1)
    # driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button').click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x1r3wxaz')))
        take_ss(driver,source_urls)

    except:
        print("Exceptopn")
        take_ss(driver,source_urls)

def twitter_login(driver,source_urls,username,password):
    print("you are in twitter login function")
    driver.get("https://twitter.com/login")
    # username = "nine_param49754"
    # password = 'Pixel@1722'
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def facebook_login(driver ,source_urls,username,password):
    driver.get("https://www.facebook.com/login/")
    
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    username_field.send_keys(username)


    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pass")))
    password_field.send_keys(password)
    time.sleep(2)
    driver.find_element(By.NAME ,"login").click()
    time.sleep(timer)
    take_ss(driver,source_urls)

def take_ss(driver,source_urls):
    # instagram_login(driver,username,password)
    for no,source in enumerate (source_urls,s_no):

        driver.get(source)
        
        # wait=WebDriverWait(driver,4).until(EC.visibility_of_element_located((By.XPATH,instaLoadXPath)))
        
        time.sleep(timer)
        s_ss = py.screenshot()
        
        s_ss.save(os.path.join(r'C:\Instagram_Screenshot_RoboPG', 'source.jpg'))
        crop_image(no)
    

def crop_image(no):
    
    img = Image.open(r'C:\Instagram_Screenshot_RoboPG\source.jpg').convert('RGB')
    img_size = img.size
    ss_name=""
    if(no<=9):
        ss_name = os.path.join(ss_path,f'{fSSName}_0{no}{lSSName}')

    else:
        ss_name = os.path.join(ss_path,f'{fSSName}_{no}{lSSName}')

    if img_size[1] in range(900,1100):
        img = img.crop((0, 42,img_size[0],img_size[1]-65))
    else:
        img = img.crop((0, 32,img_size[0],img_size[1]-55))
    
    img.save(os.path.join(ss_path,ss_name))



            

#  to crete a gui screen
 
title=customtkinter.CTkLabel(master=root,text="Screenshot Taker", font=("Georgia",25,"italic","bold"))
title.pack(padx=20,pady=(10,5))

frame=customtkinter.CTkFrame(master=root,width=600,height=100)
frame.pack(padx=20,pady=20 ,fill='both',expand=True)

source_lbl=customtkinter.CTkLabel(master=frame,text="Source URL's",font=(" Verdana",18,"bold"))
source_lbl.place(x=617,y=17)

source_text=customtkinter.CTkTextbox(master=frame,width=500,height=370,font=customtkinter.CTkFont('Verdana',18))
source_text.place(x=450,y=68)

name_det_lbl=customtkinter.CTkLabel(master=frame,text="Naming Details",font=(" Verdana",18,"bold"))
name_det_lbl.place(x=180,y=17)


lbl_bName=customtkinter.CTkLabel(frame,text=" Brand Name ",font=customtkinter.CTkFont('san-serif',17))
lbl_bName.place(x=40,y=70)

lbl_email=customtkinter.CTkLabel(frame,text="Email ID",font=customtkinter.CTkFont('Verdana',17))
lbl_email.place(x=40,y=117)

lbl_password = customtkinter.CTkLabel(frame,text="Passward",font=customtkinter.CTkFont('Verdana',17))
lbl_password.place(x=40,y=170)


lbl_SName=customtkinter.CTkLabel(frame,text="Screenshot Name ",font=customtkinter.CTkFont('Verdana',17))
lbl_SName.place(x=40,y=217)


lbl_CNO=customtkinter.CTkLabel(frame,text="Case Number ",font=customtkinter.CTkFont('Verdana',17))
lbl_CNO.place(x=40,y=270)

lbl_LName=customtkinter.CTkLabel(frame,text="Last Name ",font=customtkinter.CTkFont('Verdana',17))
lbl_LName.place(x=40,y=317)

lbl_timer=customtkinter.CTkLabel(frame,text="Sleep time for take ss ",font=customtkinter.CTkFont('Verdana',17))
lbl_timer.place(x=40,y=357)


lbl_message=customtkinter.CTkLabel(frame,text="",font=customtkinter.CTkFont('Verdana',17))
lbl_message.place(x=30,y=420)


brand_Opt=customtkinter.CTkOptionMenu(frame,width=160,font=customtkinter.CTkFont('Verdana',17),values=brand_list,variable=brand)
brand_Opt.place(x=260,y=70)

txt_email=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',15))
txt_email.place(x=260,y=117)
txt_email.insert(END,"robo__45")

txt_Pass=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',15))
txt_Pass.place(x=260,y=170)
txt_Pass.insert(END,"Pixel@2022")

txt_SName=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',15))
txt_SName.place(x=260,y=217)
txt_SName.insert(END,"SS")

txt_CNO=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',17))
txt_CNO.place(x=260,y=270)
txt_CNO.insert(END ,"1")
# prefix_txt.insert(0,c_date)

txt_LName=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',15))
txt_LName.place(x=260,y=317)
txt_LName.insert(0,c_date)
#

txt_timer=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',17))
txt_timer.place(x=260,y=357)
txt_timer.insert(END ,"3")





def get_data():
    global fSSName,s_no,lSSName,timer,email,password
    source_urls = source_text.get("1.0", "end-1c").split("\n") 
    for i in range(0,len(source_urls)):
        if source_urls[i] == "" or source_urls[i]== " ":
            source_urls.remove(source_urls[i])   

    brand_name =brand.get()
    email = txt_email.get();
    password = txt_Pass.get();
    fSSName = txt_SName.get();
    s_no=int(txt_CNO.get())
    lSSName  = txt_LName.get();
    screenshot_name = ""
    timer = int(txt_timer.get())
    

    if s_no<=9:
        screenshot_name = f"{fSSName}_0{s_no}_{lSSName}";

    else:
        screenshot_name = f"{fSSName}_{s_no}_{lSSName}";

    if len(source_urls) == 0:
        messagebox.askokcancel("source url is  blank !!"," Please give the source url !!")
    else:
        res= messagebox.askokcancel("Confirmation","Do you want to continue with this name ? \n\n " + screenshot_name)

        
        if res==True:
            if not os.path.exists(root_dir):
                create_root_dir()
            os.chdir(root_dir)
            if not os.path.exists(date.strftime('%d-%m-%Y')):
                os.mkdir(root_dir+"\\"+date.strftime('%d-%m-%Y'))

            try:

            # take ss start         
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--start-maximized") 
                chrome_options.add_argument("--disable-infobars")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-popup-blocking")
                chrome_options.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications": 2})
                driver = webdriver.Chrome(options=chrome_options)
                # take_ss(driver,source_urls,screenshot_name,email,password)
                
                if brand_name == "Instagram":
                    instagram_login(driver,source_urls,email,password)
                elif brand_name == "Twitter":
                    twitter_login(driver,source_urls,email,password)
                elif brand_name == "Youtube":
                    take_ss(driver,source_urls)
                elif brand_name == "LinkedIn" :
                    linkedin_login(driver,source_urls,email,password)
                elif brand_name == "Facebook":
                    facebook_login(driver,source_urls,email,password)
                elif brand_name == "Other":
                    take_ss(driver,source_urls)
                else:
                    take_ss(driver,source_urls)
                messagebox.showinfo("Screenshots Captured", "All screenshots have been captured successfully! \n you can access in c drive Instagram_Screenshot_RoboPG Folder")       
            except:
                print(traceback.format_exc())
                messagebox.showerror("Technical Problem ", "Please contact to pranjal Goyal !!")       

   

btn=customtkinter.CTkButton(frame,text="Submit",width=400,height=40,font=customtkinter.CTkFont('Verdana',25),command=get_data)
btn.place(x=35,y=400)

title=customtkinter.CTkLabel(master=root,text="𝓟𝓖@ℛ𝓞ℬ𝓞 ", font=("Verdana",22,"bold","italic"))
title.pack(padx=10,pady=(10,5))
root.mainloop()

