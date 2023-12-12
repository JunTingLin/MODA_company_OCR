import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  # 或者您安裝 Tesseract OCR 的實際路徑
from PIL import Image
import re

def auto_rotate_image(filepath):
    # 使用OCR的OSD功能來檢測圖片方向
    image = Image.open(filepath)
    osd = pytesseract.image_to_osd(image)
    angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))
    
    # 如果檢測到的角度不是0，旋轉圖片
    if angle != 0:
        rotated_image = image.rotate(-angle, expand=True)
        rotated_image.save(filepath)  # 覆蓋原始圖片或保存為新的文件

# 假設您的圖片路徑如下
auto_rotate_image('scan_test_page_7.png')