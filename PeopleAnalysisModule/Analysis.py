import cv ,  cv2,  thread,  time
import os
from Room import *
from Person import *
class Analysis:
    def __init__(self,cam_resolution, camera_number,  horizontal_sect,  vertical_sect, white_level,  person_ammount, new_person_tresh, sleep_period_value):
        print " analysis"
        #podzial sceny na sektory
        self.note_file_url = "results/results"
        self.cam_resolution = cam_resolution
        self.camera_number = camera_number
        self.white_level = white_level
        self.person_ammount = person_ammount
        self.sectors = []
        self.sleep_period_value =sleep_period_value
        row =[]
        self.persons =[]
        miny_x = range(0, cam_resolution[0], cam_resolution[0]/horizontal_sect)
        maksy_x = range(cam_resolution[0]/horizontal_sect,  (cam_resolution[0]/horizontal_sect*(horizontal_sect+1)),  cam_resolution[0]/horizontal_sect)
        miny_y = range(0,cam_resolution[1] , cam_resolution[1] /vertical_sect)
        maksy_y = range(cam_resolution[1]/vertical_sect,  (cam_resolution[1]/vertical_sect*(vertical_sect+1)),  cam_resolution[1]/vertical_sect )
        for i in range(vertical_sect):
            miny,  maksy= miny_y[i], maksy_y[i]
            for column in range(horizontal_sect):
                minx,  maksx = miny_x[column],  maksy_x[column]
                row.append((minx, miny, maksx,  maksy))
            self.sectors.append(row)
        self.room = Room(person_ammount, new_person_tresh)
        f= open(self.note_file_url, "w")
        f.close()
    def stop(self):    
        self.run_the_analysis =False
        
    def run_analysis(self):
        self.run_the_analysis= True
        print "run analysis"
        while self.run_the_analysis:
            images_data_file = open("images_data")
            face_number=0
            face_data =[]
            #wyszukuje linii definiujacych osobe
            for line in images_data_file:
                if(line.find("face")!=-1):
                    try:
                        face_number = eval(line[4:5].strip())   # zamienic na TRY bo sie czasem pierdoli
                        f_rect = eval(line.split(":")[1].strip())
                        face_data.append(face_number)
                        face_data.append(f_rect)
                    except:
                        break
                if(line.find("NOSE:")!=-1):
                    try:
                        nose_rect = eval(line.split(":")[1].strip())
                        face_data.append(nose_rect)
                    except:
                        break
                if(line.find("POINTS:")!=-1): 
                    try:
                        points_rect = eval(line.split(":")[1].strip())
                        face_data.append(points_rect)
                    except:
                        break
                    new_person = Person(face_data,  self.sectors,   self.white_level, self.note_file_url)
                    face_data =[]
                    #jak nadaje sie do analizy to tworze nowa osobe
                    if new_person.is_person_created():
                        print "twarz ",  face_number,  " nadaje sie do analizy"
                        person_class = self.is_a_new_person(new_person)
                        if person_class[0]:
                            print "to byla nowa osoba, dodalem ja"
                        else:
                            print "juz widzialem ta osobe, to byla osoba", person_class[1]," updatuje ja"
                            self.room.people_list[person_class[1]]=new_person
                    else:
                        print "osoba nie stworzona"
            images_data_file.close()
            time.sleep(self.sleep_period_value)
                
    def is_a_new_person(self, person):
        return self.room.check_and_add_if_new(person)
        #return False
        
    def extract_face_information(self):
        return [0, 0, 3, 2, 0]
    
    def detect_faces_with_threshold(self, original,  face_certanity):
        detected = cv.HaarDetectObjects(original,  self.haar_face, self.storage)
        #wybieram tylko te pewne twarze
        certain_faces= []
        for cvmatrix in detected:
            if cvmatrix[1]> face_certanity: certain_faces.append(cvmatrix)
        return certain_faces
  

