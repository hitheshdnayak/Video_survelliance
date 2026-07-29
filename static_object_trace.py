import cv2
import numpy as np
from ultralytics import YOLO
from color_finder import *
import webcolors

def IOU_check(box1,box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)
    inter_width = max(0, inter_x_max - inter_x_min)
    inter_height = max(0, inter_y_max - inter_y_min)
    inter_area = inter_width * inter_height
    
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    
    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area if union_area != 0 else 0

    return iou >= 0.95

def check_obj_presence(frame,key_box,model):
    results = model(frame)
    boxes = results[0].boxes.xyxy
    for box in boxes:
        box = [int(box[0]),int(box[1]),int(box[2]),int(box[3])]
        if(IOU_check(box,key_box)):
            return True
    return False

def binary_search(cap,bb,l,h,model):
    m=int((l+h)/2)
    print(m)
    
    if(abs(h-l) < 20):
        return m
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, m)
    ret,frame = cap.read()
    if(check_obj_presence(frame,bb,model)):
        return binary_search(cap,bb,m,h,model)
    else:
        return binary_search(cap,bb,l,m,model)

    
def crop_and_save_video(cap,start_frame,last_frame,output_path):
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use other codecs, e.g., 'XVID'
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    current_frame = start_frame
    
    while(current_frame<last_frame):
        ret, frame = cap.read()
        if ret:
            out.write(frame)

            current_frame += 1
        else:
            break
    out.release()
    
    
def static_trace(input_video,
                 output_path,
                 query,
                 thumbnailpath = 'C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\thumbnails2\\'
                 ):

    cap = cv2.VideoCapture(input_video)

    again = True
    frame=0
    start_frame = 0
    user_color_d = query.split(' ')
    user_color = []
    for color in user_color_d:
        rgb_value = webcolors.name_to_rgb(color)
        # Extract red, green, and blue components
        red = rgb_value.red
        green = rgb_value.green
        blue = rgb_value.blue
        user_color.append([red,green,blue])
    while(again):
        time = input("input the time in hrs:min:sec  ->  ")
        time_split = time.split(':')

        hrs = int(time_split[0])
        mins = int(time_split[1])
        sec = int(time_split[2])
        total_sec = hrs*3600 + mins*60 +sec
        # print("lap1")
        fps = cap.get(cv2.CAP_PROP_FPS)
        start_frame = int(fps * total_sec)
        # print("lap2")
        # print(hrs)
        # print(mins)
        # print(sec)
        # print(total_sec)
        # print(fps)
        # print(start_frame)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        # print("lap3")
        ret,frame = cap.read()
        # print("lap4")
        # print(ret)
        cv2.imshow('Frame',frame)
        # print("lap5")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        choice = input("is the image containing the object (y or n) : ")
        if(choice == 'y'):
            again = False
    
    #creating model from pretrained weights
    model = YOLO("C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\yolov8m.pt")
    results = model(frame)
    # print(results[0].boxes)
    
    for i in range(0,len(results[0].boxes.cls)):
        # print(results[0].boxes.cls[i])
        # print(results[0].boxes.xyxy[i])
        xyxy = results[0].boxes.xyxy[i]
        # print(xyxy)
        thumbnail = frame[int(xyxy[1]):int(xyxy[3]), int(xyxy[0]):int(xyxy[2])]
        # if(detect_color_in_bboxes(thumbnail, user_color)):  # comment and un-comment for using the query filter for color
        #     cv2.imwrite(thumbnailpath + str(i) + ".jpg", thumbnail)
        cv2.imwrite(thumbnailpath + str(i) + ".jpg", thumbnail)
    
    #taking in input of what object to track in form of number
    obj_id = input("enter the object id from the thumbnails2 folder : ")
    # print(type(obj_id)) 
    obj_bb = results[0].boxes.xyxy[int(obj_id)]
    obj_bb = [int(obj_bb[0]),int(obj_bb[1]),int(obj_bb[2]),int(obj_bb[3])]
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("total_frames = "+str(total_frames))
    last_frame = binary_search(cap,obj_bb,start_frame,total_frames,model)
    last_frame = min(total_frames,last_frame)
    
    #cropping the video between start and last frame and saving in output_path
    crop_and_save_video(cap,start_frame,last_frame,output_path)
    
    cap.release()
    print("the result is saved in static_trace.mp4")
    
if __name__ == "__main__":
    input_vid = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\vid9.mp4"
    output_vid = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\static_trace.mp4"
    static_trace(input_vid,output_vid,"white bag")