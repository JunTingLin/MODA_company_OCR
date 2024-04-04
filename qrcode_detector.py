import cv2
from typing import List

def detect_qr_codes(image_path: str) -> List[str]:
    # 初始化 QRCodeDetector
    detector = cv2.QRCodeDetector()

    # 讀取圖片
    image = cv2.imread(image_path)

    # 檢測並解碼圖片中的 QR Code
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(image)

    # 檢查是否成功檢測到 QR Code
    if not retval:
        # 如果未檢測到任何 QR Code，返回空陣列
        return []

    # 使用 set 去重，然後將結果轉為 list 返回
    unique_links = list(set(decoded_info))

    # 返回解碼後的不重複 QR Code 連結陣列
    return unique_links


if __name__ == '__main__':
    image_path = r'C:\Users\junting\Desktop\ocr_data\quotation\2024-03-21-161819 - copy-black.jpg'
    # image_path = r'C:\Users\junting\Desktop\ocr_data\data3(company)\SCAN-20231215154840_1-2_page_7.jpg'
    qr_links = detect_qr_codes(image_path)
    print("QR Code Links:", qr_links)
    print(type(qr_links))
