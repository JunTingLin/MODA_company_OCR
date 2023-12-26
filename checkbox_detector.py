import cv2

def is_checked(image_path):
    """
    檢查指定位置是否有打勾，並處理結果。

    :param image_path: 圖像文件的路徑
    :return: 處理後的結果字典
    """
    # 固定的 check_coords 坐標
    check_coords = [
        (1865,595,180,80), (2085,595,180,80),
        (1865, 705, 180, 45), (2085, 705, 180, 45),
        (1865, 770, 180, 45), (2085, 770, 180, 45),
        (1865, 825, 180, 95), (2085, 825, 180, 95),
        (1865, 945, 180, 95), (2085, 945, 180, 95),
        (1865, 1053, 180, 95), (2085, 1053, 180, 95),
        (1865, 1175, 180, 230), (2085, 1175, 180, 230),
        (1865, 1425, 180, 95), (2085, 1425, 180, 95),
        (1865, 1624, 180, 375), (2085, 1624, 180, 375),
        (1865, 2060, 180, 305), (2085, 2060, 180, 305),
        (1865, 2465, 180, 305), (2085, 2465, 180, 305),
        (1865, 2805, 180, 130), (2085, 2805, 180, 130),
        (1865, 3035, 180, 260), (2085, 3035, 180, 260),
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
image_path = 'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\checklist_70565450_page_1.jpg'  # 圖像路徑

# 獲取最終結果
final_results = is_checked(image_path)
print(final_results)
