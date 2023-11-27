from google.cloud import vision
import io

def detect_text(path):
    """從圖片中檢測文字"""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f'{response.error.message}')
    return response.text_annotations[0].description if response.text_annotations else ''
