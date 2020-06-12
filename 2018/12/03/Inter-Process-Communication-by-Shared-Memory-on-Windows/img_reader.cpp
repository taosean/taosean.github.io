#include <iostream>
#include <string>
#include <Windows.h>
#include <opencv2\core\core.hpp>
#include <opencv2\highgui\highgui.hpp>

using namespace std;
using namespace cv;

void readMemory()
{
	char *shared_object_name = "Local\\object_name_sean";

	// open shared memory file
	HANDLE shared_file_handler = OpenFileMapping(
		FILE_MAP_ALL_ACCESS,
		NULL,
		shared_object_name);

	if (shared_file_handler) {

		LPVOID lp_base = MapViewOfFile(
			shared_file_handler,
			FILE_MAP_ALL_ACCESS,
			0,
			0,
			0);

		// copy shared data from memory
		cout << "read shared data: " << endl;

		uchar* tmp = (uchar*)lp_base;
		int width;
		int height;
		int channel;
		memcpy(&width, tmp, sizeof(width));
		tmp += sizeof(int);
		memcpy(&height, tmp, sizeof(height));
		tmp += sizeof(int);
		memcpy(&channel, tmp, sizeof(channel));
		tmp += sizeof(int);

		Mat img = Mat(height, width, CV_8UC3);
		memcpy(img.data, tmp, height * width * channel);

		namedWindow("test");
		imshow("test", img);
		waitKey(2);


		// close share memory file
		UnmapViewOfFile(lp_base);
		CloseHandle(shared_file_handler);

	} else
		cout << "open mapping file error" << endl;
}

int main(int argc, char* argv[]) {
	readMemory();

	system("pause");
	return 0;
}