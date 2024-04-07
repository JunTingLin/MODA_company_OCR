import os
import fitz  # PyMuPDF

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """將單個 PDF 文件轉換為圖片並儲存"""
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]  # 獲取無副檔名的文件名
    image_files = [] 
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
            output_file = f'{output_folder}/{file_name}_page_{page_num + 1}.png'
            pix.save(output_file)
            image_files.append(f'{file_name}_page_{page_num + 1}.png')
    return image_files

def process_pdf_folder(folder_path, filenames, updater):
    """處理包含多個 PDF 和圖檔的資料夾"""
    total_files = len(filenames)
    updated_filenames = []
    for index, filename in enumerate(filenames):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            image_files = convert_pdf_to_images(pdf_path, folder_path, dpi=300)
            updated_filenames.extend(image_files) # 將新生成的圖片文件名添加到列表中
            updater.update_status(f"{filename} 已拆分...")
        else:
            updated_filenames.append(filename) # 如果不是 PDF 文件，則直接添加到列表中
            updater.update_status(f"{filename} 無需拆分...")

        updater.update_progress((index + 1) * 100 // total_files)

    return updated_filenames


if __name__ == "__main__":
    folder_path = r'C:\Users\junting\Desktop\ocr_result'
    updated_filenames = process_pdf_folder(folder_path, ['scan_test_all.pdf'])
    print(updated_filenames)