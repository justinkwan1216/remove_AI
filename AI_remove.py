import demakeup
import os
import cv2
#import speech_recognition as sr
import datetime
import pickle
import numpy as np
#from scipy.io.wavfile import write
#import ctypes
#import soundfile as sf
import subprocess
#import pyogg
import telepot
import time
from telepot.loop import MessageLoop, OrderedWebhook
#from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
#from pattern.web import plaintext
from pprint import pprint
import requests
#from bs4 import BeautifulSoup
#from lxml import etree
#from lxml import html
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
sched = BackgroundScheduler()



sched.start()
bot = telepot.Bot('1203610288:AAEmiNM7Dwrr4_4kv5Sohn90GLrNYdRpru8')
#bot = telepot.Bot('989811081:AAF4sUwvq8srjno5TPq-lm80LfjhNMrkL4I')
print(bot.getMe())

bot_status=0
tg_whole = {}
admin_id = [260780380]
users = []
#----------------user_command------
def display_userid(user_id,bot,chat_id,params):
    if bot_status==0:
        text = "Your user id: "+str(user_id)
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
    
def display_cmd(user_id,bot,chat_id,params):
    if bot_status==0:
        global admin_id
        text="Listed are all command available\n"
        for key, value in tg_commands_description.items() :
            text+=key+"\n"+value+"\n\n"
        if user_id in admin_id:
            for key, value in tg_admin_commands_description.items() :
                text+=key+"\n"+value+"\n\n"
            
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
    
def start(user_id,bot,chat_id,params):
    if bot_status==0:
        global users
        text=""
        if user_id not in users:
            users.append(user_id)
            text+="Welcome new user\nYou can type in /help to display all commands\njust send me image to received processed image"
            display_cmd(user_id,bot,chat_id,params)
        else:
            text+="You are already using this bot"


        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)

def set_whole(user_id,bot,chat_id,params):
    if bot_status==0:
        
        tg_whole[chat_id] = True
        text = "Enable whole picture to delete makeup"
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
    
def set_not_whole(user_id,bot,chat_id,params):
    if bot_status==0:
            
        tg_whole[chat_id] = False
        text = "Disable whole picture to delete makeup"
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)

def add_admin(user_id,bot,chat_id,params):
    global admin_id
    text=""
    params = params[0]
    try:
        params = int(params)
        if user_id in admin_id:
            if params not in admin_id:
                admin_id.append(params)
                text += "Admin with id "+str(params)+" added"
            else:
                text += "Admin with id "+str(params)+" already added"
        else:
            text += "You are not admin"
        
    except:
        text+="enter valid id"
            
        bot.sendMessage(chat_id, text)


def save_all_para(user_id,bot,chat_id,params):
    global tg_whole
    global admin_id
    global users
    text=""
    if user_id in admin_id:
        f = open('save.pickle', 'wb')
        
        pickle.dump((users,tg_whole,admin_id), f)
        f.close()
        text += "Saved all paramaters"
    else:
        text += "You are not admin"
    bot.sendMessage(chat_id, text)


def load_all_para(user_id,bot,chat_id,params):
    global tg_whole
    global admin_id
    global users
    text=""
    if user_id in admin_id:
        f = open('save.pickle', 'rb')

        users,tg_whole,admin_id = pickle.load(f)
        f.close()
        text += "Loaded all paramaters"
    else:
        text += "You are not admin"
    bot.sendMessage(chat_id, text)
def list_job(user_id,bot,chat_id,params):
    text=""
    if user_id in admin_id:
        jobs = sched.get_jobs()
        text += str(jobs)
    else:
        text += "You are not admin"
    
    bot.sendMessage(chat_id, text)

def set_bot_status(user_id,bot,chat_id,params):
    global bot_status
    text=""
    try:
        params = params[0]
        params = int(params)
        if user_id in admin_id:
            bot_status=params
            if bot_status !=0:
                sched.shutdown()
            else:
                sched.start()
            text += "bot status set to "+str(params)
        else:
            text += "You are not admin"
    except:
        text += "bot status not integer"
    bot.sendMessage(chat_id, text)
        
tg_bot = 0

tg_commands = {"/start":start,"/set_whole":set_whole,"/set_not_whole":set_not_whole,"/help":display_cmd,"/display_userid":display_userid,"/save_all_para":save_all_para,"/load_all_para":load_all_para,"/add_admin":add_admin,"/list_job":list_job,"/set_bot_status":set_bot_status}
tg_commands_description = {"help":"<usage: /help >","/set_whole":"<usage: /set_whole >","/set_not_whole":"<usage: /set_not_whole >","/display_userid":"<usage: /display_userid >"}
tg_admin_commands_description = {"/save_all_para":"<usage: /save_all_para >","/load_all_para":"<usage: /load_all_para >","/add_admin":"<usage: /add_admin (admin_id)>","/list_job":"<usage: /list_job >","/set_bot_status":"<usage: /set_bot_status (status)>"}
#----------------inside_command------
def remove_makeup(filename):
    x = demakeup.get_demakeup(filename)
    return x

def send_photo(chat_id,filename):
    bot.sendPhoto(chat_id, open(filename, 'rb'))
    
def delete_photo(filename):
    os.remove(filename)

