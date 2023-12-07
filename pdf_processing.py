import os
import fitz  # PyMuPDF

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """將單個 PDF 文件轉換為圖片並儲存"""
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]  # 獲取無副檔名的文件名
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
            output_file = f'{output_folder}/{file_name}_page_{page_num + 1}.png'
            pix.save(output_file)

def process_pdf_folder(folder_path):
    """處理包含多個 PDF 和圖檔的資料夾"""
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file)
            convert_pdf_to_images(pdf_path, folder_path, dpi=300)