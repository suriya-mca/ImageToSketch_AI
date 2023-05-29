from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import cv2
import numpy as np
import base64

# router instance
router = APIRouter()

# template directory
templates = Jinja2Templates(directory="templates")

@router.post("/upload")
async def image_to_sketch(request: Request, file: UploadFile = File(...)) -> HTMLResponse:

	# Read the file
	contents = await file.read()

	# Convert the file to NumPy array
	nparr = np.fromstring(contents, np.uint8)

	# Decode the image data from NumPy array and image should be loaded in color (BGR) mode
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	# Convert image to grayscale
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Invert the grayscale image
	inverted_image = cv2.bitwise_not(gray_image)

	# Apply Gaussian blur to the inverted image
	blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)

	# Blend the grayscale image with the blurred inverted image using color
	pencil_sketch = cv2.divide(gray_image, 255 - blurred_image, scale=256.0)

	# Convert the image to PNG format
	_, buffer = cv2.imencode('.png', pencil_sketch)

	# Convert the image buffer to a Base64 string
	base64_image = base64.b64encode(buffer).decode('utf-8')

	return templates.TemplateResponse("view.html", {"request": request, "base64_image": base64_image})

