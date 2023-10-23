import tensorflow as tf
import cv2
import numpy as np
from joblib import load
import matplotlib.pyplot as plt
model=tf.keras.models.load_model('utils/currency_model.h5',compile=False)
class_names=['1000_back',
  '1000_front',
  '100_back',
  '100_front',
  '10_back',
  '10_front',
  '20_back',
  '20_front',
  '5000_back',
  '5000_front',
  '500_back',
  '500_front',
  '50_back',
  '50_front',
  'others']
# function to load currency
def currency(img):
    img = np.array(img)
    # reshape the image to 224 x 224 pixels
    image = tf.image.resize(img, [224, 224])
    # expand dimensions
    image = tf.expand_dims(image, axis=0)
    # predict currency
    prediction = model.predict(image)
    # return currency
    return class_names[np.argmax(prediction)]
    

if __name__ == '__main__':
    # load image
    img = '100FRONT.jpg'
    # read image
    img = cv2.imread(img)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # get currency
    curren = currency(img)
    # print currency
    print(curren)
