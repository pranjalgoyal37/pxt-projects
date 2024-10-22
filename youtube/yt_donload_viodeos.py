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
root.title("PG@robo Youtube Videos Downloader")

download_queue = queue.Queue()
lock = threading.Lock()

video_info_list = []
df = pd.DataFrame(columns=["Title", "Length", "Link"])
lock = threading.Lock()

label_var = customtkinter.StringVar()
stop_download_flag = False

def download_video_info(video_url):
    try:
        video = YouTube(video_url)
        video_info = {
            "Title": video.title,
            "Length": video.length,
            "Link": video_url
        }

        with lock:
            video_info_list.append(video_info)
    except Exception as e:
        print(f"Error retrieving video information: {str(e)}")

def show_videos():
    url = url_text.get().strip()
    if url.startswith("Enter"):
        label_var.set("Enter the  playlist url ??")
    elif "https://www.youtube.com/playlist" in url:
        print("Start!! ")
        playlist = Playlist(url)
        label_var.set("Your playlist details are starting to collect the data... ")
        # Create a thread for each video in the playlist
        threads = [threading.Thread(target=download_video_info, args=(video_url,)) for video_url in playlist]

        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Update the DataFrame with the collected video info
        with lock:
            df = pd.DataFrame(video_info_list)

        # Save DataFrame to Excel file
        excel_filename = os.path.join(dir_text.get().strip(), "video_info.xlsx")
        df.to_excel(excel_filename, index=False)
    elif "https://www.youtube.com/" in url:
         video = YouTube(url)
         print(video.title)
         print(video.description)
def download_single_video(url):
    global stop_download_flag
    message = ""
    try:
        if stop_download_flag:
            return  # Stop downloading if the flag is set

        yt = YouTube(url)
        print(f"{url}   ------   {yt.title}\n")
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path=dir_text.get().strip())
        print(f"Download of {yt.title} completed successfully!")
        label_var.set(f"Download of {yt.title} completed successfully!")
        message = f"Download of {yt.title} completed successfully!"
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")
        message = f"An error occurred while downloading {url}: {str(e)}"
        label_var.set(f"Youtube is not allowed to download this video")
    finally:
        notification.notify(
            title='Youtube Video downloader',
            message=message,
            app_icon=None,
            timeout=10,
        )

def download_playlist():
    global stop_download_flag
    stop_download_flag = False  # Reset the stop flag
    url = url_text.get().strip()
    if url == "" :
        label_var.set("Enter the valid playlist URL ??")
    else:
        playlist_title = Playlist(url).title
        download_video_or_playlist(url, playlist_title)
        label_var.set("Downloading of Youtube videos has started...")

def download_video_or_playlist(url, playlist_title):
    global stop_download_flag
    try:
        if stop_download_flag:
            return  # Stop downloading if the flag is set

        if 'playlist' in url.lower():
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                label_var.set("Video is started to download...")
                download_queue.put(video_url)
            print("Playlist is completed downloaded!")
            label_var.set("Playlist is completed downloaded!")
        else:
            label_var.set("Download is starting...")
            download_queue.put(url)
    except Exception as e:
        label_var.set(f"An error occurred: {str(e)}")

def download_video():
    global stop_download_flag
    stop_download_flag = False  # Reset the stop flag
    video_urls = []
    video_urls = source_urls_text.get("1.0", "end-1c").split("\n")
    if len(video_urls) == 0:
        label_var.set("Enter the video URLs ??")
    else:
        for video_url in video_urls:
                label_var.set("Downloading of Youtube videos has started...")
                download_queue.put(video_url)
            

def download_worker():
    global stop_download_flag
    print("Download worker")
    while True:
        if stop_download_flag:
            break  # Stop the thread if the flag is set
        video_url = download_queue.get()
        if video_url is None:
            break
        download_single_video(video_url)
        download_queue.task_done()

def stop_downloading():
    global stop_download_flag
    stop_download_flag = True
    label_var.set("Downloading has been stopped!")

# download_thread = threading.Thread(target=download_worker,daemon=True)
# download_thread.start()

download_thread_count = 1
download_threads = [threading.Thread(target=download_worker, daemon=True) for _ in range(download_thread_count)]
for thread in download_threads:
    thread.start()

def on_textbox_click(event):
    
     if url_text.get() == "Enter the YouTube video or playlist URL":
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
url_text.insert(customtkinter.END, "Enter the YouTube video or playlist URL")
# url_text.insert(customtkinter.END, demo_url)

url_text.bind("<FocusIn>", on_textbox_click)

source_lbl = customtkinter.CTkLabel(master=root, text="URL's", font=("Verdana", 18))
source_lbl.place(x=20, y=200)

source_urls_text=customtkinter.CTkTextbox(master=root,width=325,height=180,font=customtkinter.CTkFont('Verdana',12))
source_urls_text.place(x=140,y=120)


message_lbl =customtkinter.CTkLabel(master=root,textvariable = label_var,font=customtkinter.CTkFont('Verdana',14))
message_lbl.place(x=140, y=320)


btn = customtkinter.CTkButton(root, text="show videos info", width=120, height=10, font=customtkinter.CTkFont('Verdana', 13), command=show_videos)
btn.place(x=10, y=370)

