import cv2
import numpy as np
import pandas as pd
from PIL import Image

# hsv color bounds
color_bounds = {
    'red': [(0, 50, 50), (10, 255, 255)],
    'orange': [(11, 50, 50), (25, 255, 255)],
    'yellow': [(26, 50, 50), (35, 255, 255)],
    'green': [(36, 50, 50), (70, 255, 255)],
    'blue': [(71, 50, 50), (130, 255, 255)],
    'purple': [(131, 50, 50), (155, 255, 255)],
    'pink': [(156, 50, 50), (180, 255, 255)],
    'white': [(0, 0, 0), (180, 50, 255)],
    'black': [(0, 0, 0), (180, 255, 50)]
}


# function to detect colors in an image 
# returns {'color': percentage, ...}
def detect_colors(img):
    img = np.array(img)
    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # get image dimensions
    height, width, _ = img.shape
    # get image area
    area = height * width
    # initialize color counts
    color_counts = {}
    # loop through color bounds
    for color in color_bounds:
        # get lower and upper bounds
        lower, upper = color_bounds[color]
        # create mask
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        # count number of pixels in mask
        count = cv2.countNonZero(mask)
        # calculate percentage
        percentage = round(count / area * 100, 2)
        # add to color counts
        color_counts[color] = percentage
    # return color counts
    return color_counts


# function to get dominant color in an image
# returns 'color'
def get_dominant_color(img):
    img = np.array(img)
    # get color counts
    color_counts = detect_colors(img)
    # get dominant color
    dominant_color = max(color_counts, key=lambda x: color_counts[x])
    # return dominant color
    return dominant_color


if __name__=='__main__':
    # load image
    img = 'temp6.jpg'
    # read image
    img = cv2.imread(img)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # get dominant color
    color = get_dominant_color(img)
    print(detect_colors(img))
    # print dominant color
    print(color)

# import scipy.cluster
# import sklearn.cluster
# import numpy
# from PIL import Image

# def get_color_name(rgb_tuple):
#     df = pd.read_csv('utils/colors.csv',names=['Color Name','Hex','R','G','B'])
#     df['Dist-ances'] = df.apply(lambda row: numpy.sqrt((row['R']-rgb_tuple[0])**2 + (row['G']-rgb_tuple[1])**2 + (row['B']-rgb_tuple[2])**2), axis=1)
#     return df.loc[df['Dist-ances'].idxmin()]['Color Name']





# def dominant_colors(image):  # PIL image input

#     image = image.resize((150, 150))      # optional, to reduce time
#     ar = numpy.asarray(image)
#     shape = ar.shape
#     ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)

#     kmeans = sklearn.cluster.MiniBatchKMeans(
#         n_clusters=5,
#         init="k-means++",
#         max_iter=20,
#         random_state=1000
#     ).fit(ar)
#     codes = kmeans.cluster_centers_

#     vecs, _dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
#     counts, _bins = numpy.histogram(vecs, len(codes))    # count occurrences

#     colors = []
#     for index in numpy.argsort(counts)[::-1]:
#         colors.append(tuple([int(code) for code in codes[index]]))
#     return colors  

# if __name__=='__main__':
#     image = Image.open('temp6.jpg')
#     color_codes=dominant_colors(image)
#     # get color names
#     color_names=[]
#     for color in color_codes:
#         color_names.append(get_color_name(color))
#     print(color_names)
#     # print(color_codes)
#     # print(color_names)