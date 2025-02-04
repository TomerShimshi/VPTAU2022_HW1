"""Harris Corner Detector."""
from cv2 import sqrt
import numpy as np
import cv2
from scipy import signal
from matplotlib import pyplot as plt
from torch import square


# Replace ID1 and ID2 with your IDs.
ID1 = '203200480'
ID2 = '320521461'

# Harris corner detector parameters - you may change them.
K = 0.025
CHECKERBOARD_THRESHOLD = 3e7
GIRAFFE_THRESHOLD = 4.5e9
BUTTERFLY_IMAGE = 'butterfly.jpg'

# Do not change the following constants:
# input images:
CHECKERBOARD_IMAGE = 'checkerboard.jpg'
GIRAFFE_IMAGE = 'giraffe.jpg'
# result images:
TEST_BLOCKS_FUNCTIONS_IMAGE = f'{ID1}_{ID2}_test_tiles_funcs.png'
IMAGE_AND_CORNERS = f'{ID1}_{ID2}_image_corners.png'
RESPONSE_BW_IMAGE = f'{ID1}_{ID2}_response_black_and_white.png'
RESPONSE_RGB_IMAGE = f'{ID1}_{ID2}_response_rgb.png'


def bgr_image_to_rgb_image(bgr_image: np.ndarray) -> np.ndarray:
    """Convert Blue-Green-Red image to Red-Green-Blue image.

    Args:
        bgr_image: np.ndarray of shape: (height, width, 3).

    Returns:
        rgb_image: np.ndarray of shape: (height, width, 3). Take the input
        image and in the third dimension, swap the first and last slices.
    """
    rgb_image = bgr_image.copy()
    
    """INSERT YOUR CODE HERE."""
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    return rgb_image


def black_and_white_image_to_tiles(arr: np.ndarray, nrows: int,
                                   ncols: int) -> np.ndarray:
    """Convert the image to a series of non-overlapping nrowsXncols tiles.

    Args:
        arr: np.ndarray of shape (h, w).
        nrows: the number of rows in each tile.
        ncols: the number of columns in each tile.
    Returns:
        ((h//nrows) * (w //ncols) , nrows, ncols) np.ndarray.
    Hint: Use only shape, reshape and swapaxes to implement this method.
    Take inspiration from: https://stackoverflow.com/questions/16873441/form-a-big-2d-array-from-multiple-smaller-2d-arrays
    """
    h, w = arr.shape
    """INSERT YOUR CODE HERE.
    REPLACE THE RETURNED VALUE WITH YOUR OWN IMPLEMENTATION.
    """
    #return np.random.uniform(size=((h//nrows) * (w //ncols), nrows, ncols))
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))



def image_tiles_to_black_and_white_image(arr: np.ndarray, h: int,
                                         w: int) -> np.ndarray:
    """Convert the series of tiles back to a hxw image.

    Args:
        arr: np.ndarray of shape (nTiles, nRows, nCols).
        h: the height of the original image.
        w: the width of the original image.
    Returns:
        (h, w) np.ndarray.
    Hint: Use only shape, reshape and swapaxes to implement this method.
    Take inspiration from: https://stackoverflow.com/questions/16873441/form-a-big-2d-array-from-multiple-smaller-2d-arrays
    """
    n, nrows, ncols = arr.shape
    """INSERT YOUR CODE HERE.
    REPLACE THE RETURNED VALUE WITH YOUR OWN IMPLEMENTATION.
    """
    #return np.random.uniform(size=(h, w))
    return (arr.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1,2)
               .reshape(h, w))


