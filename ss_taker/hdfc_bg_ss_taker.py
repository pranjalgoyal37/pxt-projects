
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import customtkinter 
from tkinter import messagebox
from tkinter  import *
from tkcalendar import DateEntry
# import pyautogui as py
import pandas as pd
from PIL import Image
import time
import re
import random


ss_source=[]
ss_description=[]
missing_source=[]
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root =customtkinter.CTk()
root.geometry('1000x700+300+30')
root.resizable(False, False)
root.title("Screenshot Taker By Pranjal Goyal")
root.attributes('-alpha',0.85)

now=datetime.now()
s_no=1
backup_s_no=100
root_dir = r"C:\HDFC_ICICI_Screenshot_Taker\Screenshots"
brand_list=['HDFC','ICICI','RBL','youtube',]
category_list=['customer_care','fake_handle','Fake_Job_Promotions','informatic_video','fake_bio','infringement','youtube']
brand=StringVar()
info=StringVar()
category=StringVar()
brand.set(brand_list[0])
category.set(category_list[0])
insta_count=0
twitter_count=0
credentials = [
    {'username':'Sahilusman27883','password':'Pixel@2022'},
    {'username':'John85258866721','password':'12345@pixel'},
    {'username':'ShaluGupta23','password':'Pixel@2022'},
    {'username':'RaghavShar79925','password':'Pixel@2022'},
    {'username':'GargRovin','password':'Pixel@2022'},
    {'username':'grawalArpiy','password':'Pixel@2022'},
    {'username':'nine_param49754','password':'Pixel@2022'},
    {'username':'sita364','password':'Pixel@2022'}
]


def create_root_dir():

    os.chdir('C:/')
    if not os.path.exists('HDFC_ICICI_Screenshot_Taker'):
        os.mkdir('C:/'+'HDFC_ICICI_Screenshot_Taker')
    if not os.path.exists(root_dir):
        os.mkdir('C:/'+'HDFC_ICICI_Screenshot_Taker'+"//"+"Screenshots")
    os.chdir(root_dir)

def twitter_login(driver,username,password):
    print("you are in twitter login function")
    # driver.get("https://twitter.com/login")
    # username = "nine_param49754"
    # password = 'Pixel@2022'
   
    time.sleep(3)
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)

    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def facebook_login(driver):
    driver.get("https://www.facebook.com/login/")
    username="rgarg4822@gmail.com"
    password ="Pixel@2022"
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    username_field.send_keys(username)


    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pass")))
    password_field.send_keys(password)
    time.sleep(2)
    driver.find_element(By.NAME ,"login").click()
    time.sleep(2)

def delete_cache(driver):
    try:
        driver.execute_script("window.open('');")
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        driver.get('chrome://settings/clearBrowserData')
        time.sleep(2)
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB * 1 + Keys.ENTER)
        actions.perform()
        time.sleep(2)
        
        driver.switch_to.window(driver.window_handles[0])
        print("_____________________________________________________________cache_clear________________________________________________________________")
    except:
        pass
        print("------------------------cookies_not_cleared-----------------------------------------------------------")

def instagram_login(driver):

    driver.get("https://www.instagram.com/accounts/login")
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.send_keys('rgarg4822')
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys('PIXEL@2022')
    time.sleep(1)
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[2]/form/div/div[3]').click()
    time.sleep(5)

def linkedin_login(driver):
    driver.get("https://in.linkedin.com/")
    time.sleep(8)                                                                               
    driver.find_element(By.NAME,'session_key').send_keys('rgarg4822@gmail.com')
    driver.find_element(By.NAME,'session_password').send_keys('Pixel@2022')
    driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()


