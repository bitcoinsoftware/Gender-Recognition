import time

class Room:
    def __init__(self, people_ammount , new_person_tresh, time_array):
        print "Room"
        self.results_file_url = "results/temp_results.txt"
        self.people_list =[]
        self.personID =-1
        self.people_result_list =[]  # [  (PersonID, [[Gender, Age, Emotions], [Gender, Age, Emotions], [Gender, Age, Emotions]]) ]
        #how many people  should it remember
        self.people_ammount = people_ammount
        self.new_person_tresh =new_person_tresh
        [self.time_makes_difference,  self.time_importance]  = time_array
        
    def Add_person(self,  person,  print_result=1):
        if type(person.get_face_vector())==type([]):
            if len(self.people_list)==0: #dodaje osobe jak wczesniej nie bylo zadnej
                self.people_list.append(person)
                #self.people_result_list.append((self.personID, [[person.gender, person.age,  person.emotions]])) 
                #person.personID= self.personID
                #self.personID+=1
                return None
            is_true ,  person_number = self.is_a_new_person(person)
            if is_true:  #dodaje osobe
                self.people_list.append(person)
                #self.people_result_list.append((self.personID, [[person.gender, person.age,  person.emotions]])) 
                #person.personID= self.personID
                #self.personID+=1
            else:  # updatuje osobe
                #person.personID = self.people_list[person_number].personID
                #self.people_result_list[self.personID][1].append([person.gender, person.age,  person.emotions])
                self.people_list[person_number] = person
            if len(self.people_list)==self.people_ammount: self.people_list.pop(0)
            pozycja ='none'
            if person.position ==1 : pozycja = 'PROSTO'
            elif person.position ==0: pozycja = 'PRAWO'
            else: pozycja = 'LEWO'
            
            plec ='none'
            if person.gender ==1 : plec = 'KOBIETA'
            else: plec = 'MEZCZYZNA'
            if print_result:
                print "person nr ", person_number ,"pozycja ", pozycja,  "plec ",  plec,  "wiek ",  person.age ," emocje ",  person.emotions
            #if (self.personID+1)%3==0:
            #    print self.people_result_list
            self.note_results(person_number,  person.gender, person.age, person.emotions)
            
    def Remove_person(self,  person):
        pass
            
    def note_results(self, personID,  gender,  age,  emotions):
        results = str({"personID":personID, "gender":gender,  "age":age,  "emotions":emotions})+"\n"
        f = open(self.results_file_url, "r+")
        txt = f.read()+results
        f.close()
        f = open(self.results_file_url, "w")
        f.write(txt)
        f.close()
        
    def get_results(self):
        f= open(self.results_file_url)
        ress= f.read()
        f.close()
        ress = ress.split("\n")
        personID_list =[]
        person_results_list =[]
        for res in ress:
            if len(res)>1:
                res = eval(res)
                if res["personID"] in personID_list:
                    person_results_list[res["personID"] ].append([res["gender"], res["age"], res["emotions"]])
                else:
                    personID_list.append(res["personID"])
                    person_results_list.append( [[res["gender"], res["age"], res["emotions"]]])
        return person_results_list
    
    def is_a_new_person(self, person1):
        this_person_vector = person1.get_face_vector()
        smallest_diff_sq_sum_number =0
        if type(this_person_vector)==type([]):
            person_len = len(self.people_list)
            if person_len ==0:
                return True,  person_len
            diff_sq_sum_list = []
            for person in self.people_list:  #licze roznice dla kazdej osoby
                vector , i, diff_sq_sum= person.get_face_vector(), 0, 0
                for scalar in vector:
                    
                    this_person_scalar = this_person_vector[i]
                    if i==0 and self.time_makes_difference:
                        diff_sq_sum += self.time_importance*abs(this_person_scalar-scalar)
                    else: 
                        diff_sq_sum += abs(this_person_scalar-scalar)
                    i+=1
                diff_sq_sum_list.append(diff_sq_sum/float(len(this_person_vector)))
            #wybieram najnizsza sume roznic
            difference,  i =  None , 0
            for diff in diff_sq_sum_list:
                if i==0:difference = diff
                elif diff<difference: 
                    difference ,  smallest_diff_sq_sum_number = diff , i
                i+=1
            print difference #,  person1.face_size ,  vector
            if difference > self.new_person_tresh:
                return True , person_len
        return False  ,  smallest_diff_sq_sum_number
        
