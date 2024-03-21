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
        (1900+5,611-23,150,73), (2112,611-23,150,73),
        (1900+5, 704-23, 150, 73), (2112, 704-23, 150, 73),
        (1900+5, 766-23, 150, 73), (2112, 766-23, 150, 73),
        (1900+5, 853-23, 150, 73), (2112, 853-23, 150, 73),
        (1900+5, 969-23, 150, 73), (2112, 969-23, 150, 73),
        (1900+5, 1080-23, 150, 73), (2112, 1080-23, 150, 73),
        (1900+5, 1261-23, 150, 73), (2112, 1261-23, 150, 73),
        (1900+5, 1446-23, 150, 73), (2112, 1446-23, 150, 73),

        (1900+5, 1782-60, 150, 170), (2112, 1782-60, 150, 170),
        (1900+5, 2171-60, 150, 170), (2112, 2171-60, 150, 170),

        (1900+5, 2568-60, 150, 170), (2112, 2568-60, 150, 170),
        (1900+5, 2817-60, 150, 170), (2112, 2817-60, 150, 170),

        (1900+5, 3108-40, 150, 170), (2112, 3108-40, 150, 170),
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
    :return: 處理後的結果列表
    """
    processed_results = []
    for i in range(0, len(results), 2):
        if results[i] == False and results[i+1] == True:
            processed_results.append(0)
        elif results[i] == True and results[i+1] == False:
            processed_results.append(1)
        else:
            processed_results.append('Not Sure')


    return processed_results


if __name__ == "__main__":
    image_path = r'C:\Users\junting\Desktop\ocr_data\data1\scan_test_all_page_15.jpg'

    results = is_checked(image_path, debug=True)
    print(results)