def test_tiles_functions(to_save: bool = False) -> None:
    """Show the butterfly image, its split to tiles and the reassembled
    image from tiles back to image."""
    butterfly_image = cv2.imread(BUTTERFLY_IMAGE, 0)
    plt.subplot(1, 3, 1)
    plt.title('original image')
    plt.imshow(butterfly_image, cmap='gray')
    plt.colorbar()
    tiles = black_and_white_image_to_tiles(butterfly_image, 25, 25)
    for i in range(4):
        for j in range(4):
            plt.subplot(4, 12, 8 * i + j + 1 + 4 * (i + 1))
            plt.imshow(tiles[4 * i + j], cmap='gray')
            plt.title(f'tile #{4 * i + j + 1}')
            plt.xticks([])
            plt.yticks([])

    height, width = butterfly_image.shape
    reassembled_image = image_tiles_to_black_and_white_image(tiles, height,
                                                              width)
    plt.subplot(1, 3, 3)
    plt.title('re-assembled image')
    plt.imshow(reassembled_image, cmap='gray')

    fig = plt.gcf()
    fig.set_size_inches((20, 7))
    if to_save:
        plt.savefig(TEST_BLOCKS_FUNCTIONS_IMAGE)
    else:
        plt.show()


def create_grad_x_and_grad_y(
        input_image: np.ndarray) :#-> tuple[np.ndarray, np.ndarray]:
    """Calculate the gradients across the x and y-axes.

    Args:
        input_image: np.ndarray. Image array.
    Returns:
        tuple (Ix, Iy): The first is the gradient across the x-axis and the
        second is the gradient across the y-axis.

    Recipe:
    If the image is an RGB image, convert it to grayscale using OpenCV's
    cvtColor. Otherwise, the input image is already in grayscale.
    Then, create a one pixel shift (to the right) image and fill the first
    column with zeros.
    Ix will be the difference between the grayscale image and the shifted
    image.
    Iy will be obtained in a similar manner, this time you're requested to
    shift the image from top to bottom by 1 row. Fill the first row with zeros.
    Finally, in order to ignore edge pixels, remove the first column from Ix
    and the first row from Iy.
    Return (Ix, Iy).
    """
    # Get image dimensions
    if len(input_image.shape) == 2:
        # this is the case of a black and white image
        nof_color_channels = 1
        height, width = input_image.shape

    else:
        # this is the case of an RGB image
        nof_color_channels = 3
        height, width, _ = input_image.shape

    """INSERT YOUR CODE HERE.
    REPLACE THE VALUES FOR Ix AND Iy WITH THE GRADIENTS YOU COMPUTED.
    """
    if nof_color_channels == 3:
       input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY) 
    added_x = np.zeros(input_image.shape[0])
    added_y = np.zeros(input_image.shape[1])
    #offset_x = np.concatenate((added_x,input_image[:,:-1]),axis= 0,casting="same_kind")
    #offset_x = np.hstack((added_x,input_image[:,:-1]))
    #offset_y = np.column_stack((added_y,input_image[:-1,:]))
    offset_y = np.vstack((added_y,input_image[:-1,:]))
    #offset_x = np.row_stack((added_x,input_image[:,:-1]))
    offset_x = np.column_stack((added_x,input_image[:,:-1]))
    #offset_x = np.hstack((added_x,input_image[:-1,:]))

    Ix = input_image - offset_x
    Iy = input_image - offset_y
    Iy= np.vstack((added_y,Iy[1:,:]))#Iy[1:,:]
    Ix=  np.column_stack((added_x,Ix[:,1:]))#Ix[:,1:]
    #Ix = np.random.uniform(size=(height, width))
    #Iy = np.random.uniform(size=(height, width))
    return Ix, Iy


def calculate_response_image(input_image: np.ndarray, K: float) -> np.ndarray:
    """Calculate the response image for input_image with the parameter K.

    Args:
        input_image: np.ndarray. Image array.
        K: float. the K from the equation: R ≈ det(M) −k∙[trace(M)] ^2
    Returns:
        response_image: np.ndarray of shape (h,w). The response image is R:
        R ≈ det(M) −k∙[trace(M)] ^2.

    Recipe:
    Compute the image gradient using the method create_grad_x_and_grad_y.
    The response image is given by:  R ≈ det(M) −k∙[trace(M)] ^2
    where:
        det(M) = Sxx ∙ Syy - Sxy^2
        trace(M) = Sxx + Syy
        Sxx = conv(Ix^2, g)
        Syy = conv(Iy^2, g)
        Sxy = conv(Ix ∙ Iy, g)
    Convolutions are easy to compute with signal.convolve2d method. The
    kernel g should be 5x5 ones matrix, and the mode for the convolution
    method should be 'same'.
    Hint: Use np.square, np.mutiply when needed.
    """
    # compute Ix and Iy
    Ix, Iy = create_grad_x_and_grad_y(input_image)

    """INSERT YOUR CODE HERE.
    REPLACE THE resonse_image WITH THE RESPONSE IMAGE YOU CALCULATED."""
    kernel = np.ones((5,5))
    Sxx = signal.convolve2d(np.square(Ix),kernel,mode= 'same')
    Syy = signal.convolve2d(np.square(Iy),kernel,mode= 'same')
    Sxy = signal.convolve2d(np.multiply(Ix,Iy),kernel,mode= 'same')
    detM = np.multiply(Sxx,Syy)- np.square(Sxy)
    TraceM = Sxx + Syy
    response_image = detM - K* (np.square(TraceM))
    return response_image


