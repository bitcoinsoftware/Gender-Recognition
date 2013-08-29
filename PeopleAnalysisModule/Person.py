import cv,  cv2 , os ,  time,  Image,  md5, random
from ImagesPreparer import *
   
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
 
class Person3:
    def __init__(self,  frame,  rect,  time_makes_difference=False):
        self.rect = rect ; self.time_makes_difference = time_makes_difference
        self.face_photo_valid = False
        self.face_size= [rect[2], rect[3]]
        self.personID=-1
        self.white_level = 6
        try:
            sub_image = cv.GetSubRect(frame,  rect)
        except:
            return None
        self.frame_copy = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, frame.nChannels)
        
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(sub_image, self.frame_copy)
        else:
            cv.Flip(sub_image, self.frame_copy, 0)
        self.find_eyes()
        
        if self.is_a_valid_face_photo():
            self.find_wrinkles()
            self.find_avarage_colors()
            self.find_gender_age_emotions()
            #self.count_face_vector()
            self.create_face_vector()
        
    def note_results(self, results):
        f = open(self.note_file_url, "r+")
        txt = f.read()+results
        f.close()
        f = open(self.note_file_url, "w")
        f.write(txt)
        f.close()
            
    def is_a_valid_face_photo(self):
        return self.face_photo_valid
        
    def create_face_vector(self):
        #stosuje jednak taki wektor
        #[czas, sredni_kolor, odchylenie_std_koloru, liczba_zmarszczek, plec, wiek, emocje]
        self.time = time.time()
        #self.vector = [self.time,self.av_color[0],self.av_color[1], self.av_color[2],   self.stddev[0],self.stddev[1], self.stddev[2],self.wrinkles,self.gender, self.age,  self.emotions ]
        if self.time_makes_difference:
            self.vector = [self.time,self. u2l_ratio[0],self. u2l_ratio[1],self. u2l_ratio[2],   self.u2l_sd_ratio[0],self.u2l_sd_ratio[1], self.u2l_sd_ratio[2] ]
        else:
            self.vector = [self. u2l_ratio[0],self. u2l_ratio[1],self. u2l_ratio[2],   self.u2l_sd_ratio[0],self.u2l_sd_ratio[1], self.u2l_sd_ratio[2] ]
    def get_face_vector(self):
        #vektor sklada sie z :
        #[czas, sredni_kolor, kolor_gory, kolor_dolu, odchylenie_std_koloru, liczba_zmarszczek, plec, wiek, emocje]
        if self.is_a_valid_face_photo():
            return self.vector
        else:
            return None
        
    def find_avarage_colors(self):
        width,  height = self.frame_copy.width ,  self.frame_copy.height
        frame = self.frame_copy
        self.av_color,  self.stddev = cv.AvgSdv(self.frame_copy)
       
        half_width ,  half_height = width/3 ,  height/3
        
        
        upper_rect = (0, 0, half_width,  half_height)
        lower_rect =(half_width,  half_height,half_width-1  ,  half_height-1)
        upper_sub_image = cv.GetSubRect(self.frame_copy,  upper_rect)
        upper_frame = cv.CreateImage((upper_rect[2],upper_rect[3]),cv.IPL_DEPTH_8U, frame.nChannels)
        
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(upper_sub_image, upper_frame)
        else:
            cv.Flip(upper_sub_image, upper_frame, 0)
        u_av ,  u_sd = cv.AvgSdv(upper_frame)
        
        lower_sub_image = cv.GetSubRect(self.frame_copy,  lower_rect)
        lower_frame = cv.CreateImage((lower_rect[2],lower_rect[3]),cv.IPL_DEPTH_8U, frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(lower_sub_image, lower_frame)
        else:
            cv.Flip(lower_sub_image, lower_frame, 0)
        l_av ,  l_sd = cv.AvgSdv(lower_frame)    
        
        l_av = [l_av[0], l_av[1], l_av[2]]
        l_sd = [l_sd[0], l_sd[1],  l_sd[2]]
        if l_av[0]<0.00001:l_av[0]=0.0001
        if l_av[1]<0.00001:l_av[1]=0.0001
        if l_av[2]<0.00001:l_av[2]=0.0001
        if l_sd[0]<0.00001:l_sd[0]=0.0001
        if l_sd[1]<0.00001:l_sd[1]=0.0001
        if l_sd[2]<0.00001:l_sd[2]=0.0001
        
        
        self.u2l_ratio = (u_av[0]/l_av[0],u_av[1]/l_av[1], u_av[2]/l_av[2] )
        self.u2l_sd_ratio = (u_sd[0]/l_sd[0], u_sd[1]/l_sd[1], u_sd[2]/l_sd[2])
        
        del upper_frame 
        del lower_frame
        
    def count_face_vector(self):
        self.path ,  size = self.prepare_face_picture()
        self.time = time.time()
        self.gender ,  self.age , self.emotions = self.recognize_gender_age_emotions2(self.path,  size[0],  size[1])
        self.wrinkles = find_wrinkles()
        self.count 
    def prepare_face_picture(self):
        size= (92, 112) #180,180
        offset_pct=(0.35,0.35)
        ipr =  ImagesPreparer()
        self.emotions=  1
        self.path="tmp/"+str(md5.md5(str(random.randint(0, 9999))).hexdigest()+".jpg")
        img = self.frame_copy
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage(size, 8, 1)
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        cv.SaveImage(self.path, small_img)
        return self.path ,  size
        
    def find_gender_age_emotions(self):
        size= (92, 112) #180,180
        offset_pct=(0.35,0.35)
        ipr =  ImagesPreparer()
        self.emotions=  1
        self.path="tmp/"+str(md5.md5(str(random.randint(0, 9999))).hexdigest()+".jpg")
        img = self.frame_copy
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage(size, 8, 1)
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        cv.SaveImage(self.path, small_img)
        self.recognize_gender_age_emotions2(self.path, size[0], size[1])
        
    def recognize_gender_age_emotions2(self, path, s_x , s_y):
        ff_f   ,  r = "fisherfaces_full/" , "./Recognizer2"
        l , r, s = "left/" , "right/" , "straight/"
        p  ,  m,  f = "position/", "male/", "female/"
        chl,nrm,old = "0_12/", "13_40/" , "40+/"
        pc,  g ,  a,  a3 ,e= "position.yml","gender.yml", "age.yml" , "age3G.yml" , "emotion.yml"
        #check position
        self.position = self.recognize(ff_f+p+pc, path, s_x, s_y)
        #check age3G  - child / normal / old
        if   self.position ==2: #left
            #age3G
            age3G = self.recognize(ff_f+p+l+a3 , path, s_x, s_y)
            if age3G== 0: #child
                self.age =0
                #check gender
                self.gender = self.recognize(ff_f+p+l+chl+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+l+chl+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+l+chl+f+a, path, s_x, s_y)
            elif age3G ==1: #normal
                #check gender
                self.gender = self.recognize(ff_f+p+l+nrm+g, path, s_x, s_y)
                if self.gender ==0:
                    #male
                    self.age= self.recognize(ff_f+p+l+nrm+m+a, path, s_x, s_y)
                elif self.gender ==1:
                    #female
                    self.age= self.recognize(ff_f+p+l+nrm+f+a, path, s_x, s_y)
            elif age3G ==2: #old
                self.age = 6
                #check gender
                self.gender = self.recognize(ff_f+p+l+old+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+l+old+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+l+old+f+a, path, s_x, s_y)
        elif self.position ==1: #straight
            #age3G
            age3G = self.recognize(ff_f+p+s+a3 , path, s_x, s_y)
            if age3G== 0: #child
                self.age =0
                #check gender
                self.gender = self.recognize(ff_f+p+s+chl+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+s+chl+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+s+chl+f+a, path, s_x, s_y)
            elif age3G ==1: #normal
                #check gender
                self.gender = self.recognize(ff_f+p+s+nrm+g, path, s_x, s_y)
                if self.gender ==0:
                    #male
                    self.age= self.recognize(ff_f+p+s+nrm+m+a, path, s_x, s_y)
                elif self.gender ==1:
                    #female
                    self.age= self.recognize(ff_f+p+s+nrm+f+a, path, s_x, s_y)
            elif age3G ==2: #old
                self.age = 6
                #check gender
                self.gender = self.recognize(ff_f+p+s+old+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+s+old+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+s+old+f+a, path, s_x, s_y)
        elif self.position ==0: #right
            #age3G
            age3G = self.recognize(ff_f+p+r+a3 , path, s_x, s_y)
            #child
            if age3G== 0: 
                self.age =0
                #check gender
                self.gender = self.recognize(ff_f+p+r+chl+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+r+chl+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+r+chl+f+a, path, s_x, s_y)
            #normal
            elif age3G ==1: 
                #check gender
                self.gender = self.recognize(ff_f+p+r+nrm+g, path, s_x, s_y)
                if self.gender ==0:
                #male
                    self.age= self.recognize(ff_f+p+r+nrm+m+a, path, s_x, s_y)
                elif self.gender ==1:
                #female
                    self.age= self.recognize(ff_f+p+r+nrm+f+a, path, s_x, s_y)
            #old
            elif age3G ==2: 
                self.age = 6
                #check gender
                self.gender = self.recognize(ff_f+p+r+old+g, path, s_x, s_y)
                if self.gender==0: self.age = self.recognize(ff_f+p+r+old+m+a, path, s_x, s_y)
                elif self.gender==1: self.age = self.recognize(ff_f+p+r+old+f+a, path, s_x, s_y)
        #usuwam zbedne dziadostwa
        os.system("rm -f "+self.path)
        os.system("rm -f "+self.path+".txt")
        return self.gender ,  self.age , self.emotions

    def recognize(self, fisherface , path ,size_x , size_y):
        os.system("./Recognizer2 "+fisherface+" "+path+" "+str(size_x)+" "+str(size_y))
        diagnosis_url = path+".txt"
        f=open(diagnosis_url)
        result = eval(f.read())		
        f.close()
        return result
        
    def find_eyes(self):
        eye_cascade = cv.Load("haarcascades/haarcascade_eye.xml")
        image_scale = 1
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0
        # allocate temporary images
        img =self.frame_copy
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),cv.Round (img.height / image_scale)), 8, 1)
        # convert color input image to grayscal
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        eyes=  cv.HaarDetectObjects(small_img,eye_cascade,cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags) 
        self._sort_and_select_eyes(eyes)  

    def _sort_and_select_eyes(self, eyes):  # w tej funkcji ustala sie czy face is valid
        self.face_photo_valid=0
        l_e= len(eyes)
        sorted_eyes = self._bubblesort_tuples(eyes)
        #wybieram oczy
        if l_e >0:
            #znajduje oko i oszacowuje polozenie drugiego oka
            eye_rect = sorted_eyes.pop()[0]
            eye_center = (int((eye_rect[0]+eye_rect[2]/2.0)), int((eye_rect[1]+eye_rect[3]/2.0)))
            
            if eye_center[1]< self.rect[3]/2:
                #y2 ten sam , x2 przeciwny ( width - x)  - zakladam ze morda jest pionowo :-(
                eye2_center = (self.rect[2]-eye_center[0], eye_center[1])
                self.choose_left_and_right_eye([eye_center,  eye2_center])
                self.face_photo_valid =1
            else:
                self.face_photo_valid =0
        else:
            self.face_photo_valid=0
        
    def choose_left_and_right_eye(self,  eyes):
        eye1,  eye2 = eyes[0],  eyes[1]
        if eye1[0] > eye2[0]: self.right_eye = eye1 ; self.left_eye = eye2
        else : self.right_eye = eye2 ; self.left_eye = eye1

    def _segregate_eyes(self, sorted_eyes):
        face_width = self.rect[2]
        l_s_e =len(sorted_eyes)
        if l_s_e==2:
            sub_pts = sorted_eyes[:2]
            center =[]
            for sub_pt in sub_pts:
                center.append(( int((sub_pt[0][0]+sub_pt[0][2]/2.0)),  int((sub_pt[0][1]+sub_pt[0][3]/2.0))))
            right_eye_x=  left_eye_x = center[0][0]
            right_eye_y=  left_eye_y = center[0][1]
            for i in range(2):
                if center[i][0] <     left_eye_x: left_eye_x , left_eye_y= center[i][0], center[i][1]
                elif center[i][0]>right_eye_x: right_eye_x ,  right_eye_y = center[i][0], center[i][1]
            self.left_eye,  self.right_eye = (left_eye_x, left_eye_y),  (right_eye_x, right_eye_y)

    def _bubblesort_tuples(self, array_of_tuples,index =1):
        n = len(array_of_tuples)
        while n>1:
            for i in range(n-1):
                if array_of_tuples[i][index] < array_of_tuples[i+1][index]:
                    temp =array_of_tuples[i]
                    array_of_tuples[i] = array_of_tuples[i+1]
                    array_of_tuples[i+1]=temp
            n = n-1
        return array_of_tuples
        
    def find_wrinkles(self):
        rect = self.rect
        sob_mat = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, self.frame_copy.nChannels)
        if self.frame_copy.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(self.frame_copy, sob_mat)
        else:
            cv.Flip(self.frame_copy, sob_mat, 0)
        #sob_mat = cv.CloneMat(self.frame_copy)
        cv.Sobel(sob_mat,sob_mat,1,1)
        y_max, y_badania1, y_badania2, x_max , i = rect[3],  rect[3]/5, rect[3]/4,  rect[2],  0
        twarz = sob_mat
        for x in range(x_max):
            if twarz[x,y_badania1][0]+twarz[x,y_badania1][1]+twarz[x,y_badania1][2]>self.white_level:
                i+=1
            if twarz[x,y_badania2][0]+twarz[x,y_badania2][1]+twarz[x,y_badania2][2]>self.white_level:
                i+=1
        self.wrinkles = i/2
        return self.wrinkles
