"""Basic Video Processing methods."""
import os
from pickle import FALSE
import cv2


# Replace ID1 and ID2 with your IDs.
ID1 = '203200480'
ID2 = '320521461'

INPUT_VIDEO = 'atrium.avi'
GRAYSCALE_VIDEO = f'{ID1}_{ID2}_atrium_grayscale.avi'
BLACK_AND_WHITE_VIDEO = f'{ID1}_{ID2}_atrium_black_and_white.avi'
SOBEL_VIDEO = f'{ID1}_{ID2}_atrium_sobel.avi'


def get_video_parameters(capture: cv2.VideoCapture) -> dict:
    """Get an OpenCV capture object and extract its parameters.
    Args:
        capture: cv2.VideoCapture object. The input video's VideoCapture.
    Returns:
        parameters: dict. A dictionary of parameters names to their values.
    """
    fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    parameters = {"fourcc": fourcc, "fps": fps, "height": height, "width": width}
    return parameters


def convert_video_to_grayscale(input_video_path: str,
                               output_video_path: str) -> None:
    """Convert the video in the input path to grayscale.

    Use VideoCapture from OpenCV to open the video and read its
    parameters using the capture's get method.
    Open an output video using OpenCV's VideoWriter.
    Iterate over the frames. For each frame, convert it to gray scale,
    and save the frame to the new video.
    Make sure to close all relevant captures and to destroy all windows.

    Args:
        input_video_path: str. Path to input video.
        output_video_path: str. Path to output video.

    Additional References:
    (1) What are fourcc parameters:
    https://docs.microsoft.com/en-us/windows/win32/medfound/video-fourccs

    """
    """INSERT YOUR CODE HERE.
    REMOVE THE pass KEYWORD AND IMPLEMENT YOUR OWN CODE.
    """
    cap = cv2.VideoCapture(input_video_path)
    parameters = get_video_parameters(cap)
    ret,frame = cap.read()
    out = cv2.VideoWriter(output_video_path ,parameters['fourcc'],parameters['fps'],((frame.shape[1], frame.shape[0])), isColor=False)
    # running the loop 
    while cap.isOpened(): 
  
        # extracting the frames 
        ret, img = cap.read() 

        # converting to gray-scale 
        

        if ret:
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            # displaying the video 
            cv2.imshow("Live", gray) 
            # write to gray-scale 
            out.write(gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    

    cv2.destroyAllWindows() 
    cap.release()



def convert_video_to_black_and_white(input_video_path: str,
                                     output_video_path: str) -> None:
    """Convert the video in the input path to black and white.

    Use VideoCapture from OpenCV to open the video and read its
    parameters using the capture's get method.
    Open an output video using OpenCV's VideoWriter.
    Iterate over the frames. For each frame, first convert it to gray scale,
    then use OpenCV's THRESH_OTSU to slice the gray color values to
    black (0) and white (1) and finally convert the frame format back to RGB.
    Save the frame to the new video.
    Make sure to close all relevant captures and to destroy all windows.

    Args:
        input_video_path: str. Path to input video.
        output_video_path: str. Path to output video.

    Additional References:
    (1) What are fourcc parameters:
    https://docs.microsoft.com/en-us/windows/win32/medfound/video-fourccs

    """
    """INSERT YOUR CODE HERE.
        REMOVE THE pass KEYWORD AND IMPLEMENT YOUR OWN CODE.
        """
    cap = cv2.VideoCapture(input_video_path)
    parameters = get_video_parameters(cap)
    ret,frame = cap.read()
    out = cv2.VideoWriter(output_video_path ,parameters['fourcc'],parameters['fps'],((frame.shape[1], frame.shape[0])), isColor=False)
    # running the loop 
    while cap.isOpened(): 
  
        # extracting the frames 
        ret, img = cap.read() 

        # converting to gray-scale 
        

        if ret:
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
             ### Binarization ###
            _, image_edit = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            RGB = cv2.cvtColor(image_edit, cv2.COLOR_GRAY2RGB) 
            # displaying the video 
            cv2.imshow("Live", RGB) 
            # write to black-white 
            out.write(RGB)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    

    cv2.destroyAllWindows() 
    cap.release()


def convert_video_to_sobel(input_video_path: str,
                           output_video_path: str) -> None:
    """Convert the video in the input path to sobel map.

    Use VideoCapture from OpenCV to open the video and read its
    parameters using the capture's get method.
    Open an output video using OpenCV's VideoWriter.
    Iterate over the frames. For each frame, first convert it to gray scale,
    then use OpenCV's THRESH_OTSU to slice the gray color values to
    black (0) and white (1) and finally convert the frame format back to RGB.
    Save the frame to the new video.
    Make sure to close all relevant captures and to destroy all windows.

    Args:
        input_video_path: str. Path to input video.
        output_video_path: str. Path to output video.

    Additional References:
    (1) What are fourcc parameters:
    https://docs.microsoft.com/en-us/windows/win32/medfound/video-fourccs

    """
    """INSERT YOUR CODE HERE.
        REMOVE THE pass KEYWORD AND IMPLEMENT YOUR OWN CODE.
        """
    cap = cv2.VideoCapture(input_video_path)
    parameters = get_video_parameters(cap)
    ret,frame = cap.read()
    out = cv2.VideoWriter(output_video_path ,parameters['fourcc'],parameters['fps'],((frame.shape[1], frame.shape[0])), isColor=False)
    scale = 1
    delta = 0
    ddepth = -1
    # running the loop 
    while cap.isOpened(): 
  
        # extracting the frames 
        ret, img = cap.read() 

        # converting to gray-scale 
        

        if ret:
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            grad_x = cv2.Sobel(gray, ddepth, dx=1, dy=1, ksize=5)#, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
            grad_y = cv2.Sobel(gray, ddepth,dx=1, dy=1, ksize=5)#, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)


            abs_grad_x = cv2.convertScaleAbs(grad_x)
            abs_grad_y = cv2.convertScaleAbs(grad_y)


            grad =cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0.5)
            RGB = cv2.cvtColor(grad, cv2.COLOR_GRAY2RGB)
            # displaying the video 
            cv2.imshow("Live", RGB) 
            # write to gray-scale 
            out.write(RGB)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    

    cv2.destroyAllWindows() 
    cap.release()


def main():
    convert_video_to_grayscale(INPUT_VIDEO, GRAYSCALE_VIDEO)
    convert_video_to_black_and_white(INPUT_VIDEO, BLACK_AND_WHITE_VIDEO)
    convert_video_to_sobel(INPUT_VIDEO, SOBEL_VIDEO)


if __name__ == "__main__":
    main()
