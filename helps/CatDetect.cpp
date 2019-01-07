#include <opencv2/core/core.hpp>                        //Sposób 
#include <opencv2/highgui/highgui.hpp>                    //dokładny 
#include "opencv2/objdetect/objdetect.hpp" 
#include "opencv2/imgproc/imgproc.hpp" 
#include <string> 
#include <iostream> 

using namespace cv;
using namespace std;

string face_cascade_name = "cat_haar.xml";    //Nazwa kaskady którą wykorzystujemy do rozpoznania twarzy 
CascadeClassifier face_cascade;                                //Utworzenie obiektu cascady twarzy 
string window_name = "Hello Face !";
const string img_name = "3.jpg";

void detectFace(Mat img);

int main(int argc, char** argv)
{
	Mat img;                                            //Utworzenie nowej macierzy na nasz obrazek 
	img = imread(img_name);                            //Wczytanie obrazka z dysku 
	if (!img.data)                                    //Sprawdzenie czy ładowanie obrazka przebiegło pomyslnie 
	{
		cout << "Nie znaleziono pliku " << img_name << ".";
		return -1;
	}
	if (!face_cascade.load(face_cascade_name))        //Ładowanie pliku ze sprawdzeniem poprawnoci 
	{
		cout << "Nie znaleziono pliku " << face_cascade_name << ".";
		return -2;
	}
	namedWindow(window_name, WINDOW_AUTOSIZE);    //Utworzenie okna (nazwa okna, ustalenie rozmiaru) 
	detectFace(img);
	waitKey(0);                                            //Odczekanie na wcisnięce klawisza z opóźnieniem 0ms 
	return 0;
}

void detectFace(Mat img)
{
	vector<Rect> faces;                            //Utworzenie bufora na twarze 
	Mat img_gray;                                //Utworzenie bufora na obrazek w odcieniach szarosci 

	cvtColor(img, img_gray, COLOR_BGR2GRAY);                //Konwersja obrazu do odcieni szarosci 
	//equalizeHist(img_gray, img_gray);                    //Zaaplikowanie do obrazu jego historogramu, poprawa kontrastu 

	face_cascade.detectMultiScale(img_gray, faces, 1.1, 3, 0 | CASCADE_SCALE_IMAGE, Size(50, 50));
	for (unsigned i = 0; i < faces.size(); i++)
	{
		Rect rect_face(faces[i]);    //Kwadrat okreslający twarz 
		//ellipse( img, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 120, 12 ), 2, 2, 0 ); 
		rectangle(img, rect_face, Scalar(120, 5, 86), 2, 2, 0);
	}
	imshow(window_name, img);                        //Pokazanie obrazka w oknmie o nazwie "Hello Face !" 
}
