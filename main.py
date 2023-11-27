from google.cloud import vision
import io

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return texts[0].description if texts else ''

def save_text_to_file(text, file_name):
    with open(file_name, 'w') as file:
        file.write(text)

# 使用示例
text_detected = detect_text('data\基本資料_16325089.jpg')
save_text_to_file(text_detected, 'output.txt')
