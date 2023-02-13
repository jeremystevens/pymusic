# /usr/bin/python
# Copyright 2023 Jeremy Stevens <jeremiahstevens@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
__version__ = '1.0.0' # current version

from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from ttkbootstrap.toast import ToastNotification
# other required imports 
import pygame
import pydub
import threading

# create a window
root = ttk.Window(themename="darkly",  title="PyMusic V1.0")
# set the alpha of the window
root.attributes("-alpha", 0.8)
# set geometry of main window
root.geometry("307x220")
# set the icon of the window
#root.iconphoto(False, tk.Image(file='music.png'))
style = ttk.Style(theme='vapor')


###################
# Functions for the buttons
###################
def browseFiles():
    global file_path
    # plays all music files
    file_path = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3 *.wav *.ogg")])
    #file_path = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3")])
    if file_path:
        # get name of the song without the file extension
        SongTitleLbl.config(text="Song Title:  " + file_path.split("/")[-1])
        # renove the file extension from the file name
        SongTitleLbl.config(text="Song Title:  " + file_path.split("/")[-1].split(".")[0])
        # set song title label to the song title remove file type extension from the file name

 #thread to update time remaining
def  updatRemainder(file_path):
    thread = threading.Thread(target=updateRemainingTime, args=(file_path,))
    thread.start()

def updateRemainingTime(file_path):
    # get the length of the song
    audio = pydub.AudioSegment.from_mp3(file_path)
    length = len(audio)
    # get the current time of the song
    current_time = pygame.mixer.music.get_pos()
    # calculate the remaining time
    remaining_time = length - current_time
    # convert the time to minutes and seconds
    remaining_time = remaining_time / 1000
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    # set the time remaining label to the remaining time
    TimeRemainingLbl.config(text="Time Remaining: " + str(int(minutes)) + ":" + str(int(seconds)))
    # call this function to update remaining time after every 100 milliseconds
    TimeRemainingLbl.after(100, updateRemainingTime, file_path)


def songPos(value):
    # using threading to update the slider
    thread = threading.Thread(target=findPositionThread , args=(value,))
    thread.start()
 # a function to find the postion of a song using the slider
def findPositionThread(value):
    # current postion and time in a song in milliseconds
    currentPostion = pygame.mixer.music.get_pos()
    currentTime = pygame.mixer.music.get_pos()
    # convert the value of the slider to milliseconds
    value = int(value) * 1000
    # if the value of the slider is greater than the current time of the song
    if value > currentTime:
        # calculate the difference between the value of the slider and the current time
        difference = value - currentTime
        # add the difference to the current time to get the new time
        newTime = currentTime + difference
        # set the new time of the song
        pygame.mixer.music.set_pos(newTime)
        # play current postion
        pygame.mixer.music.play(newTime)
    # if the value of the slider is less than the current time of the song
    elif value < currentTime:
        # calculate the difference between the value of the slider and the current time
        difference = currentTime - value
        # subtract the difference from the current time to get the new time
        newTime = currentTime - difference
        # set the new time of the song
        pygame.mixer.music.set_pos(newTime)
        # play from current time
        pygame.mixer.music.play(newTime)
        
        
        
def changeVolumeThread(value):
    # change the volume of the music
    pygame.mixer.music.set_volume(float(value) / 100)

# function to use keyboard to change volume
def keyboardVolume(event):
    # get the current volume
    currentVolume = pygame.mixer.music.get_volume()
    # if keyboard up is pressed increase the volume
    if event.keysym == "Up":
        # increase the volume by 0.1
        pygame.mixer.music.set_volume(currentVolume + 0.1)
        # set the volume slider to the new volume
        volumeSlider.set(pygame.mixer.music.get_volume() * 100)
    # if keyboard down is pressed decrease the volume
    elif event.keysym == "Down":
        # decrease the volume by 0.1
        pygame.mixer.music.set_volume(currentVolume - 0.1)
        # set the volume slider to the new volume
        volumeSlider.set(pygame.mixer.music.get_volume() * 100)
        
        
# create a function that uses threading to change the volume
def changeVolume(value):
    # create a thread
    thread = threading.Thread(target=changeVolumeThread, args=(value,))
    # start the thread
    thread.start()
    
def playMusic():
    pygame.init()
    updatRemainder(file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    song = file_path.split("/")[-1].split(".")[0]
    toastsong("Now Playing", song, 3000)
    pass

def  pcheck():
    if pygame.mixer.music.get_busy() == True:
        pauseMusic()
    else:
        resumeMusic()
    root.after(100, pcheck)
    
def pauseMusic():
    pygame.mixer.music.pause()
    
def resumeMusic():
    pygame.mixer.music.unpause()
    pass

def stopMusic():
    pygame.mixer.music.stop()
    pass
# toast the song title
def toastsong(title, message, duration):
    toast = ToastNotification(
    title=title,
    message=message,
    duration=3000,)
    toast.show_toast()
    
####################
# add controls to window
#####################

# song title label
SongTitleframe = ttk.Labelframe(bootstyle="primary", text="Song Title")
# show in the center of the window
SongTitleframe.pack(fill=tk.BOTH, expand=True)
# create a label for file name and add it to frame
SongTitleLbl = ttk.Label(SongTitleframe, text="")
# show in the center of the window
SongTitleLbl.pack(fill=tk.BOTH, expand=True)

#  Time Remaining in a song
TimeRemainingframe = ttk.Labelframe(bootstyle="primary", text="Time Remaining")
# show in the center of the window
TimeRemainingframe.pack(fill=tk.BOTH, expand=True)
# create label for time remaining and add it to frame
TimeRemainingLbl = ttk.Label(TimeRemainingframe, text="")
# show in the center of the window
TimeRemainingLbl.pack(fill=tk.BOTH, expand=True)

# songp postion slider
songPositionSlider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=songPos , length=300, width=5, resolution=1)
# add song position slider to window
songPositionSlider.pack()
sep1 = ttk.Separator()
# add separator to window
sep1.pack(fill=tk.BOTH, expand=True)

# Volume slider & label
volumelable = ttk.Label(bootstyle="primary", text="Volume")
volumelable.pack()
volumeSlider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=changeVolumeThread , length=200, width=5, resolution=1)
# set volme to 100
volumeSlider.set(100)
volumeSlider.pack()

# sperator
sep = ttk.Separator()
# add separator to window
sep.pack(fill=tk.BOTH, expand=True)

# browse and open file button
browseBtn = ttk.Button(bootstyle="primary", text="Open File", command=browseFiles)
# add browse button to to side of the play button
browseBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#browseBtn.pack(fill=tk.BOTH, expand=True)

# play button
playbtn = ttk.Button(bootstyle="primary", text="Play", command=playMusic)
# add to the side of the browse button
playbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# pause button
pauseBtn = ttk.Button(bootstyle="primary", text="Pause", command=pcheck)
# add pause button to window to the side of the play button
pauseBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# stop button
stopBtn = ttk.Button(bootstyle="primary", text="Stop", command=stopMusic)
# add stop button to window to the side of the pause button
stopBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# call keyboardVolume function when  the up or down key is pressed
root.bind("<Up>", keyboardVolume)
# call keyboardVolume function when  the up or down key is pressed
root.bind("<Down>", keyboardVolume)
# get the current time of the song
# check if music is playing
# main loop
root.mainloop()


