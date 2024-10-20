import socket

import threading

import rsa

public_key, private_key = rsa.newkeys(2048)
public_partner = None

choice = input("Do you want to host or (1) or to connect (2): ")

if choice == "1": 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.79", 9999))
    server.listen()

    client, _ =server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(2048))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.79", 9999))  # Also fixed the connect argument, should be a tuple.
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(2048))
    client.send(public_key.save_pkcs1("PEM"))
    
else:
    exit()



def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)


def recieving_messages(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(2048), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=recieving_messages, args=(client,)).start()
