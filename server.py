
import random
import socket
import _thread
import datetime
import requests
import json # the red lines under requests and json are a text editor issue and has got nothing to do with the python. The code is still functional and runs effortlessly
import math
     
i = 0 # count the number of threads

print("Starting......") 

#PORT = 5050
#print(socket.gethostbyname(socket.gethostname())) use this statement to know the IP adress of your computer
SERVER = input("what IP adress do you want to use? You can use the loop back adress or the computer's IP adress: ") # the user can choose from either the computer's IP adress or the loop back address
PORT =  int(input("what PORT are you using? "))  # the user also needs to provide the PORT number
datetime_object = datetime.datetime.now() # timestamp
print(datetime_object, end = '') # 
print(" server:"+SERVER+" PORT:"+str(PORT)) # print the timestamp, IP adress and the port number 
#SERVER = socket.gethostname()

ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # intializing the server

#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((SERVER,PORT)) # bind the IP address and the port number

server.listen(1) 

i = 0

def weatherCon(val): #  this function coverts the kelivn value provided by the API into celcius
    val = val-273
    val = val*(9/5)+32    
    return math.trunc(val)

def handler(connectionSocket, addr, server, thread_val): # the handler function contains the interaction with the client because each client will be passed as a thread to this function
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?" # use the openweatherAPI to get th weather info
    CITY = "Columbus"
    API_KEY = "7fc3e5205355ee68b66f96c556954d76"
    # upadting the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    

    response = requests.get(URL) 
    data = response.json() # get the json object
  

    print("-----------------------------------")
    
    while True:
        sentence = connectionSocket.recv(1024).decode() # keep the loop running untill a breaking condition hasn't been met
        print(sentence)
        temporary  = data;
        if(sentence == "1"): # option 1 to look up the wather today 
            #e= new Exception("testing type error!")   
               
            val=data['main']['temp'] # traverse the json obeject to get the temperature on that day 
            temp = weatherCon(val)

            send = str(temp)
        
            print(send)
            connectionSocket.send(send.encode() ) # encode the sending value and send it to the client 
         
               
              
               
          
        if(sentence == "2"): # option 2 to find out if someone should go out or not based on a threhold value provided by the client.
            try:
                resp = "what is threshhold? "
                connectionSocket.send(resp.encode()) # send the sentence "what is the threshold to the client"
                get_back = connectionSocket.recv(1024).decode() 
            
                thresh = int(get_back) # recieve the threshold value from the client 
                print(get_back)
                if(thresh <= weatherCon(data['main']['temp'])): # if the weather today is more than the threshold then go outside
                    resp = "yes it is a good day!!"
                else:
                    resp = "ehhh... it migh not be a good idea" # else don't
                    
                
            
                connectionSocket.send(resp.encode()) # send the response to the client 
            except Exception as e:   # try cach block to catch invalid input errors
                print("something went wrong try again with proper values")
                giving = "invalid";
                connectionSocket.send(giving.encode())
                continue
                
                
        if sentence == "3": # option 3 will close the break the loop and also exit out of the thread

            print("Exiting Server")
            connectionSocket.close() 
            server.close()
            break
        
       
        if sentence == "4": # option 4 will get the json data again from the API based on the new location
            try:   
                get_back = connectionSocket.recv(1024).decode()
                print(get_back)
                BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
                CITY = get_back
                API_KEY = "7fc3e5205355ee68b66f96c556954d76"
                # upadting the URL
                URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
                response = requests.get(URL)
                data = response.json()
                resp = (data['name'])
                connectionSocket.send(resp.encode()) # send the new location to the client as well
                print(data)
            except Exception as e:  # try catch block to handle erros with invalid city names
                giving = "invalid"
                print("something went wrong! propably wrong city name. try again")
                data = temporary    # temporary stores the old json object which needs to be assigned if there is an execption to reinitialize data
                connectionSocket.send(giving.encode());
                continue
            
        if sentence == "5": # option 5 just lets the client know about their current location
            print(data['name'])
            resp = data['name']
            connectionSocket.send(resp.encode())
            
      
while True: # keep on clreating threads
 
    try: # the try catch block will catch an execption if the serer has been closed and another client tries to close it.
        connectionSocket, addr = server.accept()
        _thread.start_new_thread(handler,(connectionSocket,addr,server,i)) # try catch block because 
        i = i+1
    except OSError as e:
        print("server closed........")
        
        break
        


  


  