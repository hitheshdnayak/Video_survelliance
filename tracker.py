import cv2
import numpy as np
from myfunctions import *
from query_processor import *
from video_processor import *
from static_object_trace import *
import os
import shutil

def empty_folder(folder_path):
    # List all files and directories in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        try:
            # Check if it is a file and remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            # Check if it is a directory and remove it and its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def track(
    video_path, 
    start_time, 
    end_time, 
    query = '',
    bytetrack_txt = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\bytrack_text.txt",
    byproduct_video = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\byproduct.mp4",
    cropped_video = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\cropped.mp4",
    thumbnail_path = 'C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\thumbnails1\\',
    destination="C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\"
    ):
  
  #processing query
  # d = process_and_display(query)
  d = {'man':['white']}
  colors,color_values = get_only_human_color(d)
  print(d)
  print(colors)
  print(color_values)
  # image = cv2.imread("C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\thumbnails\\2.jpg")
  # print(detect_color_in_bboxes(image, color_values))
  # detect_color_in_bboxes(image, color_values)
  #crop the video based on start and end time in seconds
  if(create_cropped_video(video_path, cropped_video, start_time, end_time)): # returns true or false
    print("created cropped video")
  else:
    print("invlid time values")
    return 
  # uses yolov8 model and bytrack MOT to produce a trace of each person
  process_video(cropped_video,byproduct_video,bytetrack_txt)
  thumbnails,trace = get_thumbnails(bytetrack_txt)
  # print(thumbnails)
  # print(trace)
  
  store_thumbnails_in_folder(cropped_video, thumbnails, thumbnail_path,color_values)
  key = input(f"enter the person ID (only number) check in {thumbnail_path} ") ####################
  final_output_path =f'{destination}{key}.mp4'
  get_recording_of_person(cropped_video, trace[key], final_output_path)
  print(f"!! output moving trace saved in {key}.mp4 !!")


# Empty_folder_thumbnail_1_and_2
lfolder = ['C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\thumbnails1\\','C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\thumbnails2\\']
for folder_path in lfolder:
  empty_folder(folder_path)

# output_video_path = 'C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\static_trace.mp4'
choice = int(input("for static object track enter 0 and for moving object track enter 1 : "))
if(choice == 1):
  # input_video_path = 'C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\2_095_1.mp4'
  input_video_path = input("enter input video path : ")
  query  = input("enter the query : ")
  start_time = int(input("enter the start time : "))
  end_time = int(input("enter the end time : "))
  track(input_video_path,start_time,end_time,query)
  
elif(choice ==  0):
  # input_vid = "C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\vid9.mp4"
  # output_vid = 'C:\\Users\\HDN\\Desktop\\Video_survelliance\\obj_tra_2\\static_trace.mp4'
  input_video_path = input("enter input video path : ")
  output_video_path = input("enter output video path : ")
  query  = input("enter the query : ")
  static_trace(input_video_path,output_video_path,query)
  print("!! output static trace saved in static_trace.mp4")