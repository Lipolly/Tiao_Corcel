import cv2
import numpy as np
def procuraCONE(cap):
  while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
      hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      lower_orange1 = np.array([0, 60, 80])
      lower_orange2 = np.array([10, 255, 255])
      ##upper_orange1 = np.array([0, 60, 80])
      ##upper_orange2 = np.array([10, 255, 255])


      ##imgThreshHigh = cv2.inRange(hsv_img, upper_orange1, upper_orange2)
      imgThreshLow = cv2.inRange(hsv_img, lower_orange1, lower_orange2)
      kernel = np.ones((5,5),np.uint8)
    
      edges_img = cv2.morphologyEx(imgThreshLow, cv2.MORPH_OPEN, kernel)
 
      contours, _ = cv2.findContours(edges_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      font = cv2.FONT_HERSHEY_SIMPLEX
      fontScale = 2
      fontColor = (0, 0, 255)
      lineType = 2
      cones = []
      for cnt in contours:
          boundingRect = cv2.boundingRect(cnt)
          approx = cv2.approxPolyDP(cnt, 0.06 * cv2.arcLength(cnt, True), True)
          if len(approx) == 3:
              x, y, w, h = cv2.boundingRect(approx)
              cones.append({'x':x, 'y': y, 'w': w, 'h': h})
              rect = (x, y, w, h)
              cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
              bottomLeftCornerOfText = (x, y)
              cv2.putText(frame,'traffic_cone', 
                  bottomLeftCornerOfText, 
                  font, 
                  fontScale,
                  fontColor,
                  lineType)
      cv2.imshow('Frame',frame)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break
      return cones
    else: 
      break
      
if __name__ == '__main__':
  cap = cv2.VideoCapture(0)
  
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
  cap.set(cv2.CAP_PROP_BRIGHTNESS, -34)
  cap.set(cv2.CAP_PROP_CONTRAST, 29)
  cap.set(cv2.CAP_PROP_SATURATION, 128)
  cap.set(cv2.CAP_PROP_GAIN, 54)
  cap.set(cv2.CAP_PROP_EXPOSURE, 157)
  cap.set(cv2.CAP_PROP_SHARPNESS, 3)
  cap.set(cv2.CAP_PROP_AUTO_WB, 0)
  cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4204)
  cap.set(cv2.CAP_PROP_HUE, 8)

  while(1):
    cones = procuraCONE(cap)
    print(cones)
    
