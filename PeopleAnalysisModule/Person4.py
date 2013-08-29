import cv,  cv2 , os ,  time,  Image,  md5, random
from ImagesPreparer import *
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
 
class Person4:
    def __init__(self,  frame,  rect, verify_detected_faces, run_face_analysis):
        self.rect = rect
        self.face_photo_valid = False
        self.face_size= [rect[2], rect[3]]
        self.personID=-1
        self.white_level = 6
        self.size= (92, 112) #180,180
        
        #wycina tylko twarz
        try:
            sub_image = cv.GetSubRect(frame,  rect)
        except:
            return None
        self.frame_copy = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, frame.nChannels)
        
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(sub_image, self.frame_copy)
        else:
            cv.Flip(sub_image, self.frame_copy, 0)
        self.path  = self.prepare_face_picture() # zmniejsza zdjecie twarzy by bylo dobre do analizy
        if verify_detected_faces:
            self.validate_face_photo()  # sprawdza czy na zdjeciu twarzy wystepuje nos, jesli wystepuje to znaczy ze to zdjecie twarzy
        else: self.face_photo_valid =1
        if self.is_a_valid_face_photo():
            self.time = time.time()
            self.wrinkles = self.find_wrinkles()
            self.A2B_ratio ,  self.A_B_color ,  self.C_color = self.find_avarage_colors()
            if run_face_analysis:
                self.gender ,  self.age , self.emotions = self.find_gender_age_emotions()
                gender_ratio ,  age_ratio ,  emotions_ratio = round(self.gender/3.0, 3),  round(self.age/18.0, 3),  round(self.emotions/3.0, 3)
            else: 
                self.gender ,  self.age , self.emotions,  self.position = 0, 0, 0, 1
                gender_ratio ,  age_ratio,  emotions_ratio = 0, 0, 0
                
            self.x_position_ratio = self.count_position_ratio(rect[0], frame.width)
            self.create_face_vector([self.time, self.wrinkles,self.A2B_ratio,self.A_B_color,self.C_color,
                                     gender_ratio ,age_ratio ,emotions_ratio, self.x_position_ratio] )
            
    def prepare_face_picture(self):
        self.offset_pct=(0.35,0.35)
        ipr =  ImagesPreparer()
        self.emotions=  1
        self.path="tmp/"+str(md5.md5(str(random.randint(0, 99999))).hexdigest()+".jpg")
        img = self.frame_copy
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        self.small_img = cv.CreateImage(self.size, 8, 1)
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, self.small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(self.small_img, self.small_img)
        cv.SaveImage(self.path, self.small_img)
        return self.path 

    def validate_face_photo(self):
        nose_cascade = cv.Load("haarcascades/haarcascade_mcs_nose.xml")
        image_scale = 1
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0
        noses=  cv.HaarDetectObjects(self.small_img,nose_cascade,cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags) 
        self.face_photo_valid=0
        l_n= len(noses)
        sorted_noses = self._bubblesort_tuples(noses)
        if l_n >0:
            self.face_photo_valid=1
        else:
            self.face_photo_valid = 0
            
    def is_a_valid_face_photo(self):
        return self.face_photo_valid

    def find_wrinkles(self):
        #full face image wrinkles
        rect = self.rect
        sob_mat = cv.CreateImage((rect[2],rect[3]),cv.IPL_DEPTH_8U, self.frame_copy.nChannels)
        if self.frame_copy.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(self.frame_copy, sob_mat)
        else:
            cv.Flip(self.frame_copy, sob_mat, 0)
        cv.Sobel(sob_mat,sob_mat,1,1)
        y_max, y_badania1, y_badania2, x_max , i = rect[3],  rect[3]/5, rect[3]/4,  rect[2],  0
        twarz = sob_mat
        for x in range(x_max):
            if twarz[x,y_badania1][0]+twarz[x,y_badania1][1]+twarz[x,y_badania1][2]>self.white_level:
                i+=1
            if twarz[x,y_badania2][0]+twarz[x,y_badania2][1]+twarz[x,y_badania2][2]>self.white_level:
                i+=1
        wrinkles_full = i/2
        #teraz badam tylko cere
        #crop ratio  - left:0.25 , right:0.25 , up:0.12 , down:0.12
        rect_skin = (int(rect[2]*0.25),  int(rect[3]*0.12), int(rect[2]*0.5), int(rect[3]*0.76) )
        twarz = cv.GetSubRect(sob_mat,  rect_skin)
        y_max, y_badania1, y_badania2, x_max , i = rect_skin[3],  rect_skin[3]/5, rect_skin[3]/4,  rect_skin[2],  0
        for x in range(x_max):
            if twarz[x,y_badania1][0]+twarz[x,y_badania1][1]+twarz[x,y_badania1][2]>self.white_level:
                i+=1
            if twarz[x,y_badania2][0]+twarz[x,y_badania2][1]+twarz[x,y_badania2][2]>self.white_level:
                i+=1
        wrinkles_small = i/2
        #zwracam stosunek zmarszczek na cerze do zmarszczek na calym zdjeciu twarzy
        return wrinkles_small/float(wrinkles_full)
        
    def note_results(self, results):
        f = open(self.note_file_url, "r+")
        txt = f.read()+results
        f.close()
        f = open(self.note_file_url, "w")
        f.write(txt)
        f.close()
        
    def create_face_vector(self, vect):
        self.vector = vect
            
    def get_face_vector(self):
        if self.is_a_valid_face_photo():
            return self.vector
        else:
            return None
        
    def find_avarage_colors(self):
        
        #+----+--C--+----+
        #       |--A--|    |
        #       |--B--|    |
        # +---+-------+---+
        #A_image
        rect=[0, 0, self.small_img.width, self.small_img.height]
        rect_A =(int(rect[2]*0.25),  int(rect[3]*0.12), int(rect[2]*0.5), int(rect[3]*0.38) ) #czolo nos
        rect_B =(int(rect[2]*0.25),  int(rect[3]*0.5), int(rect[2]*0.5), int(rect[3]*0.38) ) #nos broda
        rect_C =(int(rect[2]*0.25),  0, int(rect[2]*0.5), int(rect[3]*0.12) )  #wlosy
        
        A_image =  cv.GetSubRect(self.small_img, rect_A)
        B_image =  cv.GetSubRect(self.small_img, rect_B)
        C_image =  cv.GetSubRect(self.small_img, rect_C)
        A_av ,  A_sd = cv.AvgSdv(A_image)
        B_av ,  B_sd = cv.AvgSdv(B_image)
        C_av ,  C_sd = cv.AvgSdv(C_image)
        A_av ,  B_av, C_av = sum(A_av)/float(len(A_av)), sum(B_av)/float(len(B_av)), sum(C_av)/float(len(C_av))
        if B_av <0.0001: B_av =0.0001
        self.A2B_ratio ,  self.A_B_color ,  self.C_color = A_av/float(B_av) ,  (A_av+B_av)/510.0 , C_av/255.0
        return self.A2B_ratio ,  self.A_B_color ,  self.C_color
        
    def count_position_ratio(self, x0, maxx):
        self.x_position_ratio = x0/float(maxx)
        return self.x_position_ratio  
    """
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
        
        self.recognize_gender_age_emotions(self.size[0], self.size[1])
    """
    def find_gender_age_emotions(self):
        ff_f   ,  r = "fisherfaces_full/" , "./Recognizer2"
        l , r, s = "left/" , "right/" , "straight/"
        p  ,  m,  f,  pe = "position/", "male/", "female/",  "position_emotion/"
        chl,nrm,old = "0_12/", "13_40/" , "40+/"
        pc,  g ,  a,  a3 ,e= "position.yml","gender.yml", "age.yml" , "age3G.yml" , "emotion.yml"
        path = self.path
        s_x,  s_y = self.size[0], self.size[1]
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
            #check emotions
            self.emotions = self.recognize(ff_f+pe+l+e,  path,  s_x, s_y)
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
            #check emotions
            self.emotions = self.recognize(ff_f+pe+s+e,  path,  s_x, s_y)
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
                
            #check emotions
            self.emotions = self.recognize(ff_f+pe+r+e,  path,  s_x, s_y)
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
    """
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
