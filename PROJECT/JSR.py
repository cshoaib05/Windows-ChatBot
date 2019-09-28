from __future__ import absolute_import
import json
import socket
from word2number import w2n
import urllib
import pyowm
import bs4 as bs
from urllib.request import FancyURLopener
import clipboard
import imdb
import threading
import youtube_dl
from smspy import Way2sms
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

import apiai

from gtts import gTTS
import speech_recognition as sr
import os, random
import subprocess
from bs4 import BeautifulSoup
from win32com.client import Dispatch
import re
import sys
import webbrowser
import smtplib
import pyttsx3
import requests
import playsound
import time
import wikipedia
import wolframalpha
import datetime
import gsearch
# from weather import Weather


CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', '3b0e24b4a9754d8b977392a250774aaf')
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

request = ai.text_request()

request.session_id = os.environ.get(
    'API_AI_SESSION_ID', 'dd60fde7-c6ab-4f38-9487-7300c42b4916')



#Taskkill /IM chrome.exe /F

def typeCommand():
    inp = input("ME :")
    return inp 

def gsearch(word):
    url="http://www.google.com/?#q="
    webbrowser.open_new_tab(url+word)

def ysearch(word):
    url="http://www.youtube.com/results?search_query="
    webbrowser.open_new_tab(url+word)


def speak(s,audio):
    import pythoncom
    pythoncom.CoInitialize()
    print("Asistnt: "+audio)
    try:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate+0)
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')

        engine.say(audio)
        #engine.connect('started-word', onWord)
        engine.runAndWait()
    except:
        engine.stop()
        try:
            engine.say(audio)
            #engine.connect('started-word', onWord)
            engine.runAndWait()
        except:
            engine.stop()

def talkToMe(audio):
    "speaks audio passed as argument"
    t = threading.Thread(target= speak, name="thread1", args= (0,audio))
    t.start()
    #assistant(typeCommand())
 

def myCommand():
    "listens for commands"
    r = sr.Recognizer()

    with sr.Microphone() as source:
        #r.pause_threshold = 1
        print('Ready...')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source,phrase_time_limit=10)

    try:
        command = r.recognize_google(audio).lower()
        #talkToMe('Tumne ye bola: ' + command)
        print('You Said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        #print('Your last command couldn\'t be heard')
        #talkToMe("missed your words")
        print("missed your words")
        command = myCommand();
    except:
        print("No Internet connection bye")
        talkToMe("No Internet connection bye")
        sys.exit()

    
    return command

def sendsms(command):
	w2s = Way2sms()
	w2s.login('8879562143', 'H3298C')

	contacts = {'shoaib':9167075383,'salman':9664366965,'mobin':8652747053,'moin':7738545542,'s':9967186330,'atto':9930022877}
	
	for i in contacts:
		if i in command:
			command = command.replace("send text to","").replace("send sms to","").replace('that',"").replace(i,"")
			break
	else:
		print("no such contact found")
		return

	w2s.send(contacts[i], command)
	print(command)
	print(contacts[i])
	w2s.logout()



