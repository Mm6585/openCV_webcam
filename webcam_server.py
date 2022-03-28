import socket
import numpy
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 2608
INDEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

print('PORT = ' + str(UDP_PORT))

while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    n = INDEX.index(data[0])
    s[n] = data[1:46081]

    if n == 19:
        for i in range(20):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(480, 640, 3)
        out.write(frame)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

