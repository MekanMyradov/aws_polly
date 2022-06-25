# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 20:07:58 2022

@author: mekan_myradov

Hello, this project is the part of Cloud Computing course.
"""

import tkinter as tk
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing

window = tk.Tk()
window.geometry("720x480")
window.title("Polly");

text_field = tk.Text(window, height=10)
text_field.pack()

def get_text():
    # Connect to the AWS
    aws_connect = boto3.session.Session(profile_name="tmp_user")
    client = aws_connect.client(service_name="polly", region_name='us-east-1')
    
    
    text = text_field.get("1.0", "end")
    # print(text)
    
    speech = client.synthesize_speech(Text=text, Engine='neural', OutputFormat='mp3', VoiceId='Joanna')
    # print(speech)
    
    # Check if there is the audio in a returned result. If there is save the audio to a file. Otherwise raise exception.
    if "AudioStream" in speech:
        with closing(speech['AudioStream']) as stream:
            audio_path = os.path.join(gettempdir(), "speech.mp3")
            try:
                with open(audio_path, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
                
    else:
        print("Could not found AudioStream")
        sys.exit(-1)
    
    if sys.platform == "win32":
        os.startfile(audio_path)

button = tk.Button(window, height=1, width=10, text="Read Aloud", command=get_text)
button.pack()

window.mainloop()