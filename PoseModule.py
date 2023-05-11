import cv2
from PIL import Image,ImageTk
from tkinter import *
import tkinter.filedialog as fd
import mediapipe as mp
from math import sqrt
class PoseDetector:
    def __init__(self, mode=False, smooth=True,
        detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,smooth_landmarks=self.smooth,
                                    min_detection_confidence=self.detectionCon,
                                    min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True, bboxWithHands=False):
        self.lmList = []
        self.bboxInfo = {}
        self.extra_feature=None
        if self.results.pose_landmarks:
             for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    self.lmList.append([id, cx, cy, cz])
             ad = abs(self.lmList[12][1] - self.lmList[11][1]) // 2
             if bboxWithHands:
                 x1 = self.lmList[16][1] - ad
                 x2 = self.lmList[15][1] + ad
             else:
                x1 = self.lmList[12][1] - ad
                x2 = self.lmList[11][1] + ad
             y2 = self.lmList[29][2] + ad
             y1 = self.lmList[1][2] - ad
             bbox = (x1, y1, x2 - x1, y2 - y1)
             cx, cy = bbox[0] + (bbox[2] // 2), \
             bbox[1] + bbox[3] // 2
             self.bboxInfo = {"bbox": bbox, "center": (cx, cy)}
             if draw:
                cv2.rectangle(img, bbox, (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
             neck_x = int((self.lmList[12][1] + self.lmList[11][1]) / 2)
             neck_y = int((self.lmList[12][2] + self.lmList[11][2]) / 2)
             self.extra_feature = (neck_x, neck_y)
             cv2.circle(img, self.extra_feature, 5, (0, 255, 0), cv2.FILLED)
        return self.lmList, self.bboxInfo,self.extra_feature


class Pushup:
    def __init__(self):
        self.count = 0
        self.position = None

    def detect(self, lmlist):
        if len(lmlist) != 0:
            if lmlist[12][2] > lmlist[14][2] and lmlist[11][2] > lmlist[13][2] and lmlist[12][2] > lmlist[26][2] and lmlist[24][2]>lmlist[26][2] and lmlist[23][2]>lmlist[25][2]:
                self.position = 'Up'
            if lmlist[12][2] <= lmlist[14][2] and lmlist[11][2] <= lmlist[13][2] and lmlist[11][2] <= lmlist[25][2] and lmlist[24][2]<=lmlist[26][2] and lmlist[23][2]<=lmlist[25][2] and self.position == 'Up':
                self.position = 'Down'
                self.count += 1
        return self.count