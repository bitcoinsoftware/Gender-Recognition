from PyQt4 import QtCore, QtGui
import threading,  time,  md5,  urllib2,  urllib
class DataAnalysisConnections:
    def connect(self):
        QtCore.QObject.connect(self.centralwidget,QtCore.SIGNAL('insert_results'),self.insert_results)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL('clicked()'),self.run_checker)
        QtCore.QObject.connect(self.pushButton_4,QtCore.SIGNAL('clicked()'),self.stop_checker)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL('clicked()'),self.run_uploader)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),self.stop_uploader)
        QtCore.QObject.connect(self.pushButton_5,QtCore.SIGNAL('clicked()'),self.run_uploader_and_checker)
        QtCore.QObject.connect(self.pushButton_6,QtCore.SIGNAL('clicked()'),self.stop_uploader_and_checker)
        
    def run_uploader(self):
        print "run uploader"
        self.pushButton_2.enabled=0
        self.pushButton_3.enabled=1
        self.uploader_can_run=1
        thread = threading.Thread(target = self.post_data)
        thread.start()
    
    def stop_uploader(self):
        self.uploader_can_run=0
        self.pushButton_2.enabled=1
        self.pushButton_3.enabled=0

    def run_checker(self):
        self.checker_can_run=1
        self.pushButton.enabled=0
        self.pushButton_4.enabled=1
        thread = threading.Thread(target = self.check)
        thread.start()
    
    def stop_checker(self):
        self.checker_can_run=0
        self.pushButton.enabled=0
        self.pushButton_4.enabled=1
        
    def run_uploader_and_checker(self):
        self.run_checker()
        time.sleep(1)
        self.run_uploader()
        
    def stop_uploader_and_checker(self):
        self.stop_checker()
        self.stop_uploader()
    
    def post_data(self,  pswrd="piorebitcoinynaokraglo", prefix="DATA START"):
        if self.radioButton.isChecked():
            prefix +="INT"
        else:
            prefix+="OUT"
        url = "https://noszkurwa.com/AA_haksiory_tybana/facjata/data_reciver.php"
        password_field , data_field= "pass",  "log"
        password = md5.md5(pswrd).hexdigest() 
        while self.uploader_can_run==1:
            try:
                #data_dictionary=[[]*6]
                """
                data_dictionary['COUNTED']=self.spinBox.value()
                data_dictionary['MAN']=self.spinBox_4.value()
                data_dictionary['WOMAN']=self.spinBox_3.value()
                data_dictionary['AVARAGE_AGE']=self.spinBox_2.value()
                data_dictionary['NEUTRAL']=self.spinBox_7.value()
                data_dictionary['HAPPY']=self.spinBox_8.value()
                """
                #data_arr = [['COUNTED', self.spinBox.value()],['MAN', self.spinBox_4.value()], ['WOMAN', self.spinBox_3.value()], 
                 #                       ['AVARAGE_AGE', self.spinBox_2.value()], ['NEUTRAL', self.spinBox_7.value()], ['HAPPY', self.spinBox_8.value()] ]
                #COUNTED;MAN;WOMAN;AVARAGE_AGE;NEUTRAL;HAPPY
                clear_text=str(self.spinBox.value())+";"+str(self.spinBox_4.value())+";"+str(self.spinBox_3.value())+";"+str(self.spinBox_2.value())+";"+str(self.spinBox_7.value())+";"+str(self.spinBox_8.value())
                raw_text = prefix+clear_text+"DATA END"
                form_data = {password_field : password, data_field: raw_text}
                params = urllib.urlencode(form_data)
                response = urllib2.urlopen(url, params)
                data = response.read()
                print data
            except:
                print "Probably internet connection failed"
            time.sleep(self.spinBox_5.value())
    
    def check(self):
        while self.checker_can_run ==1:
            f= open("../PeopleAnalysisModule/results/temp_results.txt")
            ress= f.read()
            f.close()
            ress = ress.split("\n")
            personID_list =[]
            person_results_list =[]
            for res in ress:
                if len(res)>1:
                    try: # czasem wywala blad, jak jest podwony dostep do pliku
                        res = eval(res)
                        self.no_mistake =1
                    except:
                        person_results_list=[]
                        self.no_mistake=0
                        break
                    if res["personID"] in personID_list :
                        person_results_list[res["personID"] ].append([res["gender"], res["age"], res["emotions"]])
                    else:
                        personID_list.append(res["personID"])
                        person_results_list.append( [[res["gender"], res["age"], res["emotions"]]])
        
            results = person_results_list
            final_results_list=[]
            for person_res in results:
                gender_age_emotion_list =[[], [], []]
                for res in person_res:
                    gender_age_emotion_list[0].append(res[0])
                    gender_age_emotion_list[1].append(res[1])
                    gender_age_emotion_list[2].append(res[2])
                gender_age_emotion_list[0].sort(),  gender_age_emotion_list[1].sort(), gender_age_emotion_list[2].sort()
                g, gc = self._avarage(gender_age_emotion_list[0])
                a, ac = self._avarage(gender_age_emotion_list[1])
                e, ec = self._avarage(gender_age_emotion_list[2])
                final_results_list.append( [g, round(gc, 3), a, round(ac, 3), e, round(ec, 3)] )
            if self.no_mistake ==1:
                self.txt =""
                i=0
                for res in final_results_list:
                    self.txt+="ID:"+str(i)+" GDR: "+str(res[0])+" "+str(res[1])+ " AGE: "+str(res[2])+" "+str(res[3])+" EMO: "+str(res[4])+"\n"
                    i+=1
                self.av_age ,  self.people_in, self.am_man,  self.am_woman,  self.am_happy = self.get_statistics(final_results_list)
                self.am_neutral = self.people_in - self.am_happy
                self.centralwidget.emit(QtCore.SIGNAL("insert_results"))
                time.sleep(self.spinBox_6.value())
            else:
                time.sleep(1)
                
    def insert_results(self):
        self.plainTextEdit.setPlainText(self.txt)
        #self.av_age ,  self.people_in, self.am_man,  self.am_woman
        self.spinBox_2.setValue(self.av_age)
        self.spinBox.setValue(self.people_in)
        self.spinBox_3.setValue(self.am_woman)
        self.spinBox_4.setValue(self.am_man)
        self.spinBox_7.setValue(self.am_neutral)
        self.spinBox_8.setValue(self.am_happy)
        
    def _median(self, list):
        list.sort()
        length = len(list)
        median =list[length/2]
        return median ,  list.count(median)/float(len(list))
        
    def _avarage(self, list):
        ll =len(list)
        avr = sum(list)/float(ll)
        if avr%1>0.5:
            avr+=1
        avr = int(avr)
        return avr,  list.count(avr) / float(ll)
        
    def _most_counted_group(self,  list):
        groups = []
        counts = []
        #sprawdzam grupy
        for res in list:
            if not (res in groups):
                groups.append(res)
        for gr in groups:
            counts.append(list.count(gr))
        bgst_idx,  bgst_ct,  i =0 , 0, 0
        for ct in counts:
            if bgst_ct < ct:
                bgst_ct,  bgst_idx = ct , i
            i+=1 
        return groups[bgst_idx] ,  bgst_ct/float(len(list))
        
    def get_statistics(self, results):
        woman ,  man , happy,  age_list= 0, 0,0,   []
        for res in results:
            if res[0]==0:
                man+=1
            else:
                woman+=1
            if res[4]==0:
                happy+=1
            age_list.append(res[2])
        av_age,  blabla = self._avarage(age_list)
        return av_age ,  len(results),  man ,  woman , happy
    
