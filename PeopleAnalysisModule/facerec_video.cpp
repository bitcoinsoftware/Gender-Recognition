/*
 * Copyright (c) 2011. Philipp Wagner <bytefish[at]gmx[dot]de>.
 * Released to public domain under terms of the BSD Simplified license.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   * Neither the name of the organization nor the names of its contributors
 *     may be used to endorse or promote products derived from this software
 *     without specific prior written permission.
 *
 *   See <http://www.opensource.org/licenses/bsd-license>
 */

#include "opencv2/core/core.hpp"
#include "opencv2/contrib/contrib.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/objdetect/objdetect.hpp"

#include <iostream>
#include <fstream>
#include <sstream>
#include <time.h>
#include <cstdlib>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>

using namespace cv;
using namespace std;

string plik_csv="  ";
string klasyfikator_twarzy="  ";
string klasyfikator_dol="  ";
string klasyfikator_gora="  ";
int co_ile_analizowac=4;
int delta_x =10;
int prog_pewnosci_gora=10;
int prog_pewnosci_dol=10;
int id_kamery=0;

Rect_<int> nose, r_eye, l_eye, mouth;
string images_data_text;


//vector <int> sectors;


bool can_continue(const string& filename) {
    std::ifstream file(filename.c_str(), ifstream::in);
    if (!file) {
        string error_message = "No valid input file was given, please check the given filename.";
        CV_Error(CV_StsBadArg, error_message);
    }
    string line;
    while (getline(file, line)) {
        //#stringstream liness(line);
        if(line=="True"){return true;}
        else {return false;}
    }
}

/*function... might want it in some class?*/
int getdir (string dir, vector<string> &files)
{
    DIR *dp;
    struct dirent *dirp;
    if((dp  = opendir(dir.c_str())) == NULL) {
        cout << "Error(" << errno << ") opening " << dir << endl;
        return errno;
    }

    while ((dirp = readdir(dp)) != NULL) {
        files.push_back(string(dirp->d_name));
    }
    closedir(dp);
    return 0;
}

string int2str(int number)
{
   stringstream ss;//create a stringstream
   ss << number;//add number to the stream
   return ss.str();//return a string with the contents of the stream
}

bool chceck_if_face_matrix_is_valid(Mat face_image,Mat colored_face_image, Rect_<int> face_i, int face_number, int display_faces){
    string nose_haar = "haarcascades/haarcascade_mcs_nose.xml";
    string mouth_haar = "haarcascades/haarcascade_mcs_mouth.xml";

    string face_number_str = int2str(face_number);
    string url = "tmp/face"+face_number_str +".jpg";
    string url_upp = "tmp/faceupp"+ face_number_str+".jpg";
    string url_low = "tmp/facelow"+ face_number_str+".jpg";
    //CascadeClassifier nose_cascade;
    CascadeClassifier nose_cascade;
    nose_cascade.load(nose_haar);

    CascadeClassifier mouth_cascade;
    mouth_cascade.load(mouth_haar);

    vector< Rect_<int> > det_noses, det_elem;
    nose_cascade.detectMultiScale(face_image, det_noses);
    mouth_cascade.detectMultiScale(face_image, det_elem);
    if (det_noses.size()>0 && det_elem.size()>2)
        {

        ::images_data_text+="face"+face_number_str;
        ::images_data_text+=":["+int2str(face_i.x) +","+int2str(face_i.y)+","+int2str(face_i.width)+","+int2str(face_i.height)+"]\n";
        //liczenie koloru twarzy ponad nosem
        //cerr << *colored_face_image.size[0] <<*colored_face_image.size[1];

        Rect_<int> *upper_f = new Rect_<int>(0,0,colored_face_image.size[0], colored_face_image.size[1]/2 );
        Rect_<int> *lower_f = new Rect_<int>(0, colored_face_image.size[1]/2, colored_face_image.size[0], colored_face_image.size[1]/2);
        Mat colored_face_upper = colored_face_image(*upper_f);
        Mat colored_face_lower = colored_face_image(*lower_f);

        imwrite( url.c_str(), colored_face_image );
        imwrite( url_upp.c_str(), colored_face_upper );
        imwrite( url_low.c_str(), colored_face_lower );
        string window_name = "face"+face_number_str;
        if (display_faces==1){imshow(window_name.c_str(),colored_face_image);}

        int nose_size  = det_noses.size();
        int mouth_size = det_elem.size();
        string line="";
        ::images_data_text+="NOSE:[";

        line= "["+int2str(det_noses[0].x)+","+int2str(det_noses[0].y)+","+int2str(det_noses[0].width)+","+int2str(det_noses[0].height)+"]";
        ::images_data_text+=line;

        ::images_data_text+="]\nPOINTS:[";
        //::images_data_text+="[";
        //cerr<< det_elem.size()<<"   ilosc elementow";
        for (int i=0; i<det_elem.size();i++)
        {   if(i!=0){::images_data_text+=",";}
            line = "["+int2str(det_elem[i].x)+","+int2str(det_elem[i].y)+","+int2str(det_elem[i].width)+","+int2str(det_elem[i].height)+"]";
            ::images_data_text+=line;
        }

        ::images_data_text+="]";

        return true;
        }
}


