import os
import fitz  # PyMuPDF

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """將 PDF 文件中的每頁轉換為圖片並儲存"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with fitz.open(pdf_path) as doc:
        zoom = dpi / 72  # 将 DPI 转换为 fitz 的缩放因子
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # 加載頁面
            pix = page.get_pixmap(matrix=mat)  # 獲取頁面的像素映射，应用缩放因子
            output_file = f'{output_folder}/page_{page_num + 1}.png'
            pix.save(output_file)