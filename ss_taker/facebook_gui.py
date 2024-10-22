import pyautogui as py
from selenium import webdriver
from datetime import datetime
import time
import re
from PIL import Image, ImageDraw
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import customtkinter 
from tkinter import messagebox

now=datetime.now()
c_date = now.strftime('_%d%m%y')
date = now.strftime('%d-%m-%y')

india_page=mexico_page= usa_page= canada_page=0
india = mexico = usa = canada = 0

highlight_response = 1
root_dir = r"C:\Facebook_Screenshot_Taker\Screenshots"

def fb_login(driver):
    
    driver.get('https://www.facebook.com')
    driver.find_element(By.NAME,'email').send_keys("shivanimfilter@yahoo.com")
    driver.find_element(By.NAME,'pass').send_keys("Mshivani7&")
    driver.find_element(By.NAME,'login').click()

def take_ss(source_urls,display_urls):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    driver = webdriver.Chrome(chrome_options=option)

    driver.maximize_window()
    driver_size=driver.get_window_size()
    driver.set_window_position(-8,-8)
    driver.set_window_size(driver_size['width'],driver_size['height'])
    fb_login(driver)

    for count,(source,display) in enumerate(zip(source_urls,display_urls),1):
        
        driver.get(source)
        if count==1:
            py.keyDown('ctrl')
            py.press(['-','-','-'])
            py.keyUp('ctrl')
            

        try:
            wait=WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'#\:r2c\: > div.x1n2onr6 > div > a > div.x78zum5.x5yr21d.xl56j7k.x1n2onr6.xh8yej3 > div.__fb-dark-mode.x1afcbsf.x1uhb9sk.x1swf91x > div')))
            time.sleep(1)
            source_img = py.screenshot('C:\Facebook_Screenshot_Taker'+"\\"+'source.jpg')

        except:
            source_img = py.screenshot('C:\Facebook_Screenshot_Taker'+"\\"+'source.jpg')
        


        driver.get(display)
        d_url = driver.current_url
        set_display_page(d_url,driver)
        time.sleep(.5)
        display_img = py.screenshot('C:\Facebook_Screenshot_Taker'+"\\"+'display.jpg')
        
        final_img=merge_img()
        save_screenshot(final_img,d_url)
    driver.close()

def merge_img():

        s_ss=Image.open("C:\Facebook_Screenshot_Taker\source.jpg").crop((0,40,1920,1020))
        d_ss=Image.open("C:\Facebook_Screenshot_Taker\display.jpg").crop((0,40,1920,1020))

        if highlight_response == 1:
            draw=ImageDraw.Draw(s_ss)
            draw.rectangle([60,150,260,175],outline='red',width=3)

        source_img_size=s_ss.size
        display_img_size=d_ss.size

        merge_image = Image.new('RGB', ((source_img_size[0]+display_img_size[0]),source_img_size[1]), (250, 250, 250))
        merge_image.paste(s_ss, (0, 0))
        merge_image.paste(d_ss, (s_ss.size[0], 0))

        return merge_image

def set_display_page(display_url,driver):
        global india_page, mexico_page, usa_page, canada_page
        if india_page == 0 and re.search("https://www.amazon.in/", display_url):
            py.keyDown('ctrl')
            py.press(['-','-','-'])
            py.keyUp('ctrl')
            time.sleep(2)
            india_page += 1
            

        elif usa_page == 0 and re.search("https://www.amazon.com/", display_url):
            py.keyDown('ctrl')
            py.press(['-','-','-'])
            py.keyUp('ctrl')
            time.sleep(2)
            usa_page += 1
            

        elif canada_page == 0 and re.search("https://www.amazon.ca/", display_url):
            py.keyDown('ctrl')
            py.press(['-','-','-'])
            py.keyUp('ctrl')
            time.sleep(2)
            canada_page+=1
            

        elif mexico_page == 0 and re.search("https://www.amazon.com.mx/", display_url):
            py.keyDown('ctrl')
            py.press(['-','-','-'])
            py.keyUp('ctrl')
            time.sleep(2)
            usa_page+=1
        
def create_country_folders(country):
    os.chdir(root_dir)
    if not os.path.exists(f_date):
        os.mkdir(f_date)
        
    os.chdir(root_dir + "\\" + f_date)

    if not os.path.exists(root_dir + "\\" + f_date+"\\"+country):
        os.mkdir(country)
    return  root_dir + "\\" + f_date+"\\"+country


def create_root_dir():

    os.chdir('C:/')
    if not os.path.exists('Facebook_Screenshot_Taker'):
        os.mkdir('C:/'+'Facebook_Screenshot_Taker')
    if not os.path.exists(root_dir):
        os.mkdir('C:/'+'Facebook_Screenshot_Taker'+"//"+"Screenshots")
    os.chdir(root_dir)

