import socket
import sys
from struct import *
import threading


HOST = "0.0.0.0"
PORT = 8888
MAX  = 100

DELIMETER = '\r\n'


def parse_data(buff):
    buff = buff.split(DELIMETER)
    filename = buff[0]
    keywords = buff[1:]

    return (filename, keywords)

def pack_data(filename, counts):
    buff = filename + DELIMETER

    for keyword, count in counts.iteritems():
        buff += keyword + DELIMETER
        buff += pack("!L", count) + DELIMETER

    return buff + DELIMETER

def process_data(client_socket):
    buffs = ''
    while 1:
        buffs += client_socket.recv(1024)
        if buffs.find('\r\n\r\n') != -1:
            break


    buffs = buffs.split("\r\n\r\n")
    buffs = buffs[:len(buffs)-1]

    all_buff = ''
    for buff in buffs:

        filename, keywords = parse_data(buff)

        counts = {}
        for keyword in keywords:
            counts[keyword] = 0

        file = open(filename)
        for line in file:
            line  = line.rstrip()

            for word in line.split():
                if word in keywords:
                    counts[word] += 1

        all_buff += pack_data(filename, counts)

    client_socket.sendall(all_buff)



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(sys.argv[1])
    server.bind((HOST, PORT))
    server.listen(MAX)

    while 1:
        client_socket, address = server.accept()
        threading.Thread(target=process_data, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
