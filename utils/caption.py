from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


# function to get image caption
def get_caption(img):
    caption= computervision_client.describe_image_in_stream(img,language='en')
    return caption.captions[0].text # type: ignore
    