"""
class Person:
    def __init__(self,  frame,  rect):
        self.rect = rect
        self.white_level = 6
        sub_image = cv.GetSubRect(frame,  rect)
        self.frame_copy = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(sub_image, self.frame_copy)
        else:
            cv.Flip(sub_image, self.frame_copy, 0)
        self.find_eyes()
        if self.is_a_valid_face_photo():
            self.find_wrinkles()
            self.find_avarage_colors()
            self.find_gender_age_emotions()
            self.create_face_vector()
    
    def note_results(self, results):
        f = open(self.note_file_url, "r+")
        txt = f.read()+results
        f.close()
        f = open(self.note_file_url, "w")
        f.write(txt)
        f.close()
            
    def is_a_valid_face_photo(self):
        return self.face_photo_valid
        
    def create_face_vector(self):
        #stosuje jednak taki wektor
        #[czas, sredni_kolor, odchylenie_std_koloru, liczba_zmarszczek, plec, wiek, emocje]
        self.time = time.time()
        self.vector = [self.time,self.av_color[0],self.av_color[1], self.av_color[2],   self.stddev[0],self.stddev[1], self.stddev[2],self.wrinkles,self.gender,  self.emotions ]
        
    def get_face_vector(self):
        #vektor sklada sie z :
        #[czas, sredni_kolor, kolor_gory, kolor_dolu, odchylenie_std_koloru, liczba_zmarszczek, plec, wiek, emocje]
        if self.is_a_valid_face_photo():
            return self.vector
        else:
            return None
        
    def find_avarage_colors(self):
        self.av_color,  self.stddev = cv.AvgSdv(self.frame_copy)
        
    def find_gender_age_emotions(self):
        size= (180,180)
        offset_pct=(0.35,0.35)
        ipr =  ImagesPreparer()
        self.emotions=  1
        self.path="tmp/"+str(md5.md5(str(random.randint(0, 9999))).hexdigest()+".jpg")
        cv.SaveImage(self.path, self.frame_copy)
        image = Image.open(self.path)
        ipr.CropRotateFace(image, self.left_eye, self.right_eye, offset_pct,  size,self.path)
        os.system("./Recognizer "+"fisherfaces_gender2.yml "+self.path)
        txt_url =self.path+".txt"
        gender =  eval(open(txt_url).read())
        txt_url =self.path+".txt"
        self.gender =  eval(open(txt_url).read())
        os.system("./Recognizer "+"fisherfaces_age2.yml "+self.path)
        self.age = eval(open(txt_url).read())  
        #usuwam zbedne dziadowstwa
        os.system("rm -f "+self.path)
        os.system("rm -f "+txt_url)
        del image
        
    def find_eyes(self):
        nose_cascade = cv.Load("haarcascades/haarcascade_mcs_nose.xml");
        #eyes_mouth_cascade = cv.Load("haarcascades/haarcascade_mcs_mouth.xml")
        eye_cascade = cv.Load("haarcascades/haarcascade_eye.xml")
        #min_size = (20, 20)
        image_scale = 1
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0
        # allocate temporary images
        img =self.frame_copy
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),cv.Round (img.height / image_scale)), 8, 1)
        # convert color input image to grayscal
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        noses= cv.HaarDetectObjects(small_img, nose_cascade, cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags)
        eyes=  cv.HaarDetectObjects(small_img,eye_cascade,cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags) 
        self._sort_and_select_eyes_and_nose(eyes, noses)  

    def _sort_and_select_eyes_and_nose(self, eyes, noses):  # w tej funkcji ustala sie czy face is valid
        self.face_photo_valid=0
        l_e,  l_n = len(eyes),  len(noses)
        sorted_eyes = self._bubblesort_tuples(eyes)
        #wybieram nosy
        if l_n>1:       self.nose = self._bubblesort_tuples(noses)[0]
        elif l_n==1: self.nose = noses[0]
        #-----------------
        #wybieram oczy
        if l_e>1 and l_n>0:
            self._segregate_eyes(sorted_eyes)
            # sprawdzam czy nos jest pomiedzy oczami
            nose_center = (int((self.nose[0][0]+self.nose[0][2])/2.0),  int((self.nose[0][1]+self.nose[0][3])/2.0))
            #print self.right_eye , "  ", self.nose ,"   ", self.left_eye
            if nose_center[0]<self.right_eye[0] and nose_center[0]> self.left_eye[0]:
                self.face_photo_valid =1

    def _segregate_eyes(self, sorted_eyes):
        if len(sorted_eyes)>1:
            sub_pts = sorted_eyes[:2]
            center =[]
            for sub_pt in sub_pts:
                center.append(( int((sub_pt[0][0]+sub_pt[0][2])/2.0),  int((sub_pt[0][1]+sub_pt[0][3])/2.0)))
            right_eye_x=  left_eye_x = center[0][0]
            right_eye_y=  left_eye_y = center[0][1]
            for i in range(2):
                if center[i][0] <     left_eye_x: left_eye_x , left_eye_y= center[i][0], center[i][1]
                elif center[i][0]>right_eye_x: right_eye_x ,  right_eye_y = center[i][0], center[i][1]
            self.left_eye,  self.right_eye = (left_eye_x, left_eye_y),  (right_eye_x, right_eye_y)

    def _bubblesort_tuples(self, array_of_tuples,index =1):
        n = len(array_of_tuples)
        while n>1:
            for i in range(n-1):
                if array_of_tuples[i][index] < array_of_tuples[i+1][index]:
                    temp =array_of_tuples[i]
                    array_of_tuples[i] = array_of_tuples[i+1]
                    array_of_tuples[i+1]=temp
            n = n-1
        return array_of_tuples
        
    def find_wrinkles(self):
        rect = self.rect
        sob_mat = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, self.frame_copy.nChannels)
        if self.frame_copy.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(self.frame_copy, sob_mat)
        else:
            cv.Flip(self.frame_copy, sob_mat, 0)
        #sob_mat = cv.CloneMat(self.frame_copy)
        cv.Sobel(sob_mat,sob_mat,1,1)
        y_max, y_badania1, y_badania2, x_max , i = rect[3],  rect[3]/5, rect[3]/4,  rect[2],  0
        twarz = sob_mat
        for x in range(x_max):
            if twarz[x,y_badania1][0]+twarz[x,y_badania1][1]+twarz[x,y_badania1][2]>self.white_level:
                i+=1
            if twarz[x,y_badania2][0]+twarz[x,y_badania2][1]+twarz[x,y_badania2][2]>self.white_level:
                i+=1
        self.wrinkles = i/2
 """
