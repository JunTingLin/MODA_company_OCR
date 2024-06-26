import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  # 或者您安裝 Tesseract OCR 的實際路徑
from PIL import Image
import re
import os

def auto_rotate_images_in_folder(folder_path, filenames, updater=None):
    total_files = len(filenames)

    for index, filename in enumerate(filenames):
        filepath = os.path.join(folder_path, filename)
        try:
            # 使用OCR的OSD功能來檢測圖片方向
            image = Image.open(filepath)
            osd = pytesseract.image_to_osd(image)
            angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))

            # 如果檢測到的角度不是0，旋轉圖片
            if angle != 0:
                rotated_image = image.rotate(-angle, expand=True)
                rotated_image.save(filepath)  # 覆蓋原始圖片或保存為新的文件
                if updater: updater.update_status(f"{filename} 已旋轉...")
            else:
                if updater: updater.update_status(f"{filename} 無需旋轉...")

        except Exception as e:
            if updater: updater.update_status(f"處理 {filename} 時出錯: {e}")
        
        if updater: updater.update_progress((index + 1) * 100 // total_files)

