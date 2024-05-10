import cv2
import cv2.aruco as aruco
from servo import dropLoad
import socket
import threading
import base64

# Network settings (replace with your IP address and port)
HOST = '192.168.108.42'  # Replace with your local machine's IP address
PORT = 8000

# Aruco parameters
marker_size = 6
total_markers = 250

def findAruco(img):
    """Detects Aruco markers in the image and performs actions."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, _ = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    if ids is not None:
        for id in ids:
            print(f"Marker ID: {id[0]}")
            if id[0] == 69:
                dropLoad()
                print("Payload Drop Successful!")
                break  # Exit loop after successful drop

    # No need to draw markers for streaming, comment out if desired
    # aruco.drawDetectedMarkers(img, bbox, ids)

    return bbox, ids

def video_stream():
    """Captures video frames, detects Aruco markers, and sends frames to the network."""
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Failed to capture frame from the camera.")
            break

        _, _ = findAruco(img.copy())  # Detect markers without drawing

        # Encode frame as JPEG for efficient streaming
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        # Send encoded frame over network
        conn.sendall(b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if cv2.waitKey(1) == 113:
            break

    cap.release()

def handle_client(conn, addr):
    """Handles communication with a connected client."""
    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            # Process data from client (if applicable)
        except socket.error as e:
            print(f"Client {addr} error: {e}")
            break

    conn.close()
    print(f"Client {addr} disconnected")

def start_server():
    """Creates a socket server for streaming video."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server listening on {HOST}:{PORT}")
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    video_stream()
