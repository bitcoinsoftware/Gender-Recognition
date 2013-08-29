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

static void read_csv(const string& filename, vector<Mat>& images, vector<int>& labels, char separator = ';') {
    std::ifstream file(filename.c_str(), ifstream::in);
    if (!file) {
        string error_message = "No valid input file was given, please check the given filename.";
        CV_Error(CV_StsBadArg, error_message);
    }
    string line, path, classlabel;
    int i =0;
    while (getline(file, line)) {
        stringstream liness(line);
        getline(liness, path, separator);
        getline(liness, classlabel);
        if(!path.empty() && !classlabel.empty()) {
            images.push_back(imread(path, 0));
            cerr<<imread(path, 0).cols <<"  "<<imread(path, 0).rows<<"  "<<path<< "  "<<i<<"\n" ;
            i++;
            labels.push_back(atoi(classlabel.c_str()));
        }
    }
}

int main(int argc, const char *argv[]) {

    string path = string(argv[1]);
    string output_path = string(argv[2]);
    vector<Mat> images;
    vector<int> labels;
    // Read in the data (fails if no valid input filename is given, but you'll get an error message):
    try {
        read_csv(path, images, labels);
    } catch (cv::Exception& e) {
        cerr << "Error opening file \"" << path << "\". Reason: " << e.msg << endl;
        // nothing more we can do
        exit(1);
    }
    int im_width = images[0].cols;
    int im_height = images[0].rows;
    Ptr<FaceRecognizer> model = createFisherFaceRecognizer();
    model->train(images, labels);
    model->save(output_path);
    return 0;
}
