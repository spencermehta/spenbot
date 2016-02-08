import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import random
import config
import time
import datetime


#Twitch IRC connection
server = "irc.twitch.tv"
irc = socket.socket()
irc.connect((server, 6667))

irc.send(bytes("PASS " + config.password + "\r\n", 'utf-8'))
irc.send(bytes("USER " + config.nick + " 0 * :" + config.bot_owner + "\r\n", 'utf-8'))
irc.send(bytes("NICK " + config.nick + "\r\n", 'utf-8'))
irc.send(bytes("JOIN " + config.channel + "\r\n", 'utf-8'))



#Sends messages to irc
def message(msg):
    global queue
    queue += 1
    if queue < 20:
        irc.send(bytes("PRIVMSG " + config.channel + " :" + msg + "\r\n", 'utf-8'))
    else:
        print("Spamming. Message not sent")



#Prevent IP ban for spam
def queuetimer():
    global queue
    queue = 0
    threading.Timer(30,queuetimer).start()
queuetimer()



while True:
    #Output from irc
    try:
        twitchdata = irc.recv(1204)
        twitchdata = twitchdata.decode()
        data = twitchdata.split(":")[1]
        
        twitchuser = data.split("!")[0]
        twitchmsg = twitchdata.split(":")[2]
        twitchmsg = twitchmsg.lower()
        twitchmsg = twitchmsg.strip("\r\n")

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        
        chat = date + " " + twitchuser + ": " + twitchmsg + "\n"
        chatlog = open("chatlog.txt", "a")
        chatlog.write(chat)
        
        chat = "\033[1;44;40m" + date + "\033[1;32;40m " + twitchuser +": \033[0;37;40m"+ twitchmsg
        print(chat)

    
    
        if twitchdata.find("PING") != -1:
            irc.send(twitchdata.replace("PING", "PONG")) #responds to PINGS from the server
    
        if "!twitter" in twitchmsg: 
            msg = "Twitter - twitter.com/spencermehta"
            message(msg)
            print("\033[1;31;40m" + msg + "\033[0;37;40m")
            
        elif "!youtube" in twitchmsg :
            msg = "Youtube - youtube.com/spencermehta"
            message(msg)
            print("\033[1;31;40m" + msg + "\033[0;37;40m")
            
        elif "!github" in twitchmsg:
            msg = "Github - github.com/spencermehta"
            message(msg)
            print("\033[1;31;40m" + msg + "\033[0;37;40m")

    except Exception as e:
        print("Error: ", e)
