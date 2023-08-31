import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from pytube import YouTube ##pip install pytube
#from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import instaloader # pip install instaloader
import threading
import os

root = tk.Tk()
root.title("Downloader")
root.minsize(517, 170)

def openfile():
    print ("open file function activated")

def savefile():
    print ("save file function activated")

def help():
    messagebox.showinfo(title="About", message="Instagram and YouTube Downloder version 1.0 !")

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_command(label="Save", command=savefile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut")
editmenu.add_command(label="Copy")
editmenu.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=help)
menubar.add_cascade(label="Help", menu=helpmenu)

root .config(menu=menubar)

def widgets():
    global my_progress,label2
    link_label = tk.Label(root, text="Vide Link")
    link_label.grid(row=0, column=0, padx=20)
    link_label.config(font=("None", 15), fg="blue")

    link_input = tk.Entry(root, width=40, textvariable=video_link)
    link_input.grid(row=0, column=1, padx=20)
    
    link_label = tk.Label(root, text="Post Link")
    link_label.grid(row=1, column=0, padx=20)
    link_label.config(font=("None", 15), fg="blue")

    postLink_Entry = tk.Entry(root, width=40, textvariable=insta_link)
    postLink_Entry.grid(row=1, column=1, padx=20)

    place_label = tk.Label(root, text="Directory")
    place_label.grid(row=2, column=0)
    place_label.config(font=("None", 15), fg="blue")

    place_input = tk.Entry(root, width=30, textvariable=download_dir)
    place_input.grid(row=2, column=1, sticky="w", padx=20)

    place_btn = tk.Button(root, text="Open", width="11", bg="blue", fg="white", command=browse)
    place_btn.grid(row=2, column=2)

    download_btn = tk.Button(text="Download Youtube", command=thread)
    download_btn.grid(row=0, column=2, pady=10)
    download_btn.config(height=1, width=14, bg="green", fg="white")
    
    download_btn = tk.Button(text="Download Post", command=downloadPost)
    download_btn.grid(row=1, column=2, pady=10)
    download_btn.config(height=1, width=13, bg="green", fg="white")
    
    my_progress=ttk.Progressbar(root,orient=HORIZONTAL,length=400,mode="indeterminate")
    label2=Label(root,text="0%",font=("Arial Bold",15))



def thread():
  thread=threading.Thread(target=downloda)
  thread.start()



def on_progress(stream, chunk, bytes_remaining):
  global inc,my_progress,label2
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage_of_completion = bytes_downloaded / total_size * 100
  inc=int(percentage_of_completion)
  print(inc)
  my_progress["value"]+=inc-my_progress["value"]
  label2.config(text=f"{inc}%")
  if my_progress["value"]==100:
    my_progress.grid_forget()
    label2.grid_forget()
    label2["text"]="0%"



def browse():
    directory = askdirectory(initialdir="YOUR DIRECTORY PATH", title="save")
    download_dir.set(directory)

def downloda():
    global my_progress
    my_progress.config(mode="determinate")
    my_progress.grid(row=5,column=0,columnspan=2)
    label2.grid(row=5,column=2)
    link = video_link.get()
    save_dir = download_dir.get()
    yt = YouTube(link)
    yt.register_on_progress_callback(on_progress)
    yt.streams.filter(res="720p").first().download(save_dir)
    messagebox.showinfo(title="Success", message="Your vide download successfully!")
    
    
def downloadPost():
    global my_progress
    my_progress.grid(row=4,column=0,columnspan=2)
    my_progress.start(5)
    link = insta_link.get()
    
    def download():
        
        if 'https://www.instagram.com/p/' in link:
            try:
                location = filedialog.askdirectory()
                os.chdir(location)
                URL = link.replace('https://www.instagram.com/p/', '')
                URL = URL.replace('/','')
                L = instaloader.Instaloader()
                L.login('user', 'password')
                post = instaloader.Post.from_shortcode(L.context, URL)
                L.download_post(post, target=URL)
                my_progress.grid_forget()
                messagebox.showinfo('Info', 'Download Compeleted!')
                
            except:
                my_progress.grid_forget()
                messagebox.showerror('Error', 'URL IS INCORRECT')
                
        else:
            my_progress.grid_forget()
            messagebox.showerror('Error', 'URL NOT FOUND')
            
    
    threading.Thread(target=download).start()


exit_btn = tk.Button(text='Exit App', bg='#121212', fg='white', borderwidth=3, font=('Arial', 11), width=30, command=root.destroy)
exit_btn.grid(row=4, column=2, pady=5)
exit_btn.config(height=1, width=7, bg="red", fg="white")

download_dir = tk.StringVar()
video_link = tk.StringVar()
insta_link = tk.StringVar()

widgets()

root.mainloop()
