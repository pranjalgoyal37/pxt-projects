import os
from pytube import YouTube, Playlist
from tkinter import messagebox
import customtkinter
import threading
import queue
import pandas as pd
from plyer import notification

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry('480x460+750+220')
root.resizable(False, False)
root.title("PG@robo Youtube Audio Downloader")

download_queue = queue.Queue()
lock = threading.Lock()

audio_info_list = []
df = pd.DataFrame(columns=["Title", "Length", "Link"])
lock = threading.Lock()

label_var = customtkinter.StringVar()
stop_download_flag = False

def download_audio_info(audio_url):
    try:
        audio = YouTube(audio_url)
        audio_info = {
            "Title": audio.title,
            "Length": audio.length,
            "Link": audio_url
        }

        with lock:
            audio_info_list.append(audio_info)
    except Exception as e:
        print(f"Error retrieving audio information: {str(e)}")

def show_audio():
    url = url_text.get().strip()
    if url.startswith("Enter"):
        label_var.set("Enter the playlist URL ??")
    elif "https://www.youtube.com/playlist" in url:
        playlist = Playlist(url)
        label_var.set("Your playlist details are starting to collect the data... ")
        # Create a thread for each audio in the playlist
        threads = [threading.Thread(target=download_audio_info, args=(audio_url,)) for audio_url in playlist]

        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Update the DataFrame with the collected audio info
        with lock:
            df = pd.DataFrame(audio_info_list)

        # Save DataFrame to Excel file
        excel_filename = os.path.join(dir_text.get().strip(), "audio_info.xlsx")
        df.to_excel(excel_filename, index=False)
    elif "https://www.youtube.com/" in url:
         audio = YouTube(url)
         print(audio.title)
         print(audio.description)
def download_single_audio(url):
    global stop_download_flag
    message = ""
    try:
        if stop_download_flag:
            return  # Stop downloading if the flag is set

        yt = YouTube(url)
        print(f"{url}   ------   {yt.title}\n")
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=dir_text.get().strip())
        print(f"Download of {yt.title} audio completed successfully!")
        label_var.set(f"Download of {yt.title} audio completed successfully!")
        message = f"Download of {yt.title} audio completed successfully!"
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")
        message = f"An error occurred while downloading {url}: {str(e)}"
        label_var.set(f"Youtube is not allowed to download this audio")
    finally:
        notification.notify(
            title='Youtube Audio downloader',
            message=message,
            app_icon=None,
            timeout=10,
        )

def download_audio_or_playlist(url, playlist_title):
    global stop_download_flag
    try:
        if stop_download_flag:
            return  # Stop downloading if the flag is set

        if 'playlist' in url.lower():
            playlist = Playlist(url)
            for audio_url in playlist.video_urls:
                label_var.set("Audio is started to download...")
                download_queue.put(audio_url)
            print("Playlist audio is completed downloaded!")
            label_var.set("Playlist audio is completed downloaded!")
        else:
            label_var.set("Download is starting...")
            download_queue.put(url)
    except Exception as e:
        label_var.set(f"An error occurred: {str(e)}")

def download_audio():
    global stop_download_flag
    stop_download_flag = False  # Reset the stop flag
    audio_urls = []
    audio_urls = source_urls_text.get("1.0", "end-1c").split("\n")
    if len(audio_urls) == 0:
        label_var.set("Enter the audio URLs ??")
    else:
        for audio_url in audio_urls:
                label_var.set("Downloading of Youtube audio has started...")
                download_queue.put(audio_url)
            

def download_audio_worker():
    global stop_download_flag
    print("Download audio worker")
    while True:
        if stop_download_flag:
            break  # Stop the thread if the flag is set
        audio_url = download_queue.get()
        if audio_url is None:
            break
        download_single_audio(audio_url)
        download_queue.task_done()

def stop_downloading():
    global stop_download_flag
    stop_download_flag = True
    label_var.set("Downloading has been stopped!")

download_thread_count = 5
download_threads = [threading.Thread(target=download_audio_worker, daemon=True) for _ in range(download_thread_count)]
for thread in download_threads:
    thread.start()

def on_textbox_click(event):
    
     if url_text.get() == "Enter the YouTube audio or playlist URL":
        url_text.delete(0, customtkinter.END) 



dir_lbl = customtkinter.CTkLabel(master=root, text="Directory", font=("Verdana", 18))
dir_lbl.place(x=20, y=20)

dir_text = customtkinter.CTkEntry(master=root, height=30, width=325, font=customtkinter.CTkFont('Verdana', 12))
dir_text.place(x=140, y=20)
dir_text.insert(customtkinter.END, r"D:\GLA_DATA\4th sem")

url_lbl = customtkinter.CTkLabel(master=root, text="Playlist URL", font=("Verdana", 18))
url_lbl.place(x=20, y=70)

url_text = customtkinter.CTkEntry(master=root, height=30, width=325, font=customtkinter.CTkFont('Verdana', 12))
url_text.place(x=140, y=70)
url_text.insert(customtkinter.END, "Enter the YouTube audio or playlist URL")

url_text.bind("<FocusIn>", on_textbox_click)

source_lbl = customtkinter.CTkLabel(master=root, text="URL's", font=("Verdana", 18))
source_lbl.place(x=20, y=200)

source_urls_text=customtkinter.CTkTextbox(master=root,width=325,height=180,font=customtkinter.CTkFont('Verdana',12))
source_urls_text.place(x=140,y=120)


message_lbl =customtkinter.CTkLabel(master=root,textvariable = label_var,font=customtkinter.CTkFont('Verdana',14))
message_lbl.place(x=140, y=320)



btn = customtkinter.CTkButton(root, text="show audio info", width=120, height=10, font=customtkinter.CTkFont('Verdana', 13), command=show_audio)
btn.place(x=10, y=370)

btn = customtkinter.CTkButton(root, text="download playlist", width=140, height=10, font=customtkinter.CTkFont('Verdana', 14), command=download_audio_or_playlist)
btn.place(x=145, y=370)

btn = customtkinter.CTkButton(root, text="Download_videos", width=160, height=10, font=customtkinter.CTkFont('Verdana', 14), command=download_audio)
btn.place(x=300, y=370)

btn = customtkinter.CTkButton(root, text="Stop the downloading", width=260, height=10, font=customtkinter.CTkFont('Verdana', 14), command=stop_downloading)
btn.place(x=100, y=420)

root.mainloop()


