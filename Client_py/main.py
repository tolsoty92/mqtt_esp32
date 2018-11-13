from time import sleep
import paho.mqtt.client as mqtt  # import the client1
from concurrent.futures import ThreadPoolExecutor
from Lib.func_module import  *
import cv2.aruco as aruco
import cv2
import numpy as np
from Lib.aruco_tools import *

# CV initilization
stream = cv2.VideoCapture(0)
width = 640
height = 480
stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)

parameters = aruco.DetectorParameters_create()
font = cv2.FONT_HERSHEY_SIMPLEX

camera_params = np.load("405(640x480).npz")

newcameramtx = camera_params["newcameramtx"]
roi = camera_params["roi"]
mtx = camera_params["mtx"]
dist = camera_params["dist"]
rvecs = camera_params["rvecs"]
tvecs = camera_params["tvecs"]

RUN = True
dst_pt = (-1, -1)
CHECKPOINT = True


# MQTT initialization
SERVER_IP = "192.168.0.121"
PORT = 1883
PLATFORMS_SET = {5,}
FEEDBACK_TOPIC = "esp32/feedback/+"
CONNECTON_TOPIC = "Connected"
MSG_TOPIC = "esp32/"

NUMBER_OF_CLIENTS = 1

MAX_WORKERS = 10
WORKER_TIME = 0.1
MESSAGES_QOS = 2

client = mqtt.Client("")

RUN = True

if __name__== "__main__":
    client = mqtt.Client("BOSS")
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    start_connection_client(client, SERVER_IP, PORT, CONNECTON_TOPIC)
    client.subscribe(FEEDBACK_TOPIC, qos=MESSAGES_QOS)
    client.loop(WORKER_TIME)
    while RUN:
        # client.loop(WORKER_TIME)
        ret, img = stream.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if CHECKPOINT:
            dst_pt = generate_dst_pt(width, height)
            CHECKPOINT = False

        draw_dst_pt(img, dst_pt)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if np.all(ids != None):
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)  # Estimate pose of each marker
            for id in ids:
                direction_point, cntr = detect_direction(corners[0])
                CHECKPOINT = is_it_checkpoint(cntr, dst_pt)
                direction_point = find_direction_point(direction_point, cntr)
                abs_error_angle = find_angle_error(direction_point, cntr, dst_pt)
                error_angle = find_angle_direction(direction_point, cntr, dst_pt, abs_error_angle)
                cv2.line(img, direction_point, direction_point, (150, 0, 255), 1)
                cv2.line(img, cntr, dst_pt, (30, 255, 15), 1)
                cv2.line(img, cntr, direction_point, (250, 180, 140), 2)
                cv2.circle(img, direction_point, 1, (200, 55, 255), 15, cv2.LINE_8)
                cv2.putText(img, str(error_angle), (25, 25), font, 0.5, (255, 255, 200), 2)
                if abs(error_angle) > 10:
                    send_angle(client, id, MSG_TOPIC, angle=error_angle, qos=MESSAGES_QOS)
                    error_angle = -1
                strg = ''
            for i in range(0, ids.size):
                strg += str(ids[i][0]) + ', '
            cv2.putText(img, "Id: " + strg, (0, 64), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "No Ids", (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('img', img)
        if cv2.waitKey(100) & 0xFF == 27:
            RUN = not RUN

    stream.release()
    cv2.destroyAllWindows()