def delete(chat_id,reply):
    messageId = reply['message_id']
    bot.deleteMessage((chat_id, messageId))
    
def parse_cmd(cmd_string):
    text_split = cmd_string.split()
    # return cmd, params
    return text_split[0], text_split[1:]

def add_command(cmd, func):
    global tg_commands
    tg_commands[cmd] = func


def remove_command(cmd):
    global tg_commands
    del tg_commands[cmd]

def scan_all_face(user_id,chat_id,image,faces,length_faces,filename):

    reply_faces = bot.sendMessage(chat_id, "Saving all face...")
    delete(chat_id, reply_faces)

    for i in range(length_faces):
        (x, y, w, h) = faces[i]
        temp_image = image[y:y+h, x:x+w]
        cv2.imwrite("photo_download/"+user_id+"/"+str(i)+"_"+filename,temp_image)
    
    removed_array=[]
    reply_AI = bot.sendMessage(chat_id, "Running AI on all face...")
    delete(chat_id, reply_AI)
    
    for i in range(length_faces):
        removed = remove_makeup("photo_download/"+user_id+"/"+str(i)+"_"+filename)
        sched.add_job(delete_photo, args=["photo_download/"+user_id+"/"+str(i)+"_"+filename])
        removed_array.append(removed)

    reply_face = bot.sendMessage(chat_id, "Putting face on original image...")
    delete(chat_id, reply_face)

    
    for i in range(length_faces):
        (x, y, w, h) = faces[i]
        temp = cv2.resize(removed_array[i], (w,h), interpolation=cv2.INTER_CUBIC)
        image[y:y+h, x:x+w]=temp
        
    return image
    
def scan_whole_face(user_id,chat_id,image,filename):
    

    reply_AI = bot.sendMessage(chat_id, "Running AI on whole image...")
    delete(chat_id, reply_AI)
    
    removed = remove_makeup("photo_download/"+user_id+"/"+filename)
    removed = cv2.resize(removed, (image.shape[1],image.shape[0]), interpolation=cv2.INTER_CUBIC)
    image = removed
    
    return image
                

def handle(msg):
    
    global bot
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    jobs = sched.get_jobs()
    if len(jobs)<=5:

        if content_type == "text":
            user_id = msg['from']['id']
            msg_text = msg['text']
            chat_id = msg['chat']['id']
            msg_id = msg['message_id']
            #print("[MSG] {uid} : {msg}".format(uid=msg['from']['id'], msg=msg_text))
            if msg_text[0] == '/':
                cmd, params = parse_cmd(msg_text)
                try:
                    sched.add_job(tg_commands[cmd], args=[user_id,bot,chat_id, params])
                    #tg_commands[cmd](user_id,bot,chat_id, params)
                    

                except KeyError:
                    bot.sendMessage(chat_id, "Unknown command: {cmd}".format(cmd=cmd))


        elif content_type == "photo":
            if bot_status==0:
                try:
                    whole = tg_whole[chat_id]
                except:
                    whole = False
                    
                reply_whole = bot.sendMessage(chat_id, "whole image is set to: "+str(whole))
                delete(chat_id, reply_whole)
                
                user_id = msg['from']['id']
                user_id = str(user_id)
                if not os.path.exists("photo_download/"+user_id):
                    os.makedirs("photo_download/"+user_id)
                
                chat_id = msg['chat']['id']
                now = datetime.datetime.now()
                file_id = msg[content_type][-1]['file_id']
                
                file_path = bot.getFile(file_id)["file_path"].split("/")[1]
                reply_received = bot.sendMessage(chat_id, "Photo received")
                delete(chat_id, reply_received)
               
                filename = 'img_' + str(user_id) + "_" + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + '-' + str(now.microsecond) + '.' + file_path.split(".")[1]

                reply_download = bot.sendMessage(chat_id, "Photo download...")
                delete(chat_id, reply_download)
                bot.download_file(msg[content_type][-1]['file_id'], "photo_download/"+user_id+"/"+filename)
                
                
                image = cv2.imread("photo_download/"+user_id+"/"+filename)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                if not whole:
                    reply_AI = bot.sendMessage(chat_id, "Scanning face...")
                    delete(chat_id, reply_AI)
                    
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags = cv2.CASCADE_SCALE_IMAGE
                    )

                    length_faces=len(faces)

                    reply_found = bot.sendMessage(chat_id, str(length_faces)+" face found")
                    delete(chat_id, reply_found)
                
                    if length_faces>0:
                        image = scan_all_face(user_id,chat_id,image,faces,length_faces,filename)
                    else:
                        image = scan_whole_face(user_id,chat_id,image,filename)
                        
                else:
                    image = scan_whole_face(user_id,chat_id,image,filename)


                cv2.imwrite("photo_download/"+user_id+"/"+"AI_"+filename,image)
                send_photo(chat_id,"photo_download/"+user_id+"/"+"AI_"+filename)
                sched.add_job(delete_photo, args=["photo_download/"+user_id+"/"+"AI_"+filename])
            else:
                bot.sendMessage(chat_id, "Bot is down")
    else:
        bot.sendMessage(chat_id, "Bot is very busy")
   

MessageLoop(bot, handle).run_as_thread()
print("I'm listening...")


while(1):
    
    time.sleep(0.01)
