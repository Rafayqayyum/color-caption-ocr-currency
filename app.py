from fastapi import FastAPI, File, UploadFile, status, Response
import uvicorn
from utils.ocr import ocr
from utils.caption import get_caption
from io import BytesIO
from PIL import Image
import numpy as np
from utils.pk_currency import currency
from utils.color import detect_colors, get_dominant_color
import logging

app = FastAPI()
MESSAGE = "message"
NO_IMAGE_FOUND = "No image found"
IMAGE_FORMAT_NOT_SUPPORTED = "Image format not supported"
SUPPORTED_FORMATS = ["jpg", "jpeg", "jfif", "png"]

# set CORS policy, so that the frontend can access the API
# https://fastapi.tiangolo.com/tutorial/cors/
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins
    allow_credentials=True,
    allow_methods=["*"], # allow all methods
    allow_headers=["*"], # allow all headers
)

# Read an image
def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    # read image to cv2 without changing color channels
    image=np.array(image)
    return image

@app.post('/captionapi')
async def caption_api(image: UploadFile=File(...), response: Response = None):
    #CHECK IF IMAGE IS UPLOADED
    if not image.filename or image.filename == "":
        #return status code and message
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { MESSAGE: NO_IMAGE_FOUND}
    #CHECK IF IMAGE IS IN SUPPORTED FORMAT
    ext=image.filename.split(".")[1] in SUPPORTED_FORMATS
    if not ext:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {MESSAGE: IMAGE_FORMAT_NOT_SUPPORTED}
    file=await image.read()
    image=BytesIO(file) 
    response.status_code = status.HTTP_200_OK
    return {MESSAGE: get_caption(image)}


@app.post('/ocrapi')
async def ocr_api(image: UploadFile=File(...), response: Response = None):
    #CHECK IF IMAGE IS UPLOADED
    if not image.filename or image.filename == "":
        #return status code and message
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {MESSAGE: NO_IMAGE_FOUND}
    #CHECK IF IMAGE IS IN SUPPORTED FORMAT
    ext=image.filename.split(".")[1] in SUPPORTED_FORMATS
    if not ext:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {MESSAGE: IMAGE_FORMAT_NOT_SUPPORTED}
    img=read_imagefile(await image.read())
    response.status_code = status.HTTP_200_OK
    return {MESSAGE: ocr(img)}

@app.post('/currencyapi')
async def currency_api(image: UploadFile=File(...), response: Response = None):
    #CHECK IF IMAGE IS UPLOADED
    if not image.filename or image.filename == "":
        #return status code and message
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { MESSAGE: NO_IMAGE_FOUND}
    #CHECK IF IMAGE IS IN SUPPORTED FORMAT
    ext=image.filename.split(".")[1] in SUPPORTED_FORMATS
    if not ext:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {MESSAGE: IMAGE_FORMAT_NOT_SUPPORTED}
    img=read_imagefile(await image.read())
    response.status_code = status.HTTP_200_OK
    return {MESSAGE: currency(img)}
    
@app.post('/colorapi')
async def color_api(image: UploadFile=File(...), response: Response = None):
    #CHECK IF IMAGE IS UPLOADED
    if not image.filename or image.filename == "":
        #return status code and message
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {MESSAGE: NO_IMAGE_FOUND}
    #CHECK IF IMAGE IS IN SUPPORTED FORMAT
    ext=image.filename.split(".")[1] in SUPPORTED_FORMATS
    if not ext:
        response.status_code = response.status_code
        return {MESSAGE: IMAGE_FORMAT_NOT_SUPPORTED}
    img=read_imagefile(await image.read())
    colors=detect_colors(img)
    # get the top 3 non zero percentage colors from colors dictionary
    colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)[:5]
    # remove the colors with 0 percentage
    colors = [color[0] for color in colors if color[1] != 0]
    # make a color string
    colors = ", ".join(colors)
    response.status_code = status.HTTP_200_OK
    return {MESSAGE: colors}


if __name__ == "__main__":
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("app.log")
    fh.setLevel(logging.DEBUG)
    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # set formatter to fh
    fh.setFormatter(formatter)
    # add file handler to logger
    logger.addHandler(fh)
    # run uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)