def take_ss(source_urls,date,brand_name,category_name,missing_text,driver):
    facebook_count = 1

    path='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div'
  
    for no,source in enumerate (source_urls,1):
        url_no = no%50
        url_bar_source=driver.current_url
        if re.search("https://www.facebook.com",source) and facebook_count ==1:
            facebook_login(driver)
            facebook_count +=1

        if re.search("https://www.instagram.com",source) and insta_count ==1:
            instagram_login(driver)
            insta_count +=1

        if re.search("https://twitter.com/i/flow/login",url_bar_source) :
            
            driver.implicitly_wait(7)
            creds = random.choice(credentials)
            password = creds['password']
            username=creds['username']
            twitter_login(driver,username,password)
        
        
        if url_no == 0  and re.search("https://twitter.com",source):
            driver.delete_all_cookies()
            delete_cache(driver)

        driver.get(source)

      
        print()
        

        if category_name == "customer_care":
                print(category_name)
                
                try: 
                    wait=WebDriverWait(driver,4).until(EC.visibility_of_element_located((By.XPATH,path)))
                    title=driver.title
                    url=driver.current_url
                    if driver.title != "Tweet / Twitter":
                        time.sleep(4)
                        # s_ss = py.screenshot()
                        driver.save_screenshot("C:\HDFC_ICICI_Screenshot_Taker\source.jpg")

                        # s_ss.save('C:\HDFC_ICICI_Screenshot_Taker\source.jpg')
                        crop_image(date,brand_name,category_name)

                        ss_description.append(title)
                        ss_source.append(url)
                    else:
                        print(source)
                        print(missing_text)
                        missing_source.append(source)    

                except Exception as e:
                    print(e)
                    missing_source.append(source)
        else:            
            time.sleep(6)
            driver.save_screenshot("C:\HDFC_ICICI_Screenshot_Taker\source.jpg")
            # s_ss = py.screenshot()
            # s_ss.save('C:\HDFC_ICICI_Screenshot_Taker\source.jpg')
            crop_image(date,brand_name,category_name)
          
# driver = webdriver.F()
# driver.save_screenshot()
def crop_image(date,brand_name,category_name):
    global s_no
    img = Image.open(r"C:\HDFC_ICICI_Screenshot_Taker\source.jpg").convert('RGB')
    img_size = img.size

    # if img_size[1] in range(900,1100):
    #     img = img.crop((0, 42,img_size[0],img_size[1]-65))
    # else:
    #     img = img.crop((0, 32,img_size[0],img_size[1]-55))
    

    if not os.path.exists(brand_name +" "+category_name ):
        os.mkdir(root_dir+"\\"+date.strftime('%d-%m-%Y')+"\\"+brand_name+" "+category_name)
    save_path=os.path.join(root_dir,date.strftime('%d-%m-%Y'),brand_name+" "+category_name)

    if (s_no <= 9):
        print(save_path)
        img.save(save_path+"\\"+"pxt_"+str(brand_name)+"_"+str(category_name)+"_" +"0"+ str(s_no) +str(date.strftime('_%d%m%y')) + ".jpg")
        
    else:
        img.save(save_path+"\\"+"pxt_"+str(brand_name)+"_"+str(category_name)+"_"+ str(s_no) +str(date.strftime('_%d%m%y')) + ".jpg")
    s_no += 1




def get_data():
    global s_no,missing_source
    missing_source = []
    missing_text.delete("1.0", "end")
    source_urls=source_text.get("1.0", "end-1c").split("\n") 
    for i in range(0,len(source_urls)):
        if source_urls[i] == "" or source_urls[i]== " ":
            source_urls.remove(source_urls[i])   
    
    s_no=int(txt_CNO.get())
    date=date_entry.get_date()
    brand_name =brand.get()
    category_name=category.get()
    len_source="Total source  url is :"+str(len(source_urls))
    info_lbl.configure(text=len_source)

    if s_no<=9:
        screenshot_name = "pxt_"+str(brand_name)+"_"+str(category_name)+"_" +"0"+ str(s_no) +str(date.strftime('_%d%m%y')) + ".jpg"
    else:
        screenshot_name = "pxt_"+str(brand_name)+"_"+str(category_name)+"_" + str(s_no) +str(date.strftime('_%d%m%y'))+ ".jpg"

    
    if len(source_urls) == 0:
        messagebox.askokcancel("source url is  blank !!"," the source url !!")
    else:
        res= messagebox.askokcancel("Confirmation","Do you want to continue with this name ? \n\n " + screenshot_name)

        if res==True:
            if not os.path.exists(root_dir):
                create_root_dir()
            os.chdir(root_dir)
            if not os.path.exists(date.strftime('%d-%m-%Y')):
                os.mkdir(root_dir+"\\"+date.strftime('%d-%m-%Y'))
            os.chdir(root_dir+"//"+date.strftime('%d-%m-%Y'))


            try:
                chrome_options =Options()
                chrome_options.add_argument('--disable-notifications')
                driver=webdriver.Firefox()
                driver.maximize_window()
                take_ss(source_urls,date,brand_name,category_name,missing_text,driver)

                if missing_source !=0:
                    df=pd.DataFrame(missing_source)
                    df_02=pd.DataFrame(ss_description,ss_source)
                    with pd.ExcelWriter(root_dir+"//"+str(date.strftime('%d-%m-%Y'))+"//"+f"{brand_name}_{now.strftime('%H-%M')}.xlsx") as writer:
                        df.to_excel(writer,sheet_name="missing_source_url",index=False)
                        df_02.to_excel(writer,sheet_name=f"{brand_name}_{now.strftime('%d-%m-%Y')}",index=False)
                    df.to_clipboard(sep=' ',index=False)    
                    missing_text.insert(END, "\n".join(missing_source))

            except Exception as e:
                print(e)
                if missing_source !=0:
                    df=pd.DataFrame(missing_source)
                    df_02=pd.DataFrame(ss_description,ss_source)
                    with pd.ExcelWriter(root_dir+"//"+str(date.strftime('%d-%m-%Y'))+"//"+f"{brand_name}_{now.strftime('%H-%M')}.xlsx") as writer:
                        df.to_excel(writer,sheet_name="missing_source_url",index=False)
                        df_02.to_excel(writer,sheet_name=f"{brand_name}_{now.strftime('%d-%m-%Y')}",index=False)
                    df.to_clipboard(sep=' ',index=False)    
                    missing_text.insert(END, "\n".join(missing_source))

            len_source="Total missing source  url is :"+str(len(missing_source))
            missing_lbl.configure(text=len_source)

