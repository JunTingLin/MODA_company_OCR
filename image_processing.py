import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  # 或者您安裝 Tesseract OCR 的實際路徑
from PIL import Image
import re
import os
from utils import numerical_sort

def auto_rotate_images_in_folder(folder_path, update_progress=None, update_status=None):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=numerical_sort)
    total_files = len(files)

    for index, filename in enumerate(files):
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
                print(f"已旋轉 {filename}...")
                if update_status:
                    update_status.emit(f"已旋轉 {filename}...")
            else:
                print(f"{filename} 無需旋轉...")
                if update_status:
                    update_status.emit(f"{filename} 無需旋轉...")

        except Exception as e:
            print(f"處理 {filename} 時出錯: {e}")
            if update_status:
                update_status.emit(f"處理 {filename} 時出錯: {e}")
        
        if update_progress:
            current_progress = (index + 1) * 100 // total_files
            update_progress.emit(current_progress)

