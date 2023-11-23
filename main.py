import socket
import threading 

import rsa

public_key,private_key=rsa.newkeys(1024)
public_partner=None



choice = input("to host click (1), to connect click (2)")

if choice == "1":
    address1 = input("enter your ip address")
    server=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind((address1, 9999))
    server.listen()


    client, _ =server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner=rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice =="2":
    address2=input("enter the host ip address") 
    client=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    client.connect((address2, 9999))
    public_partner=rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()

def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(),public_partner))
        print("You: " + message)

def receiving_messages(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024),private_key).decode())


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()