def assistant(command):
    "if statements for executing commands"
    #os.system('nircmd.exe killprocess wmplayer.exe')


        

    if command == "hello1" or command == "hi1" or command=="hey1":
        print("hello ")
        talkToMe("hello sir")
    elif 'clear'==command:
        os.system("cls")

    elif ('from' in command or 'what' in command or 'where' in command or 'who' in command or 'whose' in command or 'when' in command or 'how' in command or 'whom' in command or 'why' in command or 'which' in command):
        #talkToMe('I don\'t know what you mean!')
        try:
            request = ai.text_request()
            request.query = command
            response = request.getresponse().read()
            output = json.loads(response)
            answer = output["result"]["fulfillment"]["speech"]
            #print('answer:',answer)
            #talkToMe(answer)

            if(answer=="" or answer=="not found"):
                #talkToMe(answer+" on layer 1") 
                try:
                    
                    client = wolframalpha.Client("4E3H79-A3ARKHYKU9")
                    #print('command:',command)
                    res = client.query(command)
                    answer = next(res.results).text
                    #print(answer)
                    talkToMe(answer)
                    #talkToMe("improve your internet speed")
                except:
                    try:
                        
                        print("IN WIKI")
                        talkToMe(wikipedia.summary(command))
                        #talkToMe("improve your internet speed")
                    except:
                        talkToMe("Sorry I got nothing, do you want me to search on google?")
                        if(typeCommand()=='yes'):
                            print("IN gsearch")
                            gsearch(command)
                        else:
                            talkToMe("OK, ask me something else.")
            else:
                talkToMe(answer)
                pass
        except:
            pass

    elif command == "what time is it" or command == "tell me time" or command == "what's the time" or command == "time" or command == "what is today" or command == "what's today" :
        t = time.asctime(time.localtime(time.time()))
        talkToMe(t)

    elif 'send text' in command or 'send sms' in command:
    	sendsms(command)

    elif '-' in command or '+' in command or '*' in command or '/' in command or '%' in command:
        try:
            talkToMe(str(eval(command)))
        except:
            talkToMe("not a valid equation")

    elif command == "bye" or command == "buy" or command=='exit':
        if hr >= 20 and hr <=24:
            print("Good night\n")
            talkToMe("Good night")
            sys.exit()
        else:
            print("see you again \n")
            talkToMe("see you again ")
            sys.exit()

    elif command == "how are you1":
        print("I'm good. How are you?\n")
        talkToMe("I'm good. How are you?")

    elif 'stop' in command:
        #engine.stop()
        talkToMe(command)

    elif command == "ok1" or command == 'okay1' or command == 'yeah1':
        print("Yes")
        talkToMe("yes")
    

    elif 'open' in command:

        if 'website' in command:
            reg_ex = re.search('open website (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
                print('Done!')

        elif 'notes' in command or 'note' in command:
            os.system('start "" "D:\\PYTHON\\PROJECT\\Notes.txt"')
        
        else:
            #command = 'open notepad'
            command = command.replace('open ',"")
            #command = command.replace(" ","")
            
            os.system('nircmd sendkeypress rwin')
            for i in command:
                os.system('nircmd sendkeypress '+i)
            os.system('nircmd sendkeypress enter')


    elif 'movie' in command:
        command =  command.replace("movie","")
        command =  command.replace("about","")
        command = command.title()

        
        try:
            print("Name of a movie:"+command.replace("about movie",""))
            app = imdb.IMDb()
            results = app.search_movie(command)
            #if not results:
            #breturn "error 404"
            first = results[0]
            ID = first.movieID
            data = app.get_movie(ID)
            talkToMe("Year: "+str(data['year']))
            talkToMe("IMDb ratings: "+str(data['rating']))
        except:
           talkToMe("Error 404 not found")


    elif 'search' in command or 'google' in command or 'images of' in command or 'image of' in command or 'google map' in command:
        
        if 'images' in command:
            url = "https://www.google.com/search?tbm=isch&q={}".format(command.replace("images of", ""))
            webbrowser.open(url)

        
        #command=command.replace('on',"")
        elif 'google map' in command:
            url = "https://www.google.co.in/maps/place/" + command.replace("google map","")
            webbrowser.open(url)

        else:
            command=command.replace('google',"")
            command=command.replace('search',"")
            gsearch(command)






    elif 'youtube' in command or "video" in command:

        command=command.replace("on","")
        command=command.replace("search","")

        if 'play' in command:
            command=command.replace("play","")
            command=command.replace("on","")
            command=command.replace("youtube","")
            try:
                def ytPlayer(word):
                    a=[]
                    #word = input()

                    url = 'https://www.youtube.com/results?search_query=+'+word
                    yt='https://www.youtube.com'
                    #webbrowser.open_new_tab(url)

                    class MyOpener(FancyURLopener):
                        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'   # Set this to a string you want for your user agent

                    myopener = MyOpener()
                    page = myopener.open(url).read()
                    webpage = page.decode('utf-8')

                    soup = bs.BeautifulSoup(webpage,'lxml')

                    div = soup.body
                    for data in div.find_all(href=True):
                        a.append(data.get('href'))

                #print(a)

                    matching = [s for s in a if '/watch?' in s]
                # print(matching[0])

                    ytplaylink = yt+matching[0]

                # print(ytplaylink)
                # pwrshllink= 'powershell -command Invoke-WebRequest '+ytplaylink+' -OutFile '+word+'.mp3'
                    webbrowser.open_new_tab(ytplaylink)
                    

                ytPlayer(command)
                return
            except:
                ytPlayer(command)

        if "download" in command:
            command=command.replace("video","")
            command=command.replace("download","")
            a1=[]
            a11=[]
            word1 =command #input('ENTER THE VIDEO NAME TO DOWNLOAD')

            url1 = 'https://www.youtube.com/results?search_query=+'+word1
            yt1='https://www.youtube.com'
            #webbrowser.open_new_tab(url)

            class MyOpener1(FancyURLopener):
                version1 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'   # Set this to a string you want for your user agent
            myopener1 = MyOpener1()
            page1 = myopener1.open(url1).read()
            webpage1 = page1.decode('utf-8')

            soup1 = bs.BeautifulSoup(webpage1,'lxml')

            div1 = soup1.body
            for data1 in div1.find_all(href=True):
                a1.append(data1.get('href'))

            #print(a)

            matching1 = [s1 for s1 in a1 if '/watch?' in s1]

            ytplaylink1 = yt1+matching1[0]

            print(ytplaylink1)
            #os.walk(r"D:\ArmanK\python_programs\SUBLIME_FILES\SpeechRecog\video")
            def download():
                quality=input('WHICH QUALITY DO YOU WANT ME TO DOWNLOAD?')
                if '' in quality:
                    pass
                if '240' in quality:
                    r=os.system('"cd /d E:\\VIDEOS" && youtube-dl -f 5 '+ytplaylink1)
                if '360' in quality:
                    r=os.system('"cd /d E:\\VIDEOS" && youtube-dl -f 43 '+ytplaylink1)
                elif '480' in quality:
                    r=os.system('"cd /d E:\\VIDEOS" && youtube-dl -f 18 '+ytplaylink1)
                elif '720' in quality:
                    r=os.system('"cd /d E:\\VIDEOS" && youtube-dl -f 22 '+ytplaylink1)
                if(r==1):
                    print('THE FORMAT YOU SELECTED NOT FOUND... PELASE SELECT LOWER QUALITY')
                    download()

            download()
        else:
            ysearch(command.replace('youtube',""))

    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/',headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('hahaha')

    elif 'facts' in command:
        fw = open('D:\\PYTHON\\PROJECT\\.facts.txt',encoding="utf8")
        facts = fw.read()
        facts = facts.split('\n')
        while True:    
            i = random.randrange(0,len(facts)-1)
            #print(facts[i])
            talkToMe(facts[i])
            break

    elif 'quotes' in command:
        fw = open('D:\\PYTHON\\PROJECT\\.quotes.txt','r')
        vocab = fw.read()
        vocab = vocab.split('\n')

        while True:
            i = random.randint(0,2002)
            if i % 2 == 0:
                if len(vocab[i]) < 118:
                    #sendmessage(vocab[i],vocab[i+1])
                    #print(vocab[i]+" said by "+vocab[i+1])
                    talkToMe(vocab[i]+" said by "+vocab[i+1])
                    break
                else:
                    continue
            else:
                continue

    elif 'teach me' in command:
        fw = open('D:\\PYTHON\\PROJECT\\.vocab.txt','r')
        vocab = fw.read()
        vocab = vocab.split('\n')

        while True:
            i = random.randint(0,len(vocab)-1)
            if i % 2 == 0:
                #sendmessage(vocab[i],vocab[i+1])
                print(vocab[i]+"--"+vocab[i+1])
                for j in range(3):
                    talkToMe(vocab[i]+" meaning "+vocab[i+1]+".")
                break
            else:
                continue

    elif 'cricket' in command:
        url = "http://static.cricinfo.com/rss/livescores.xml"
        sc = requests.get(url)
        soup = BeautifulSoup(sc.text,'lxml')

        i = 1
        for data in soup.findAll('item'):
            print(str(i)+'. '+data.find('description').text)
            i += 1
         

        '''for i in range(10):
            url = 'http://www.snapple.com/real-facts/list-view/'+str(i+1)
            print('url:',url)       
            sc = requests.get(url)
            soup = BeautifulSoup(sc.text,'lxml')
            fact = soup.findAll('p',{'class':'fact_detail'})
            print('fact:',fact)
            for i in range(len(fact)):
                fw.write(fact[i].text+'')
        '''

    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'armaan' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('username', 'password')

            #send message`
            mail.sendmail('Arman Khan', 'ak682015@gmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')


    elif 'lock'== command:
        subprocess.call('rundll32.exe user32.dll,LockWorkStation')

    elif 'new folder' in command:
        os.system('mkdir ad')

    elif 'new file' in command:
        talkToMe("name of a file?")
        #name=str(myCommand())
        name=str(typeCommand())
        if('python' in command):
            os.system('NUL >'+ name+'.py')
        else:
            os.system('NUL >'+name+'.txt')
        talkToMe("File Created")
 
    elif 'cmd' in command:
        os.system('start "" "C:\\WINDOWS\\system32\\cmd.exe"')

    elif 'take a note' in command:


        f = open('Notes.txt','a')
        t = time.asctime(time.localtime(time.time()))
        f.write('\n'+t+'\n'+command.replace('take a note that',"")) 
        f.close()
        talkToMe("Done")

    elif 'read my notes' in command:
        f = open('Notes.txt','r')
        talkToMe(f.read())
        f.close()

    elif 'clear my notes' in command:
        f = open('Notes.txt','w')
        f.close()
        talkToMe("Done")

    

    elif 'minimise all' in command:
        os.system('nircmd sendkeypress rwin+"d"')

    elif 'maximise all' in command:
        os.system('nircmd sendkeypress rwin+shift+"m"')

    elif 'volume' in command or 'silent' in command or 'mute' in command:
        if 'max' in command or 'full' in command:
            os.system('nircmd.exe mutesysvolume 30000')
        elif 'increase' in command or 'up' in command:
            os.system('nircmd.exe changesysvolume 10000')
        elif 'decrease' in command or 'down' in command:
            os.system('nircmd.exe changesysvolume -10000')
        elif 'silent' in command or 'mute' in command:
            os.system('nircmd.exe mutesysvolume 1')
        else:
            os.system('nircmd.exe mutesysvolume 0')


    elif 'low brightness' in command or 'low light' in command:
        os.system('nircmd.exe setbrightness 5')
    elif 'medium brightness' in command or 'medium light' in command:
        os.system('nircmd.exe setbrightness 50')
    elif 'full brightness' in command or 'max light' in command: 
        os.system('nircmd.exe setbrightness 100')
    elif 'screen of' in command:
        os.system('nircmd.exe monitor off')
    elif 'screen on' in command:
        os.system('nircmd sendkeypress ctrl')
    elif 'empty bin' in command:
        os.system('nircmd.exe emptybin')

    elif 'next song' in command:
        a=str(random.choice(os.listdir("E:\\MUSIC")))
        path = "E:\\MUSIC"+'\\'+a
        os.system(path)

    elif 'song' in command or 'music' in command or 'play' in command:
        print("IN SONG")

        command=command.title()
        command=command.replace('Song',"")
        command=command.replace('Music',"")
        command=command.replace('Play',"")
        for root, dirs,files in os.walk("E:\\MUSIC"):
            for file in files:
                file = file.replace('(',"")
                file = file.replace(')',"")
                # file = file.replace(''," ") 
                # file = file.replace('('," ")
                # file = file.replace('('," ")
                # file = file.replace('('," ")
                if command in file.replace('_',' '):
                    path = "E:\\MUSIC"+'\\'+file
                    os.system('"'+path+'"')
                    break
            else:
                talkToMe("Song Not Found. Do you want me to Download it?")
                if(typeCommand()=='yes'):
                    a2=[]
                    word2 = command.replace('play',"")
                    word2 = command.replace('song',"")
                    word2 = word2+' lyrics'
                    url2 = 'https://www.youtube.com/results?search_query=+'+word2
                    yt2='https://www.youtube.com'
                    #webbrowser.open_new_tab(url)
                    class MyOpener2(FancyURLopener):
                        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'   # Set this to a string you want for your user agent

                    myopener2 = MyOpener2()
                    page2 = myopener2.open(url2).read()
                    webpage2 = page2.decode('utf-8')

                    soup2 = bs.BeautifulSoup(webpage2,'lxml')

                    div2 = soup2.body
                    for data2 in div2.find_all(href=True):
                        a2.append(data2.get('href'))

                        #print(a)

                    matching2 = [s2 for s2 in a2 if '/watch?' in s2]
                    asa2 =matching2[0]
                    asa2 = asa2.replace('/watch?v=','')
                    print(asa2)
                    # webbrowser.open(DLlink)

                    ytplaylink2 = yt2+matching2[0]
                    print(ytplaylink2)
                    word2 = word2.replace(" ","_")
                    word2 = '1_'+word2
                    os.system('"cd /d E:\\MUSIC" && youtube-dl --output '+word2+'.%(ext)s -i --extract-audio --audio-format mp3 --audio-quality 0 '+ytplaylink2)
                    #webbrowser.open_new_tab(ytplaylink)
                else:
                    talkToMe("Ok, ask me something else.")

    elif 'music' in command or 'song' in command or 'play' in command:
        a=str(random.choice(os.listdir("E:\\MUSIC")))
        path = "E:\\MUSIC"+'\\'+a
        os.system(path)

    

        #if 'video' in command:
         #   command=command.title()




    elif 'stop music'in command:
        os.system('nircmd.exe killprocess wmplayer.exe')

    elif 'task manager' in command:
        os.system('nircmd sendkeypress ctrl+shift+esc')

    elif 'clipboard' in command or 'clip board' in command:
        talkToMe(clipboard.paste())

    elif 'calculate' in command:

        value = command.replace("what's ", "")
        value = command.replace("calculate","")
        value = value.replace(" times", "*")
        value = value.replace(" plus", "+")
        value = value.replace(" minus", "-")
        value = value.replace(" divides", "/")
        value = value.replace(" divide", "/")
        value = value.replace(" x", "*")
        print(value)

        try:
            
            finalValue = eval(value)
            #print(finalValue)
            #eval(finalValue)
            talkToMe(finalValue)
                

        except:
            try:
                client = wolframalpha.Client("4E3H79-A3ARKHYKU9")
                #print('command:',command)
                res = client.query(command)
                answer = next(res.results).text
                #print(answer)

                #print("IN WIKI")
                talkToMe(answer)
            except:
                talkToMe("I don't Understand")

    elif 'current temperature' in command:
        owm = pyowm.OWM('3b8dc8474c4fdddfea2631f41f134a97')  
        obs = owm.weather_at_place("Mumbai,in")  
        temperature=obs.get_weather().get_temperature('celsius')
        talkToMe("The temperature is "+str(temperature['temp_max'])+" degree celsius")

    elif 'change wallpaper' in command:
        a=str(random.choice(os.listdir("C:\\Users\\HP-Probook\\Downloads")))
        print('a',a)
        pic_path = "C:\\Users\\HP-Probook\\Downloads"+'\\'+a
        print('pic_path',pic_path)
        cmd = 'REG ADD \"HKCU\\Control Panel\\Desktop\" /v Wallpaper /t REG_SZ /d \"%s\" /f' %pic_path
        os.system(cmd)
        os.system('rundll32.exe user32.dll, UpdatePerUserSystemParameters')
        os.system('rundll32.exe user32.dll, UpdatePerUserSystemParameters')
        print('Wallpaper is set.')


    # elif 'open' in command:
    #     #command = 'open notepad'
    #     command = command.replace('open',"")
    #     command = command.replace(" ","")
        
    #     os.system('nircmd sendkeypress rwin')
    #     for i in command:
    #         os.system('nircmd sendkeypress '+i)
    #     os.system('nircmd sendkeypress enter')

    elif 'news' in command:
        req = Request('https://www.google.com/search?q=news&client=firefox-b-ab&source=lnms&tbm=nws&sa=X&ved=0ahUKEwiwo5iM-pHaAhUIqo8KHSlQBbwQ_AUIDCgD&biw=1366&bih=654', headers={'User-Agent': 'Mozilla/5.0'})

        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')

        soup = bs.BeautifulSoup(webpage,'lxml')

        div = soup.body

        for data in div.find_all('h3'):
            news=data.text
            print(news)

    elif (command==""):
        assistant(typeCommand())
            
            

    else:
        request = ai.text_request()
        request.query = command
        response = request.getresponse().read()
        output = json.loads(response)
        answer = output["result"]["fulfillment"]["speech"]
        #talkToMe(answer)
        if(answer=="" or answer=="not found"):

            talkToMe("What "+command+"? "+"do you want me to search deeply?")
            #if(myCommand()=='yes'):
            if(typeCommand()=="yes"):
                try:
                    client = wolframalpha.Client("4E3H79-A3ARKHYKU9")
                    #print('command:',command)
                    res = client.query(command)
                    answer = next(res.results).text
                    #print(answer)

                    #print("IN WIKI")
                    talkToMe(answer)
                    #talkToMe("improve your internet speed")

                except:

                    try:
                        #print(wikipedia.summary(command))
                        
                        print("IN WIKI")
                        talkToMe(wikipedia.summary(command))
                        #talkToMe("improve your internet speed")
                    except:
                        talkToMe("Even internet has no answer about it.")
            else:
                talkToMe("OK, ask me some thing else")

        else:
            talkToMe(answer)


now = datetime.datetime.now()
hr=now.hour
#print(hr)

if (hr < 12):
    #print("Good moring. Have a nice day")
    talkToMe("Good moring. Have a nice day!")
elif (hr >= 12 and hr < 17):
    #print("Good afternoon")
    talkToMe("Good afternoon!")
elif (hr >= 17 and hr <= 24):
    #print("Good Evening")
    talkToMe("Good Evening!")

#talkToMe('Hello')

#loop to continue executing multiple commands
def start():
    while True:
        #assistant(myCommand())
        assistant(typeCommand())
start()