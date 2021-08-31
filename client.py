import socket
from colorama import Fore, Back, Style
 # import Python Open Weather Map to our project.


CONNECT = input("Please provide the IP adress:") # provide the cleint with the server and port number info
PORT = int(input("Please provide the port number:"))


print(CONNECT)



clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the socket 
clientSocket.connect((CONNECT,PORT)) # bind the IP address and the port number
while True: 
    
    try:
        sentence  = input("Please select a command by entering the approiate number- \n1.temperature today \n2.should I go out \n3.close the server\n4.chage the location\n5.what is you location?----------:")

        if(sentence!="1" and sentence!= "2" and  sentence!= "3" and sentence!="4"and sentence!="5" ): # if an invalid option is selected show the error
            print("invalid command!! select either- weather today?, should I got out?, close")
            continue;
        if(sentence == "5"):  # ask for the location
            clientSocket.send(sentence.encode()) # standard send the option to the server and then accept the server's response
            print(Fore.BLUE+clientSocket.recv(1024).decode())
            print(Style.RESET_ALL)
            print("")
       
        if(sentence == "4"): # option 4 tell the server to change the location of your choice
            clientSocket.send(sentence.encode())
            change = input("what location would you like to chage to?  ")
        
        
            clientSocket.send(change.encode()) 
            modSentence2 = clientSocket.recv(1024).decode();
            
            if(modSentence2 == "invalid"): # if the server returns invalid that means that something went wrong and the client just need to go to the top of the loop.
                print(Fore.RED+"invalid input try again!")
                print("")
                print(Style.RESET_ALL)
                continue
            print(Fore.BLUE+"your location has been changed to:"+modSentence2) # recieve the info about the new location and then print
            print(Style.RESET_ALL)
            print("")       
      
        if(sentence == "3"): # this option is meant to close the server. So if the server is closed break out of the loop as the client behavior will stop as well
            print(sentence)
            clientSocket.send(sentence.encode()) 
           
            print()
            break;

        if(sentence == "2"): # if the option is 2 recieve the question of threshhold
            clientSocket.send(sentence.encode())
            modSentence = clientSocket.recv(1024)
            if(modSentence == "invalid"): # same as case 4 
                print("invalid input try again!")
                continue
            
            resp = input(modSentence.decode())
        
        

            
            #if()# provide the threshold info
            clientSocket.send(resp.encode())
            print(Fore.BLUE+clientSocket.recv(1024).decode()) # recive the response weather the user should go out or not from the server
            print(Style.RESET_ALL)
            print("")
    

        
        resp = None;
        if(sentence == "1"): # option 1 just recieve the info about the weather today and display it to the user
            clientSocket.send(sentence.encode())
            print(Fore.BLUE+clientSocket.recv(1024).decode())
            print(Style.RESET_ALL)
            print("")
    except ConnectionResetError as e:
        print(type(e))
        print(Fore.BLUE+"the server is closed")
        print(Style.RESET_ALL)
        break
    

clientSocket.close()



