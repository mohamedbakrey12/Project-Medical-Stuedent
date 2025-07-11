# ⬅️ سكربت لاستخراج النصوص من ملفات rawimport os
import fitz  # PyMuPDF
from tqdm import tqdm
import os

# 🗂️ المجلدات
raw_folder = "data/raw"
processed_folder = "data/processed"

# ✅ تأكد من وجود المجلد الوجهة
os.makedirs(processed_folder, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text.strip()

def extract_all_pdfs():
    for filename in tqdm(os.listdir(raw_folder), desc="📄 استخراج النصوص من ملفات PDF"):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(raw_folder, filename)
            text = extract_text_from_pdf(pdf_path)

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(processed_folder, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

    print("✅ تم استخراج جميع النصوص بنجاح إلى مجلد processed.")

if __name__ == "__main__":
    extract_all_pdfs()
