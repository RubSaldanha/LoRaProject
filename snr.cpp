#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

double e_x = 0.0, e_r = 0.0, max_err = 0.0;
void energy_signals(Mat in, Mat res);
double snr();

int main (int argc, char** argv)
{

    if (argc != 3)
    {
        cerr << "Usage: ./ex6 <inFile_Path.ppm>" << endl;
        return -1;
    }
    Mat orig = imread(argv[argc-2],IMREAD_COLOR);
    Mat res = imread(argv[argc-1],IMREAD_COLOR);
    
    if (!orig.data){
        cout << "Could not open or find the image" << endl;
        return -1;
    }
    energy_signals(orig,res);
    std::cout << "snr: " << snr() << endl;
    std::cout << "Max_err: " << snr() << endl;
    return 0;
}

void energy_signals(Mat in, Mat res){
    int ch = in.channels();
    for (int j = 0; j < in.rows; j++)
        {
            for (int k = 0; k < in.cols; k++)
            {
                for (int i = 0; i < ch; i++)
                {
                    e_x += (in.at<Vec3b>(j, k)[i]^2);
                    e_r += (res.at<Vec3b>(j, k)[i]^2);
                    if(abs(in.at<Vec3b>(j, k)[i]-res.at<Vec3b>(j, k)[i])>max_err){
                        max_err = abs(in.at<Vec3b>(j, k)[i]-res.at<Vec3b>(j, k)[i]);
                     }
                }
            }
        }
}
double snr(){
    return 10*log10(e_x/e_r);
}
double maxerr(){
    return max_err;
}