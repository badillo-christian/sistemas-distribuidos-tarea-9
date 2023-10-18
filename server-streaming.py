import cv2
import socket
import pickle
import struct

# Configuración del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8888))
server_socket.listen(10)

# Inicializar la cámara
cap = cv2.VideoCapture(0)

while True:
    client_socket, addr = server_socket.accept()
    print('Conexión desde: ', addr)
    
    if client_socket:
        while True:
            ret, frame = cap.read()
            data = pickle.dumps(frame)
            message_size = struct.pack("L", len(data))
            client_socket.sendall(message_size + data)
            
            # Para finalizar la transmisión, presionar 'q'
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break

cap.release()