int main(int argc, const char *argv[]) {

    if (argc != 3) {
        cout << "usage: " << argv[0] << " </path/to/device id>  <display faces (1 or 0)>  " << endl;
        //cout << "\t <device id> -- The webcam device id to grab frames from." << endl;
        exit(1);
    }
    // Get the path to your CSV:
    string fn_haar = "haarcascades/haarcascade_frontalface_default.xml";
    int deviceId = atoi(argv[1]);
    //int horizontal_sectors = atoi(argv[2]);
    //int vertical_sectors = atoi(argv[3]);
    int display_faces = atoi(argv[2]);

    bool faces_validation_vector [256]; for (int i =0; i<256;i++){faces_validation_vector[i]=0;}
    int previous_faces_ammount=0;
    Mat previous_faces[256];

    CascadeClassifier haar_cascade;
    haar_cascade.load(fn_haar);
    VideoCapture cap(deviceId);
    //int width  = ; int height = ;
    int cam_resolution[] = {cap.get(CV_CAP_PROP_FRAME_WIDTH),cap.get(CV_CAP_PROP_FRAME_HEIGHT)};
    //cerr<< cam_resolution[0];
    // Check if we can use this device at all:
    if(!cap.isOpened()) {
        cerr << "Capture Device ID " << deviceId << "cannot be opened." << endl;
        return -1;
    }
    // Holds the current frame from the Video device:
    Mat frame;
    int sito =1;
    int i=0;
    bool show_main_view = true; 
    //stringstream ss;
    //string url;

    IplImage stub, *dst_img;
    IplImage *img2;
   for(;;)
     {
        ::images_data_text = "";
        i++;
        // sprawdza czy moze kontynuowac
        if (i==10)  {i=0; if(can_continue("should_stop.txt")){break;}}
        sito++;
        if (i%4==0)  //co 4 klatke moze jechac ale jedziemy po kazdej
            {
            cap >> frame;
            imshow("main", frame);
            Mat original = frame.clone();
            Mat gray;
            //Mat colored_face;
            cvtColor(original, gray, CV_BGR2GRAY);
            vector< Rect_<int> > faces;
            haar_cascade.detectMultiScale(gray, faces);
            
            //do tad git
            

            if (sito ==10)
            {
                sito=0;
                string dir = string("tmp");
                vector<string> files = vector<string>();
                getdir(dir,files);
                for (int i=0;i<files.size();i++){remove((dir +"/"+files[i]).c_str());}
                if(display_faces==1){destroyAllWindows();}
            }
            /*
            for (int i =0;i>previous_faces_ammount;i++){
                if (faces_validation_vector[i])
                    {
                    string name = "face"+int2str(i);
                    destroywindow(name.c_str());
                    cvReleaseImage(previous_faces[i]);
                    }
            }*/



            for(int i = 0; i < faces.size(); i++) {  //sledzenie twarzy
                //cout << faces[i][0]<<endl;
                // Process face by face:
                Rect facjata = faces[i];
                
                int a, b,c,d;
                a = (facjata.x-facjata.width/8);
                b = (facjata.y-facjata.height/8);
                c = (facjata.width+facjata.width/8);
                d = (facjata.height+facjata.height/8);
                if (a<0){a=0;}
                if (b<0){b=0;}
                if (c>=cam_resolution[0]-a){c=cam_resolution[0]-a-1;}
                if (d>=cam_resolution[1]-b){d=cam_resolution[1]-b-1;}
                cout<<endl<<facjata.x<<" "<<facjata.y<<" "<<facjata.width<<" "<<facjata.height<<endl;
                cout <<a <<" "<<b<<" "<<c<<" "<<" "<<d<<endl;
                
                //Rect * face_i1 = new Rect(a,b,c,d);
                Rect_<int> *face_i1 = new Rect_<int>(a,b,c,d);
                Rect face_i = *face_i1;
                Mat face = gray(face_i);
                //Mat face_resized;
                Mat colored_face = original(face_i);
                //int prediction = 10;
                faces_validation_vector[i] = chceck_if_face_matrix_is_valid(face, colored_face, face_i, i,display_faces);
                //previous_faces[i] = colored_face;
            }
            previous_faces_ammount = faces.size();
            time_t czas;
            time( & czas );

            ::images_data_text= int2str(czas) +"\n"+::images_data_text;

            fstream File;
            File.open("images_data", ios::out);
            File << ::images_data_text.c_str();
            File.close();
            cerr<< ::images_data_text;
            cerr<<"\n";

            char key = (char) waitKey(100);
            // Exit this loop on escape:
            if(key == 27)
                break;
        }

    }


    return 0;
}
