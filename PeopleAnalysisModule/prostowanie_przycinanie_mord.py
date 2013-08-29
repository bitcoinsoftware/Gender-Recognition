import sys, math, Image, os
import cv , cv2
 
def odleglosc(ob1,ob_ref):
    odl_x , odl_y = ob_ref[0][0]-ob1[0][0] , ob_ref[0][1]-ob1[0][1] 
    if odl_x<0:odl_x=-odl_x
    if odl_y<0:odl_y=-odl_y
    return odl_x+odl_y
    
    
def Detect_face_and_eyes(img_src):
  imcolor = cv.LoadImage(img_src) # input image
  # loading the classifiers
 # haarFace = cv.Load('./haarcascades/haarcascade_frontalface_default.xml')
  haarEyes = cv.Load('./haarcascades/haarcascade_mcs_righteye.xml')
  haarMouth = cv.Load('./haarcascades/haarcascade_mcs_mouth.xml')
  # running the classifiers
  storage = cv.CreateMemStorage()
  detectedMouth = cv.HaarDetectObjects(imcolor,  haarMouth, storage)
  detectedEyes = cv.HaarDetectObjects(imcolor, haarEyes, storage)
  
  if len(detectedEyes)<2:
      haarEyes = cv.Load('./haarcascades/haarcascade_eye.xml')
      detectedEyes = cv.HaarDetectObjects(imcolor, haarEyes, storage)

  
  if detectedEyes: #lewe oko jest pierwsze
   for eye in detectedEyes:
    cv.Rectangle(imcolor,(eye[0][0],eye[0][1]),(eye[0][0]+eye[0][2],eye[0][1]+eye[0][3]),cv.RGB(155, 55, 200),2)
    
  cv.NamedWindow('Face Detection', cv.CV_WINDOW_AUTOSIZE)
  cv.ShowImage('Face Detection', imcolor) 
  cv.WaitKey()
  print detectedEyes
  return detectedEyes
  
def Sort_detected(detected):
  n = len(detected)
  if n==2:return detected
  while n>1:
    for i in range(n-1):
      if detected[i][1] > detected[i+1][1]:
        detected[i], detected[i+1] =detected[i+1], detected[i]
    n = n-1
  return detected

def Change_to_gray_scale(image,size):
  new32F = cv.CreateImage (size, cv.IPL_DEPTH_32F, 1)
  print type(image)
  cv.CvtColor(image,new32F,cv.CV_RGB2GRAY)
  return new32F
  
def grayscale(image):
    image =image.convert("L")
    return image

def Distance(p1,p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  return math.sqrt(dx*dx+dy*dy)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
  if (scale is None) and (center is None):
    return image.rotate(angle=angle, resample=resample)
  nx,ny = x,y = center
  sx=sy=1.0
  if new_center:
    (nx,ny) = new_center
  if scale:
    (sx,sy) = (scale, scale)
  cosine = math.cos(angle)
  sine = math.sin(angle)
  a = cosine/sx
  b = sine/sx
  c = x-nx*a-ny*b
  d = -sine/sy
  e = cosine/sy
  f = y-nx*d-ny*e
  return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
  # calculate offsets in original image
  offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # get the direction
  eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # calc rotation angle in radians
  rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # distance between them
  dist = Distance(eye_left, eye_right)
  # calculate the reference eye-width
  reference = dest_sz[0] - 2.0*offset_h
  # scale factor
  scale = float(dist)/float(reference)
  # rotate original around the left eye
  image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # crop the rotated image
  crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # resize it
  image = image.resize(dest_sz, Image.ANTIALIAS)
  image = grayscale(image)
  return image
  
  #92x112

  
if __name__ == "__main__":
  folder_src= "./training_photos/mezczyzni/"
  #"./zdjecia/testowe/"
  for file_name in os.listdir(folder_src):
    #image_name = "./s45/2.pgm
    #file_name = "4.pgm"
    image_name = folder_src+file_name
    size= (92,112)
    offset_pct=(0.35,0.35)
    image =  Image.open(image_name)
    #output_image_name="."+image_name.split(".")[1]+"cropped.pgm"
    output_image_name = image_name
    detection_output = Detect_face_and_eyes(image_name)
    if len(detection_output)>1:
        p_oko, l_oko = detection_output[0],detection_output[1]
        print p_oko, l_oko
        sr_l_o , sr_p_o = (l_oko[0][0]+l_oko[0][2]/2 ,l_oko[0][1]+l_oko[0][3]/2 ), (p_oko[0][0]+p_oko[0][2]/2 ,p_oko[0][1]+p_oko[0][3]/2)
    
        if sr_p_o[0]<sr_l_o[0]: #jesli jednak prawe oko jest zapisane jako pierwsze to zmieniamy
            temp = sr_l_o 
            sr_l_o = sr_p_o
            sr_p_o = temp
    
        CropFace(image, eye_left= sr_l_o, eye_right=sr_p_o, offset_pct=(0.35,0.35), dest_sz=size).save(output_image_name)
