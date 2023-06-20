# ---------------------Importing-Libraries---------------------------------
import numpy as np
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import speech_recognition as sr
import os
import re
import sys
from moviepy.editor import *

# GUI
from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk

try:
    os.remove("my_concatenation.mp4")
except:
    pass

# ------------------------------------SPEECH RECOGNITION-------------------------------
r = sr.Recognizer()


def Speech(textbox):
    textbox.delete("0.0", "end")
    with sr.Microphone() as source:  # using microphone as input
        print("Listening...")
        audio = r.listen(source)
        print("Processing...")
        try:
            vishal = r.recognize_google(audio)
            print("You said:", vishal)
            textbox.insert(END, vishal)  # updating recognized text in textbox
        except:
            textbox.insert(END, "try again Sorry, I couldn't understand what you said.")


def translate(textbox):
    stop=[ 'me', 'our', 'ours', 'ourselves', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourselves', 'him', 'his', 'himself',  "she's", 'hers', 'it', "it's", 'its', 'itself',  'them', 'their', 'theirs', 'themselves', "whom" ,'that', "that'll",  'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'if', 'or', 'because', 'as', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'into', 'through', 'during',  'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', ' further', 'then', 'once', 'here', 'there', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',  'nor', 'not', 'only', 'own',  'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "shouldve", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn']
    input_text = str(textbox.get("0.0", "end"))
    sentences = nltk.sent_tokenize(input_text)
    wl = WordNetLemmatizer()
    ps = PorterStemmer()
    for i in range(len(sentences)):
        review = re.sub("[^a-z A-Z]", " ", sentences[i])
        review = review.lower()
        review = review.split()
        review = [
            wl.lemmatize(ps.stem(word))
            for word in review
            if not word in set(stop)
        ]
    print(review)
    arg_array = []
    try:
        for text in review:
            path = "C:/Users/VISHAL/Desktop/surya/AIML/"
            path="C:/Users/VISHAL/Desktop/surya/AIML/sign languages/"
            arg_array.append(VideoFileClip(path + text + ".mp4"))
            print(text + ".mp4")
        print(arg_array[0])
        final_clip = concatenate_videoclips(arg_array, method="compose")
        final_clip.write_videofile("my_concatenation.mp4")
        cap = cv2.VideoCapture("my_concatenation.mp4")
        cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Video Player", 780, 494)

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                cv2.imshow("Video Player", frame)
            quitButton = cv2.waitKey(25) & 0xFF == ord("q")
            closeButton = (
                cv2.getWindowProperty("Video Player", cv2.WND_PROP_VISIBLE) < 1
            )

            if quitButton or closeButton:
                break
        cap.release()
        cv2.destroyAllWindows()
    except:
        textbox.delete("0.0", "end")
        textbox.insert(END, "Sorry for inconvience!!! Given word is not present in our database.We are expanding our dataset")
        print(
            "Apologies for the inconvenience! It appears that the word you're seeking is currently on an adventurous expedition away from our database.",
            "But we're diligently working on expanding our dataset to ensure that no word can escape our grasp in the future.",
            " So, please bear with us for a while",
            sep=" ",
        )


# --------------------------------------GUI------------------------------------
def GUI():
    set_appearance_mode("system")
    set_default_color_theme("blue")


    root = CTk()
    root.geometry("900x600")
    root.title("Sign language Translator")

    # Title label
    lbT = CTkLabel(master=root, text="Sign Language Translator", font=("cascadia code", 28))
    lbT.place(relx=0.5, rely=0.1, anchor=CENTER)

    #lbT.place(x=270, y=50)


    # textbox for providing text
    textbox = CTkTextbox(
        master=root, width=392, height=250, font=("cascadia code", 20), border_width=1
    )
    textbox.configure(fg_color=root._fg_color)
    textbox.place(relx=0.5, rely=0.5, anchor=CENTER)





    # importing image to use on microphone button
    img = CTkImage(Image.open(r"C:\Users\VISHAL\Downloads\microphone.png"), size=(45, 45))
    img.configure(fg_color=root._fg_color)


    # microphone button to call speech function
    btM = CTkButton(master=root,text="",width=15,image=img,fg_color="#242424",hover_color="#242424",corner_radius=15,command= lambda: Speech(textbox))
    btM.place(relx=0.674, rely=0.66, anchor=CENTER)


    # translate button to call translate function
    btT = CTkButton(master=root,width=40,text="Translate",font=("cascadia code", 22),corner_radius=30,command=lambda :translate(textbox))
    btT.place(relx=0.5, rely=0.8, anchor=CENTER)

    # main loop of tkinter window
    root.mainloop()


def main():
    GUI()
    
if __name__ == "__main__":
    main()