def our_harris_corner_detector(input_image: np.ndarray, K: float,
                               threshold: float) -> np.ndarray:
    """Calculate the corners for input image with parameters K and threshold.
    Args:
        input_image: np.ndarray. Image array.
        K: float. the K from the equation: R ≈ det(M) −k∙[trace M] ^2
        threshold: float. minimal response value for a point to be detected
        as a corner.
    Returns:
        output_image: np.ndarray with the height and width of the input
        image. This should be a binary image with all zeros except from ones
        in pixels with corners.
    Recipe:
    (1) calculate the response image from the input image and the parameter K.
    (2) apply Non-Maximal Suppression per 25x25 tile:
     (2.1) convert the response image to  tiles of 25x25.
     (2.2) For each tile, create a new tile which is all zeros except from
     one value - the maximal value in that tile. Keep the maximal value in
     the same position it was in the original tile.
     Hint: use np.argmax to find the index of the largest response value in a
     tile and read about (and use): np.unravel_index.
    (3) Convert the result tiles-tensor back to an image. Use
    the method: image_tiles_to_black_and_white_image.
    (4) Create a zeros matrix of the shape of the original image, and place
    ones where the image from (3) is larger than the threshold.
    """
    response_image = calculate_response_image(input_image, K)
    """INSERT YOUR CODE HERE.
    REPLACE THE output_image WITH THE BINARY MAP YOU COMPUTED."""
    #first convert to tiles
    #if len(input_image.shape) > 2:
      # response_image = cv2.cvtColor(response_image, cv2.COLOR_RGB2GRAY)  
    tiles= black_and_white_image_to_tiles(response_image,25,25)
    new_tiles= np.zeros(tiles.shape)
    shoof = tiles.shape[0]
    for i in range(shoof):
        tile = tiles[i]
        index = np.argmax(tile)
        new_tile_index= np.unravel_index(index,tile.shape,order= 'C')
        temp =tile[new_tile_index]
        new_tiles[i,new_tile_index[0],new_tile_index[1]]=tile[new_tile_index]
    h,w = response_image.shape
    new_image = image_tiles_to_black_and_white_image(new_tiles,h,w)
    output_image = np.zeros(response_image.shape)
    output_image = np.where(new_image > threshold,1,0)
    idx1 = np.nonzero(output_image)
    idx1=list( zip(idx1[0],idx1[1]))
    i=0
    count1 = len(idx1) 
    #print('idx1 = {}'.format(idx1))
    
        
    while (i<len(idx1)):
        j=0
        idx2 = np.nonzero(output_image)
        idx2=list( zip(idx2[0],idx2[1]))
        while (j<len(idx2)):

            delta = np.abs(idx1[i][0]- idx2[j][0])+ np.abs(idx1[i][1]- idx2[j][1]) #np.sqrt(np.abs(idx[i][0]- idx[j][0])**2+ np.abs(idx[i][1]- idx[j][1])**2)
            temp1 =idx2[j] 
            temp2 =idx1[i]
            if delta <=10 and delta != 0:
                 
                if response_image[idx1[i][0],idx1[i][1]]<=response_image[idx2[j][0],idx2[j][1]]: 
                    output_image[idx1[i][0],idx1[i][1]] = 0
                else:
                    output_image[idx2[j][0],idx2[j][1]] = 0 
                j+=2
            else:
                j+=1
        i+=1
    '''  
    idx = np.nonzero(output_image)
    idx=list( zip(idx[0],idx[1]))
    count2 = len(idx)
    print('idx2 = {}'.format(idx))
    '''


    return output_image


