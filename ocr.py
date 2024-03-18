from google.cloud import vision
import io

def detect_text_from_picture(path):
    """從圖片中檢測文字"""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f'{response.error.message}')
    return response.text_annotations[0].description if response.text_annotations else ''

if __name__ == "__main__":
    image_path = r'C:\Users\junting\Desktop\ocr_data\data1\scan_test_all_頁面_01.jpg'
    text = detect_text_from_picture(image_path)
    print("識別的文字內容如下：")
    print(text)