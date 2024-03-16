#include <nuttx/config.h>
#include <stdio.h>
#include <fcntl.h>

int camera_fd = -1;

int set_up_camera();

int main(int argc, char *argv[])
{
  printf("Good day, and Welcome!\n");
  if (set_up_camera() != 0) {
    printf("Camera setup failed\n");
    return -1; // Return non-zero value to indicate failure
  }
  return 0;
}


int set_up_camera()
{
  printf("Setting up the camera\n");
  camera_fd = open("/dev/video0", O_RDWR);
  if (camera_fd < 0)
  {
    printf("Error opening camera\n");
    return -1;
  }
  printf("Camera opened\n");
  return 0;
}
