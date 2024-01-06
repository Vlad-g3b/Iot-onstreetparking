import cv2
import numpy as np
from ultralytics import YOLO


model = YOLO("yolov8s.pt")

model.train(model="yolov8s.pt", data="/home/vlad/Dev/Iot/AiCarDetection/datasets/yolo/data.yaml" ,epochs=100)