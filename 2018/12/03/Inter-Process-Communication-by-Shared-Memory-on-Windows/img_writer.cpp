#include <Windows.h>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>
#include <opencv2\core\core.hpp>
#include <opencv2\highgui\highgui.hpp>

using namespace std;
using namespace cv;

//struct MyData
//{
//	int width;
//	int height;
//	int channel;
//	MyData(int _width, int _height, int _channel) : width(_width), height(_height), channel(_channel)
//	{}
//};

void writeMemory(char* imgDir)
{
	// define shared data
	char *shared_file_name = "file_name_sean";
	char * shared_object_name = "Local\\object_name_sean";

	Mat img = imread(imgDir, IMREAD_COLOR);

	int width = img.cols;
	int height = img.rows;
	int channel = img.channels();
	uchar* img_data = img.data;

	unsigned long data_size = sizeof(uchar) * width * height * channel;
	unsigned long buffer_size = data_size + 3 * sizeof(int);

	cout << "share buffer " << endl;

	// create shared memory file
	HANDLE hFile = CreateFile(shared_file_name,
		GENERIC_READ | GENERIC_WRITE,
		FILE_SHARE_READ | FILE_SHARE_WRITE,
		NULL,
		OPEN_ALWAYS, // open exist or create new, overwrite file
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	if (hFile == INVALID_HANDLE_VALUE)
		cout << "create file error" << endl;

	HANDLE shared_file_handler = CreateFileMapping(
		hFile, // Use paging file - shared memory
		NULL,                 // Default security attributes
		PAGE_READWRITE,       // Allow read and write access
		0,                    // High-order DWORD of file mapping max size
		buffer_size,            // Low-order DWORD of file mapping max size
		shared_object_name);    // Name of the file mapping object

	if (shared_file_handler) {
		// map memory file view, get pointer to the shared memory
		LPVOID lp_base = MapViewOfFile(
			shared_file_handler,  // Handle of the map object
			FILE_MAP_ALL_ACCESS,  // Read and write access
			0,                    // High-order DWORD of the file offset
			0,                    // Low-order DWORD of the file offset
			buffer_size);           // The number of bytes to map to view

		
		// write width, height, channel to a memory
		uchar* tmp = (uchar*) malloc(buffer_size);
		memcpy(tmp, &width, sizeof(width));
		tmp += sizeof(width);
		memcpy(tmp, &height, sizeof(height));
		tmp += sizeof(height);
		memcpy(tmp, &channel, sizeof(channel));
		tmp += sizeof(channel);
		memcpy(tmp, img.data, data_size);

		for (int i = 0; i < 10; i++) {
			uchar val = tmp[i];
			cout << (int)val << endl;
		}

		// copy data to shared memory
		tmp -= sizeof(int) * 3;
		memcpy(lp_base, tmp, buffer_size);

		free(tmp);

		FlushViewOfFile(lp_base, buffer_size); // can choose save to file or not
		
		// process wait here for other task to read data
		cout << "already write to shared memory, wait ..." << endl;

		this_thread::sleep_for(chrono::seconds(6000));

		// close shared memory file
		UnmapViewOfFile(lp_base);
		CloseHandle(shared_file_handler);
		CloseHandle(hFile);
		//unlink(shared_file_name);
		cout << "shared memory closed" << endl;
	} else
		cout << "create mapping file error" << endl;
}


int main(int argc, char* argv[]) {
	char* imgDir = "C:/Users/taoxuan.G08/Documents/Visual Studio 2015/Projects/cnpy-solution/cv/vehicle.jpeg";
	writeMemory(imgDir);

	return 0;
}