from PyQt4 import QtCore, QtGui
from Analysis import *
import cv2.cv as cv
import Person4,  Room ,  sys ,  time
import threading
class Functions:
    def load_params(self):
        self.opened_sub_images =[0]*16
        self.mx =255
        self.time_makes_difference = self.checkBox_4.isChecked()
        self.time_importance = self.horizontalSlider.value()
        self.new_person_tresh = self.doubleSpinBox_7.value()
        self.person_ammount = self.spinBox_7.value()
        self.face_cert = self.doubleSpinBox_2.value()
        self.should_camera_be_able_to_run = 1
        self.print_result = self.checkBox_13.isChecked()
        self.picture =0

        self.camera_number = [self.spinBox_3.value(),self.spinBox_2.value() ]
        self.show_main_view = [self.checkBox.isChecked(), self.checkBox_6.isChecked()]
        self.verify_detected_faces = [self.checkBox_2.isChecked(),self.checkBox_7.isChecked()]
        self.mark_detected_objects = [self.checkBox_3.isChecked(),self.checkBox_8.isChecked()]
        self.flip_image_verticaly = [self.checkBox_10.isChecked(),self.checkBox_11.isChecked()]
        self.run_face_analysis = [self.checkBox_12.isChecked(),self.checkBox_9.isChecked()]
        #camera 2
        self.run_reverse_camera = self.checkBox_5.isChecked()
        
        self.room = Room.Room(self.person_ammount, self.new_person_tresh, [self.time_makes_difference,  self.time_importance])
        self.results_file_url = "results/temp_results.txt"
        f = open(self.results_file_url, "w")
        f.close()

    def turn_camera_on(self):
        print "turn camera on"
        self.load_params()
        thread = threading.Thread(target = self._run_camera,  args=(0, ))
        thread.start() 
        if self.run_reverse_camera:
            thread2 = threading.Thread(target = self._run_camera,  args=(1,  ))
            thread2.start()
        
    def make_the_rectangle_bigger(self, x0,  y0, w,  h,  h2h0, img_height, image_scale):
        h2 = int(h2h0*h)
        y02 = y0 - int((h2h0-1)*h/2.0)
        if y02<0: y02=0
        if y02+h2 >=img_height: y02 = img_height -1
        x0 ,  y02 ,  w,  h2 = int(x0 * image_scale),  int(y02 * image_scale), int(w * image_scale),  int(h2 * image_scale)
        return x0,  y02,  w ,  h2
        
    def create_person_and_add_to_room(self,img,rect, camera_position):
        person = Person4.Person4(img,  rect, self.verify_detected_faces[camera_position], self.run_face_analysis[camera_position] )  #sprawdza czy zdjecie nadaje sie do analizy cech, okresla cechy, zwraca wektor cech
        if camera_position==0:
            self.room.Add_person(person,  self.print_result)
        else:
            self.room.Remove_person(person, self.print_result)
        del(person)
    
    def _run_camera(self, camera_position):
        cascade = cv.Load("haarcascades/haarcascade_frontalface_alt2.xml")
        capture = cv.CreateCameraCapture(self.camera_number[camera_position])
        if self.show_main_view[camera_position]: cv.NamedWindow("result"+str(camera_position), 1)
        if capture:
            frame_copy = None
            #i=0
            prev_t,  now_t = time.time(), 0
            while self.should_camera_be_able_to_run:
                frame = cv.QueryFrame(capture)
                if self.flip_image_verticaly[camera_position]: cv.Flip(frame, frame)
                if not frame:
                    print "not frame"
                else:
                    now_t= time.time()
                    fps = 1/(now_t - prev_t)
                    prev_t = now_t
                    print fps
                    self.detect_and_draw(frame, cascade,  camera_position)
                    #cv.WaitKey(1)
                    #continue
                #if self.show_main_view[camera_position]: cv.ShowImage("result"+str(camera_position), frame)
                #if not frame_copy:
                #    frame_copy = cv.CreateImage((frame.width,frame.height),cv.IPL_DEPTH_8U, frame.nChannels)
                #if frame.origin == cv.IPL_ORIGIN_TL:
                #    cv.Copy(frame, frame_copy)
                #else:
                #    cv.Flip(frame, frame_copy, 0)
                #if cascade:
               #self.detect_and_draw(frame, cascade,  camera_position)
        #else:
            #image = cv.LoadImage(input_name, 1)
           
            #cv.WaitKey(0)
        try:
            cv.DestroyWindow("result"+str(camera_position))
        except:
            print "could not destroy window"

    def detect_and_draw(self,img, cascade, camera_position=0):
        min_size = (20, 20)
        image_scale = self.horizontalSlider_3.value()
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0
        # allocate temporary images
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img_height = cv.Round (img.height / image_scale)
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),small_img_height), 8, 1)
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)
        if faces:
            for ((x, y, w, h), n) in faces:
                if self.face_cert<n:
                     x2 , y2, w2 , h2 = self.make_the_rectangle_bigger(x, y, w, h, 1.22,  small_img_height, image_scale)
                     self.create_person_and_add_to_room(img ,(x2, y2, w2, h2) , camera_position)
                     if self.mark_detected_objects[camera_position] :
                         pt2 = (int(x2 + w2), int(y2 + h2))
                         cv.Rectangle(img, (x2, y2), pt2, cv.RGB(255, 0, 0), 3, 8, 0)
        if self.show_main_view[camera_position]: cv.ShowImage("result"+str(camera_position), img)

    def _close_windows(self, all=0):
        """
        if all:
            try:
                cv.DestroyWindow("result")
            except: pass
        for i in range(16):
            try:
                cv.DestroyWindow("face"+str(i))
            except: pass
        """
        cv.DestroyAllWindows()
        
    def turn_camera_off(self):
        print "turn camera off"
        self.should_camera_be_able_to_run =0
        
    def exit(self):
        exit()
        
    def _show_found_face(self, image, rect,  face_number):
        sub_image = cv.GetSubRect(image,  rect)
        cv.ShowImage("face"+str(face_number), sub_image)
        
    def set_new_person_treshold(self):
            if self.checkBox_4.isChecked()==True:
                self.doubleSpinBox_7.setValue(.5)
            elif self.checkBox_4.isChecked()==False:
                self.doubleSpinBox_7.setValue(0.15)
            
    def run_data_analysis_module(self):
        thread = threading.Thread(target = self.start_data_analysis_module_in_external_terminal)
        thread.start()
        
    def start_data_analysis_module_in_external_terminal(self):
        os.system("python ../DataAnalysisModule/Ui_DataAnalysis.py")
