import cv2
import numpy as np
from ultralytics import YOLO
from query_processor import *

class_map = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
    6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant',
    11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
    16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
    22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
    27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
    32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
    36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
    40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
    57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet',
    62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
    67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
    72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors',
    77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}

# Create a new dictionary with keys and values interchanged
class_map = {v: k for k, v in class_map.items()}

def convert_to_list(input_video):
    cap  = cv2.VideoCapture(input_video)
    count = 0
    l = []
    while(True):
        ret,frame = cap.read()
        if(not(ret)):
            break
        if(count%30):
            l.append(frame)

    return l

'''
0: 'person',
1: 'bicycle',
2: 'car',
3: 'motorcycle',
4: 'airplane', 
5: 'bus', 
6: 'train', 
7: 'truck', 
8: 'boat', 
9: 'traffic light', 
10: 'fire hydrant', 
11: 'stop sign', 
12: 'parking meter', 
13: 'bench', 
14: 'bird', 
15: 'cat', 
16: 'dog', 
17: 'horse', 
18: 'sheep', 
19: 'cow', 
20: 'elephant', 
21: 'bear', 
22: 'zebra', 
23: 'giraffe', 
24: 'backpack', 
25: 'umbrella', 
26: 'handbag', 
27: 'tie', 
28: 'suitcase', 
29: 'frisbee', 
30: 'skis', 
31: 'snowboard', 
32: 'sports ball', 
33: 'kite', 
34: 'baseball bat', 
35: 'baseball glove', 
36: 'skateboard', 
37: 'surfboard', 
38: 'tennis racket', 
39: 'bottle', 
40: 'wine glass', 
41: 'cup', 
42: 'fork', 
43: 'knife', 
44: 'spoon', 
45: 'bowl', 
46: 'banana', 
47: 'apple', 
48: 'sandwich', 
49: 'orange', 
50: 'broccoli', 
51: 'carrot', 
52: 'hot dog', 
53: 'pizza', 
54: 'donut', 
55: 'cake', 
56: 'chair', 
57: 'couch', 
58: 'potted plant', 
59: 'bed', 
60: 'dining table', 
61: 'toilet', 
62: 'tv', 
63: 'laptop', 
64: 'mouse', 
65: 'remote', 
66: 'keyboard', 
67: 'cell phone', 
68: 'microwave', 
69: 'oven', 
70: 'toaster', 
71: 'sink', 
72: 'refrigerator', 
73: 'book', 
74: 'clock', 
75: 'vase', 
76: 'scissors', 
77: 'teddy bear', 
78: 'hair drier', 
79: 'toothbrush'
'''
def check_for_object(frame,model,query):
    results = model(frame)
    results = results[0]
    n_and_a = process_and_display(query)
    l2 = []
    for noun in n_and_a:
        oid = class_map[noun]
        l2.append([oid,n_and_a[noun]])


def binary_search(input_video,model,query):
    frames = convert_to_list(input_video)
    l=0
    h = len(frames)-1
    while(l<h):
        m = int((l+h)/2)
        bool_1 = check_for_object(frames[m],model,query)
        if(bool_1):
            l=m+1
        else:
            h=m-1
    