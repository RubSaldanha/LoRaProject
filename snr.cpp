#include <iostream>
#include <string>
#include <cmath>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

double e_x = 0.0, e_r = 0.0, max_err = 0.0;
void energy_signals(Mat in, Mat res);
double getPSNR(Mat in, Mat res);
double snr();

int main (int argc, char** argv)
{

    if (argc != 3)
    {
        cerr << "Usage: ./snr <original> <noisy>" << endl;
        return -1;
    }

    Mat orig = imread(argv[argc-2],IMREAD_COLOR);
    Mat res = imread(argv[argc-1],IMREAD_COLOR);
    
    if (!orig.data){
        cout << "Could not open or find the original image" << endl;
        return -1;
    }
    if (!res.data){
        cout << "Could not open or find the noisy image" << endl;
        return -1;
    }
    // energy_signals(orig,res);
    // std::cout << "snr: " << snr() << endl;
    // std::cout << "Max_err: " << snr() << endl;
    std::cout << "PSNR: " << getPSNR(orig, res) << endl;
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

/* Compares two images and outputs the peak signal to noise ratio found in all the image's channels.
    More SNR means more similarity with original image*/
double getPSNR(Mat in, Mat res){
    double original_value = 0.0, reconstructed_value = 0.0, channel_err = 0.0, psnr = 0.0, snr = 0.0;
    int ch = in.channels();
    for (int i = 0; i < ch; i++){
        for (int j = 0; j < in.rows; j++){
            for (int k = 0; k < in.cols; k++){
                original_value = in.at<Vec3b>(j, k)[i];
                reconstructed_value = res.at<Vec3b>(j, k)[i];
                channel_err += pow(abs(original_value-reconstructed_value),2);
            }
        }
        channel_err = channel_err/(in.rows*in.cols);
        if (channel_err == 0)
            snr = 0.0;
        else  
            snr = 10 * log10(pow(255,2)/channel_err);

        channel_err = 0.0;
        cout << "snr: " << snr << endl;
        if (snr > psnr){
            psnr = snr;
        }
    }

    return psnr;

}


double snr(){
    return 10*log10(e_x/e_r);
}
double maxerr(){
    return max_err;
}