def plot_response_for_black_an_white_image(input_image: np.ndarray,
                                           response_image: np.ndarray,
                                           to_save: bool = False) -> None:
    """Plot the original black and white image, the response image and a
    Zoom-in on an interesting region."""
    plt.subplot(1, 3, 1)
    plt.title('original image')
    plt.imshow(input_image, cmap='gray')
    plt.subplot(1, 3, 2)
    plt.title('response image')
    plt.imshow(response_image, cmap='jet')
    plt.colorbar()
    plt.subplot(1, 3, 3)
    plt.title('response image - zoom in\n on (130:170, 230:270)')
    plt.imshow(response_image[130:170, 230:270], cmap='jet')
    plt.colorbar()
    fig = plt.gcf()
    fig.set_size_inches((14, 7))
    if to_save:
        plt.savefig(RESPONSE_BW_IMAGE)
    else:
        plt.show()


def plot_response_for_rgb_image(input_image: np.ndarray,
                                response_image: np.ndarray,
                                to_save: bool = False) -> None:
    """Plot the original RGB image, the response image and a Zoom-in on an
    interesting region."""
    plt.subplot(1, 3, 1)
    plt.title('original image')
    plt.imshow(bgr_image_to_rgb_image(input_image))
    plt.subplot(1, 3, 2)
    plt.title('response image')
    plt.imshow(response_image, cmap='jet')
    plt.colorbar()
    plt.subplot(1, 3, 3)
    plt.title('response image - zoom in\n on (40:120, 420:500)')
    plt.imshow(response_image[40:120, 420:500], cmap='jet')
    plt.colorbar()
    fig = plt.gcf()
    fig.set_size_inches((14, 7))
    if to_save:
        plt.savefig(RESPONSE_RGB_IMAGE)
    else:
        plt.show()


def create_corner_plots(black_and_white_image: np.ndarray,
                        black_and_white_image_corners: np.ndarray,
                        grb_image: np.ndarray,
                        rgb_image_corners: np.ndarray,
                        to_save: bool = False) -> None:
    """Plot the two images with the corners in the same plot."""
    plt.subplot(1, 2, 1)
    plt.imshow(black_and_white_image, cmap='gray')
    corners = np.where(black_and_white_image_corners == 1)
    plt.plot(corners[1], corners[0], 'ro')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    rgb_image = bgr_image_to_rgb_image(grb_image)
    plt.imshow(rgb_image)
    corners = np.where(rgb_image_corners == 1)
    plt.plot(corners[1], corners[0], 'ro')
    plt.axis('off')
    fig = plt.gcf()
    fig.set_size_inches((14, 7))
    if to_save:
        plt.savefig(IMAGE_AND_CORNERS)
    else:
        plt.show()


def main(to_save: bool = False) -> None:
    test_tiles_functions(to_save)
    # Read checkerboard image as grayscale
    checkerboard = cv2.imread(CHECKERBOARD_IMAGE, 0)
    # Read giraffe image
    giraffe = cv2.imread(GIRAFFE_IMAGE)

    # checkerboard response image
    checkerboard_response_image = calculate_response_image(checkerboard, K)
    plot_response_for_black_an_white_image(checkerboard,
                                           checkerboard_response_image,
                                           to_save)

    # giraffe response image
    giraffe_response_image = calculate_response_image(giraffe, K)
    plot_response_for_rgb_image(giraffe, giraffe_response_image, to_save)

    # CALL YOUR FUNCTION TO FIND THE CORNER PIXELS
    checkerboard_corners = our_harris_corner_detector(checkerboard, K,
                                                      CHECKERBOARD_THRESHOLD)
    giraffe_corners = our_harris_corner_detector(giraffe, K, GIRAFFE_THRESHOLD)

    # create the output plot.
    create_corner_plots(checkerboard, checkerboard_corners, giraffe,
                        giraffe_corners, to_save)


if __name__ == "__main__":
    main(to_save=True)
