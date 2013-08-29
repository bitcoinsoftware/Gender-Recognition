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

using namespace cv;
using namespace std;
//int im_width =  180;
//int im_height = 180;

string int2str(int number)
{
   stringstream ss;//create a stringstream
   ss << number;//add number to the stream
   return ss.str();//return a string with the contents of the stream
}

int main(int argc, const char *argv[]) {

    Mat image;
    image = imread( argv[2], 1 );

    if( argc != 5 || !image.data )
    {
    cout << " No image data \n";
    cout << "usage:   ./face_classifier <url_to_casscade_classyfier> <url_to_face_image>" << endl;
    return -1;
    }
    string url ,out_url,width, height;
    url = argv[2];
    out_url = argv[1];
    width = argv[3];
    height = argv[4];
    int im_width = atoi(width.c_str());
    int im_height = atoi(height.c_str());
    string text_file_url = url+ ".txt";
    Mat graySample;
    cvtColor( image, graySample, CV_RGB2GRAY );
    Mat face_resized;
    cv::resize(graySample, face_resized, Size(im_width, im_height), 1.0, 1.0, INTER_CUBIC);
    // Now perform the prediction, see how easy that is:
    Ptr<FaceRecognizer> model = createFisherFaceRecognizer();
    model->load(out_url);
    int prediction = model->predict(face_resized);
    fstream File;
    File.open(text_file_url.c_str(), ios::out);
    File<< int2str(prediction);
    File.close();
    return 0;
}
