import cv2
import numpy as np

#To display the target video
def play_video(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name):
	
	cv2.namedWindow(display_window_name)
	cap = cv2.VideoCapture(video_file)
	while(cap.isOpened()):
		#reading frame by frame
		ret, frame = cap.read()

		cv2.imshow(display_window_name,frame)

		#Video stops playing if 'q' or escapse is pressed
		#Change the frame rate according to application
		if cv2.waitKey(25) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()


#This function will count the total number of cars in the video
def count_cars(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name):
	target_row =  600
	cv2.namedWindow(display_window_name)
	cap = cv2.VideoCapture(video_file)
	reference_frame = None
	image_area = None
	fgbg = cv2.createBackgroundSubtractorMOG2()

	ret, ref_frame = cap.read()
	ref_frame = ref_frame[:,500:1100,:]
	image_area = ref_frame.shape[0] * ref_frame.shape[1]

	while(cap.isOpened()):
		#reading frame by frame
		ret, frame = cap.read()

		if ret is False:
			exit()

		frame = frame[:,500:1100,:]

		#frame = cv2.line(frame,(100,650),(600,600),(255,0,255),5)
		frame = cv2.line(frame,(100,600),(600,600),(0,0,255),1)
		frame = cv2.line(frame,(100,550),(600,550),(0,0,255),1)
		frame = np.array(frame,dtype='uint8')
		

		#Getting the reference frame
		if ret is not None and reference_frame is None:
			reference_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			reference_frame = cv2.GaussianBlur(reference_frame,(29,29),0)
			image_area = frame.shape[0] * frame.shape[1]
			continue
	
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#blurring each frame :: to aid in contour detection
		blurred = cv2.GaussianBlur(gray,(29,29),0)

		#finding the difference in frames
		delta = cv2.absdiff(reference_frame, blurred)
		
		ret1, thresh = cv2.threshold(delta,30,255,cv2.THRESH_BINARY)
		#dilate is done to close the small holes in the image
		thresh = cv2.dilate(thresh, None, iterations=5)
		cv2.imshow("Thresholded",thresh)
		#cv2.waitKey(0)
		
		

		'''
		fgmask = fgbg.apply(frame)
		ff = cv2.medianBlur(fgmask,7)
		ret1, thresh = cv2.threshold(ff,128,255,cv2.THRESH_BINARY)


		cv2.imshow("Thresholded",thresh)
		#cv2.waitKey(0)
		'''

		#Detecting contours

		(_,cnt,_) = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
		for contour in cnt:
			#need to find a suitable area range to filter the contours
			contour_area = cv2.contourArea(contour)
			if (contour_area >0.009 * image_area) and  (contour_area <0.10* image_area):
				
				### Moments are required to calculate the center point ###
				M = cv2.moments(contour)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.circle(frame, (cX, cY), 1, (255,111,251), 1)
				### The center point will be used to count the cars #######
				(x,y,w,h) = cv2.boundingRect(contour)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)



				#cv2.drawContours(frame,cnt,-1,(0,255,0),3)
				cv2.imshow(display_window_name,frame)

				#### Include the logic of line crossing ###########	
				#### Logic 1 : Count the number of Color dots crossing the line
				'''
				line_check_array = frame[600,100:600,:]
				cv2.imshow("line",line_check_array)
				for  i in range(line_check_array.shape[0]):
					for j in range(line_check_array.shape[1]):
						x = line_check_array[i,j,:]
						if x[0] == 255 and x[1]==111 and x[2] == 251:
							print "Hello"
				'''

		#Video stops playing if 'q' or escapse is pressed
		#Change the frame rate according to application
		if cv2.waitKey(25) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
