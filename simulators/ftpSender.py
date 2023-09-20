import socket

def main():


    try:

        # intiliaze the socket and send send the file
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 21))

        file = open('sample.txt', 'rb')        

        # set name of file on the receiver side 
        client.send("transfered_doc.pdf".encode())

        data = file.read()
        client.sendall(data)
        client.send(b"<END>")

        file.close()
        client.close()

    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()