title=customtkinter.CTkLabel(master=root,text="HDFC_ICICI Screenshot Taker ", font=("Georgia",25,"italic","bold"))
title.pack(padx=40,pady=(10,5))

frame=customtkinter.CTkFrame(master=root,width=600,height=280)
frame.pack(padx=20,fill='both',expand=True)


source_lbl=customtkinter.CTkLabel(master=frame,text="Source URL's",font=(" Verdana",18,"bold"))
source_lbl.place(x=620,y=20)

source_text=customtkinter.CTkTextbox(master=frame,width=500,height=270,font=customtkinter.CTkFont('Verdana',18))
source_text.place(x=450,y=68)

name_det_lbl=customtkinter.CTkLabel(master=frame,text="Naming Details",font=(" Verdana",18,"bold"))
name_det_lbl.place(x=180,y=20)


lbl_bName=customtkinter.CTkLabel(frame,text=" Brand Name ",font=customtkinter.CTkFont('san-serif',20))
lbl_bName.place(x=40,y=70)

lbl_date=customtkinter.CTkLabel(frame,text=" Date ",font=customtkinter.CTkFont('Verdana',20))
lbl_date.place(x=40,y=130)


lbl_CNO=customtkinter.CTkLabel(frame,text=" Case Number ",font=customtkinter.CTkFont('Verdana',20))
lbl_CNO.place(x=40,y=190)


lbl_category=customtkinter.CTkLabel(frame,text=" Category ",font=customtkinter.CTkFont('Verdana',20))
lbl_category.place(x=40,y=250)                      


brand_Opt=customtkinter.CTkOptionMenu(frame,width=160,font=customtkinter.CTkFont('Verdana',17),values=brand_list,variable=brand)
brand_Opt.place(x=260,y=70)

date_entry=DateEntry(frame,width=8,font=('Verdana 20'))
date_entry.place(x=260,y=120)

txt_CNO=customtkinter.CTkEntry(frame, width=160,font=customtkinter.CTkFont('Verdana',20))
txt_CNO.place(x=260,y=190)
txt_CNO.insert(END,"1")

category_Opt=customtkinter.CTkOptionMenu(frame,width=160,font=customtkinter.CTkFont('Verdana',17),values=category_list,variable=category)
category_Opt.place(x=260,y=250)
# category_Opt.config(CTkfont=("Verdana  11"))

btn=customtkinter.CTkButton(frame,text="Submit",width=400,height=40,font=customtkinter.CTkFont('Verdana',25),command=get_data)
btn.place(x=35,y=300)


title=customtkinter.CTkLabel(master=root,text=" Info Details", font=(" Verdana",24,"bold","italic"))
title.pack(padx=40,pady=(10,5))

frame_02=customtkinter.CTkFrame(root,width=100 ,height=150)
frame_02.pack(padx=20,pady=10,fill='both',expand=True)

source_lbl=customtkinter.CTkLabel(master=frame_02,text="Missing Source URL's",font=(" Verdana",18,"bold"))
source_lbl.place(x=620,y=20)


info_lbl=customtkinter.CTkLabel(frame_02,text="Total length of source : ",font=customtkinter.CTkFont('Verdana',17))
info_lbl.place(x=20,y=60)

missing_text=customtkinter.CTkTextbox(frame_02,width=550,font=customtkinter.CTkFont('Verdana',17))
missing_text.place(x=400,y=50)

missing_lbl=customtkinter.CTkLabel(frame_02,text="Total Missing  source url's is : ",font=customtkinter.CTkFont('Verdana',17))
missing_lbl.place(x=20,y=100)


root.mainloop()