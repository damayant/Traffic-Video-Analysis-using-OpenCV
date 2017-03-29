import cv2
from projectutils import play_video,count_cars

video_file = '../Dataset/traffic1.avi' #ground truth 8
window_name= "Target Video" 
#play_video(video_file,25,window_name)
#count_cars(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name)
count_cars(video_file,50,0,0,0,0,0,0,window_name)