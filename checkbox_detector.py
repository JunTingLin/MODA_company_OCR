import cv2

def draw_check_coords(image, check_coords):
    """
    在圖像上繪製指定坐標的矩形框。

    :param image: 要繪製的圖像
    :param check_coords: 要繪製的矩形框的坐標列表
    """
    # 在每個坐標上繪製矩形框
    for (x, y, w, h) in check_coords:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 綠色矩形框

    # 顯示圖像
    cv2.imshow('Check Coords', image)
    cv2.waitKey(0) # 等待按鍵輸入
    cv2.destroyAllWindows()

def is_checked(image_path, debug=False):
    """
    檢查指定位置是否有打勾，並處理結果。

    :param image_path: 圖像文件的路徑
    :param debug: 是否顯示除錯視窗
    :return: 處理後的結果字典
    """
    # 固定的 check_coords 坐標
    # x, y, w, h 分別為左上角 x 座標、左上角 y 座標、寬度、高度
    check_coords = [
        (1900,611,107,50), (2112,611,107,50),
        (1900, 670, 107, 50), (2112, 670, 107, 50),
        (1900, 766, 107, 50), (2112, 766, 107, 50),
        (1900, 853, 107, 50), (2112, 853, 107, 50),
        (1900, 969, 107, 50), (2112, 969, 107, 50),
        (1900, 1080, 107, 50), (2112, 1080, 107, 50),
        (1900, 1261, 107, 50), (2112, 1261, 107, 50),
        (1900, 1446, 107, 50), (2112, 1446, 107, 50),

        (1900, 1782, 107, 50), (2112, 1782, 107, 50),
        (1900, 2171, 107, 50), (2112, 2171, 107, 50),

        (1900, 2568, 107, 50), (2112, 2568, 107, 50),
        (1900, 2817, 107, 50), (2112, 2817, 107, 50),

        (1900, 3108, 107, 50), (2112, 3108, 107, 50),
    ]

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    results = []
    for (x, y, w, h) in check_coords:
        roi = gray[y:y+h, x:x+w]
        _, threshold = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY_INV)
        count = cv2.countNonZero(threshold)

        if count > 50:  # 這個閾值可能需要調整
            results.append(True)
        else:
            results.append(False)

    if debug:
        print(results) # 顯示檢查結果
        # 繪製並顯示坐標
        draw_check_coords(image.copy(), check_coords)

    return process_results(results)

def process_results(results):
    """
    處理檢查結果，每兩個結果為一組。

    :param results: 勾選框檢查結果的列表
    :return: 處理後的結果字典
    """
    processed_results = {}
    for i in range(0, len(results), 2):
        key = f"{(i//2) + 1}."
        if results[i] == False and results[i+1] == True:
            processed_results[key] = '否'
        elif results[i] == True and results[i+1] == False:
            processed_results[key] = '是'
        else:
            processed_results[key] = 'Not Sure'

    return processed_results

# 使用範例
# image_path = 'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\checklist_16325089_page_1.jpg'
# image_path = 'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\checklist_16590299_page_1.jpg'
image_path = 'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\checklist_70565450_page_1.jpg'

# 獲取最終結果
final_results = is_checked(image_path, debug=True)
print(final_results)
