import cv2

def is_checked(image_path, check_coords):
    """
    檢查指定位置是否有打勾。

    :param image_path: 圖像文件的路徑
    :param check_coords: 檢查點的坐標，格式為 [(x1, y1, w1, h1), (x2, y2, w2, h2), ...]
    :return: 每個坐標點是否打勾的布爾值列表
    """
    # 讀取圖像
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    results = []
    for (x, y, w, h) in check_coords:
        # 擷取特定區域
        roi = gray[y:y+h, x:x+w]
        # 應用閾值來檢測勾選
        _, threshold = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY_INV)
        count = cv2.countNonZero(threshold)

        # 如果該區域有足夠的黑色像素，則認為是打勾
        if count > 50:  # 50是一個示例閾值，可能需要根據您的特定情況進行調整
            results.append(True)
        else:
            results.append(False)

    return results


image_path = 'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\checklist_16325089_page_1.jpg'  # 圖像路徑

# 格式為(x, y, w, h)，其中x, y是勾選框左上角的坐標，w, h是勾選框的寬度和高度。
check_coords = [
    (1865,580,200,125),
    (2070,580,200,125)
]

print(is_checked(image_path, check_coords))