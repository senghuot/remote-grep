import socket
import sys
from struct import *

HOST = "localhost"
PORT = 8081
DELIMETER = '\r\n'


def unpack_data(buff):
    buff = buff.split(DELIMETER)
    filename = buff[0]
    counts   = {}

    for i in range(1, len(buff), 2):
        keyword = buff[i]
        count = unpack("!I", buff[i+1])
        counts[keyword] = count[0]

    return filename, counts


def parse_arguments(argv):
    buff = ''
    for i in range(3, len(argv), 1):
        if argv[i] == 'file':
            i += 1
            buff += argv[i] + DELIMETER

            for j in range(i+1, len(argv), 1):
                if argv[j] != 'file':
                    buff += argv[j] + DELIMETER
                else:
                    i = j - 1
                    break

            buff += DELIMETER

    return buff


def main():

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    buff = parse_arguments(sys.argv)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(buff)

    buffs = client_socket.recv(1024)
    buffs = buffs.split("\r\n\r\n")
    buffs = buffs[:len(buffs)-1]


    for buff in buffs:
        filename, counts = unpack_data(buff)

        print "File: %s" %(filename)
        for keyword, count in counts.iteritems():
            print "  %s: %d" %(keyword, count)



if __name__ == "__main__":
    main()