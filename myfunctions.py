import cv2
import numpy as np
from query_processor import *
from color_finder import *


def create_cropped_video(video_path, output_path, start_time, end_time):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    if(start_frame >end_frame) or (start_frame > int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) or (end_frame > int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) :
          return False

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.isOpened():
        ret_val, frame = cap.read()
        if not ret_val or cap.get(cv2.CAP_PROP_POS_FRAMES) > end_frame:
            break
        out.write(frame)
    cap.release()
    out.release()
    return True

def get_thumbnails(bytrack_txt):
    t = dict()
    trace = dict()
    file = open(bytrack_txt, "r")
    lines = file.readlines()
    for line in lines:
      line = line.strip()
      cols = line.split(',')
      key = cols[1]
      if(key not in t) or (t[key][6]<cols[6]):
        t[key] = cols
      if(key not in trace):
        trace[key] = [cols]
      else:
        trace[key].append(cols)
    return t,trace


def store_thumbnails_in_folder(video_path, thumbnails, path,user_color=[]):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None
    for thumbnail in thumbnails.values():
      x1 = float(thumbnail[2])
      y1 = float(thumbnail[3])
      x2 = float(thumbnail[4])
      y2 = float(thumbnail[5])
      key = thumbnail[1]

      cap.set(cv2.CAP_PROP_POS_FRAMES, int(thumbnail[0]))
      ret, frame = cap.read()
      if not ret:
          return None
      frame = frame[int(y1):int(y2), int(x1):int(x2)]
      # if(detect_color_in_bboxes(frame, user_color)):  # comment and un-comment for using the query filter for color
      #   cv2.imwrite(path + key + ".jpg", frame)
      cv2.imwrite(path + key + ".jpg", frame)
    cap.release()

def get_recording_of_person(video_path, trace_of_person, output_path):
  cap = cv2.VideoCapture(video_path)
  if not cap.isOpened():
      print("Error: Could not open video.")
      return None

  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  fps = cap.get(cv2.CAP_PROP_FPS)
  out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


  for detail in trace_of_person:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(detail[0]))
    ret, frame = cap.read()
    if not ret:
      break
    x1 = float(detail[2])
    y1 = float(detail[3])
    x2 = float(detail[4])
    y2 = float(detail[5])
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    out.write(frame)

  cap.release()
  out.release()