def save_screenshot(final_img, d_url):
# def save_screenshot():
    global india, usa, mexico, canada , other_country
    print(check_response)
    print(d_url)
    if re.search("https://www.amazon.in/", d_url):
        path=create_country_folders("india")
        if (india <= 9):
            final_img.save(path +"\\"+ suffix + "0" +str(india )+ "_"+f_date + ".jpg")
        else:
            final_img.save(path +"\\"+ suffix +str(india )+ "_"+f_date + ".jpg")
        india+=1

    elif re.search("https://www.amazon.ca/", d_url):
        path=create_country_folders("canada")

        if (canada <= 9):
            final_img.save(path +"\\"+ suffix + "0" +str(canada)+ "_"+f_date + ".jpg")
        else:
            final_img.save(path +"\\"+ suffix +str(canada)+ "_"+f_date + ".jpg")
        canada += 1

    elif re.search("https://www.amazon.com/", d_url):
        path=create_country_folders("USA")
        if (usa <= 9):
            final_img.save(path +"\\"+ suffix + "0" +str(usa)+ "_"+f_date + ".jpg")
        else:
            final_img.save(path +"\\"+ suffix +str(usa)+ "_"+f_date + ".jpg")
        usa += 1

    elif re.search("https://www.amazon.com.mx/", d_url):
        path=create_country_folders("mexico")
        if(mexico<=9):
            final_img.save(path +"\\"+ suffix + "0" +str(mexico)+ "_"+f_date + ".jpg")
        else:
            final_img.save(path +"\\"+ suffix  +str(mexico)+ "_"+f_date + ".jpg")
        mexico += 1

    else :
        path=create_country_folders("Other Country")
        if(other_country <=9):
            final_img.save(path +"\\"+ suffix + "0" +str(other_country)+ "_"+f_date + ".jpg")
        else:
            final_img.save(path +"\\"+ suffix  +str(other_country)+ "_"+f_date + ".jpg")
        other_country += 1
    
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root =customtkinter.CTk()
root.geometry('1000x700+300+30')
root.resizable(False, False)
root.title("Screenshot Taker By Pranjal Goyal")
root.attributes('-alpha',0.85)


def display_input():
        global highlight_response
        highlight_response=check_response.get()

def get_data():
    global s_no ,c_date,f_date,suffix,india, usa, mexico, canada,other_country,highlight_response
    highlight_response=check_response.get()

    india=usa=mexico=canada=other_country=int(s_no_txt.get())

    source_urls=source_text.get("1.0", "end-1c").split("\n")
    display_urls=display_text.get("1.0", "end-1c").split("\n")

    if len(source_urls) != len(display_urls):
        messagebox.showwarning("warning ","please check the total no of display and source url ")
    else:
        s_no=int(s_no_txt.get())
        c_date=prefix_txt.get()
        f_date=c_date.split('_')[1]
        suffix=suffix_txt.get()

        if not os.path.exists(root_dir):
            print("create_root_dir")
            create_root_dir()
        start_time=time.time()


        take_ss(source_urls,display_urls)

        end=time.time()
        print(end-start_time)
        # except Exception as e:
        #     print(e)
        #     pass

root.geometry('1000x650')
title=customtkinter.CTkLabel(master=root,text="Facebook Screenshot Taker ", font=("monospace",24))
title.pack(padx=40,pady=(15,5))
frame=customtkinter.CTkFrame(master=root,width=600,height=400)
frame.pack(padx=20,pady=(20,0),fill='both',expand=True)

check_response=customtkinter.IntVar(value=1)

display_lbl=customtkinter.CTkLabel(master=frame,text="Display URL's",font=("monospace",18))
display_lbl.place(x=620,y=20)

display_text=customtkinter.CTkTextbox(master=frame,width=400,height=300)
display_text.place(x=500,y=50)

source_lbl=customtkinter.CTkLabel(master=frame,text="Source URL's",font=("monospace",18))
source_lbl.place(x=180,y=15) 

source_text=customtkinter.CTkTextbox(master=frame,width=400,height=300)
source_text.place(x=20,y=50)

def preview_name():
    no=int(s_no_txt.get())
    if no<=9:
        no= "0"+str(no)
    else:
        no=str(no)

    ss_name=suffix_txt.get()+str(no)+prefix_txt.get()+".jpg"
    pre_name_lbl.configure(text=ss_name)

frame_02=customtkinter.CTkFrame(root,width=100 ,height=200)
frame_02.pack(padx=10,pady=10,fill='both',expand=True)

ll_ss_name=customtkinter.CTkLabel(frame_02,text="Screenshot name -:",font= ("Arial",14))
ll_ss_name.place(x=20,y=20)

preview_lbl=customtkinter.CTkLabel(frame_02,text="Preview SS name ",font= ("Arial",14))
preview_lbl.place(x=20,y=60)


suffix_txt=customtkinter.CTkEntry(frame_02, width=300)
suffix_txt.place(x=160,y=20)
suffix_txt.insert(0,"pxt_amazoncl1_sm_fake_handle_")


s_no_txt=customtkinter.CTkEntry(frame_02,width=100)
s_no_txt.place(x=480,y=20)
s_no_txt.insert(0,1)


prefix_txt=customtkinter.CTkEntry(frame_02,width=200)
prefix_txt.place(x=600,y=20)
prefix_txt.insert(0,c_date)


pre_name_lbl=customtkinter.CTkLabel(frame_02,font= ("Arial",14))
pre_name_lbl.place(x=160,y=60)
pre_name_lbl


submit_btn=customtkinter.CTkButton(frame_02,text="Submit",width=160,font=("Arial",24),command=get_data)
submit_btn.place(x=650,y=60)

preview_btn=customtkinter.CTkButton(frame_02,text="Preview",width=140,font=("Arial",24),command=preview_name)
preview_btn.place(x=480,y=60)

t1 = customtkinter.CTkCheckBox(frame_02, text="Highlight_handler", variable=check_response, onvalue=1, offvalue=0, command=display_input)
t1.place(x=50,y=90)

root.mainloop()