btn = customtkinter.CTkButton(root, text="download playlist", width=140, height=10, font=customtkinter.CTkFont('Verdana', 14), command=download_playlist)
btn.place(x=145, y=370)

btn = customtkinter.CTkButton(root, text="Download_videos", width=160, height=10, font=customtkinter.CTkFont('Verdana', 14), command=download_video)
btn.place(x=300, y=370)

btn = customtkinter.CTkButton(root, text="Stop the downloading", width=260, height=10, font=customtkinter.CTkFont('Verdana', 14), command=stop_downloading)
btn.place(x=100, y=420)

root.mainloop()










# import os
# import threading
# import queue
# import pandas as pd
# from tkinter import messagebox
# import customtkinter
# import youtube_dl

# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("dark-blue")
# root = customtkinter.CTk()
# root.geometry('480x460+750+220')
# root.resizable(False, False)
# root.title("PG@robo Youtube Videos Downloader")

# download_queue = queue.Queue()
# lock = threading.Lock()

# video_info_list = []
# df = pd.DataFrame(columns=["Title", "Length", "Link"])
# lock = threading.Lock()

# label_var = customtkinter.StringVar()
# stop_download_flag = False

# def download_video_info(video_url):
#     try:
#         if not video_url:
#             print("Error: Empty URL")
#             return

#         with youtube_dl.YoutubeDL() as ydl:
#             info = ydl.extract_info(video_url, download=False)
#             video_info = {
#                 "Title": info.get('title', ''),
#                 "Length": info.get('duration', 0),
#                 "Link": video_url
#             }

#             with lock:
#                 video_info_list.append(video_info)
#     except Exception as e:
#         print(f"Error retrieving video information: {str(e)}")


# def show_videos():
#     url = url_text.get().strip()
#     if url.startswith("Enter"):
#         label_var.set("Enter the  playlist url ??")
#     elif "https://www.youtube.com/playlist" in url:
#         playlist_title = ""
#         with youtube_dl.YoutubeDL() as ydl:
#             playlist_info = ydl.extract_info(url, download=False)
#             playlist_title = playlist_info.get('title', '')
#             for entry in playlist_info['entries']:
#                 video_url = entry['url']
#                 threading.Thread(target=download_video_info, args=(video_url,)).start()

#         label_var.set("Your playlist details are starting to collect the data... ")
#     elif "https://www.youtube.com/" in url:
#         threading.Thread(target=download_video_info, args=(url,)).start()

# def download_video():
#     global stop_download_flag
#     stop_download_flag = False  # Reset the stop flag
#     video_urls = source_urls_text.get("1.0", "end-1c").split("\n")
#     if len(video_urls) == 0:
#         label_var.set("Enter the video URLs ??")
#     else:
#         for video_url in video_urls:
#             threading.Thread(target=download_video_info, args=(video_url,)).start()

# def stop_downloading():
#     global stop_download_flag
#     stop_download_flag = True
#     label_var.set("Downloading has been stopped!")

# def on_textbox_click(event):
#     if url_text.get() == "Enter the YouTube video or playlist URL":
#         url_text.delete(0, customtkinter.END) 

# dir_lbl = customtkinter.CTkLabel(master=root, text="Directory", font=("Verdana", 18))
# dir_lbl.place(x=20, y=20)

# dir_text = customtkinter.CTkEntry(master=root, height=30, width=325, font=customtkinter.CTkFont('Verdana', 12))
# dir_text.place(x=140, y=20)
# dir_text.insert(customtkinter.END, r"D:\GLA_DATA\4th sem")

# url_lbl = customtkinter.CTkLabel(master=root, text="Playlist URL", font=("Verdana", 18))
# url_lbl.place(x=20, y=70)

# url_text = customtkinter.CTkEntry(master=root, height=30, width=325, font=customtkinter.CTkFont('Verdana', 12))
# url_text.place(x=140, y=70)
# url_text.insert(customtkinter.END, "Enter the YouTube video or playlist URL")

# url_text.bind("<FocusIn>", on_textbox_click)

# source_lbl = customtkinter.CTkLabel(master=root, text="URL's", font=("Verdana", 18))
# source_lbl.place(x=20, y=200)

# source_urls_text=customtkinter.CTkTextbox(master=root,width=325,height=180,font=customtkinter.CTkFont('Verdana',12))
# source_urls_text.place(x=140,y=120)

# message_lbl =customtkinter.CTkLabel(master=root,textvariable=label_var,font=customtkinter.CTkFont('Verdana',14))
# message_lbl.place(x=140, y=320)

# btn = customtkinter.CTkButton(root, text="show videos info", width=120, height=10, font=customtkinter.CTkFont('Verdana', 13), command=show_videos)
# btn.place(x=10, y=370)

# btn = customtkinter.CTkButton(root, text="Download_videos", width=160, height=10, font=customtkinter.CTkFont('Verdana', 14), command=download_video)
# btn.place(x=300, y=370)

# btn = customtkinter.CTkButton(root, text="Stop the downloading", width=260, height=10, font=customtkinter.CTkFont('Verdana', 14), command=stop_downloading)
# btn.place(x=100, y=420)

# root.mainloop()

