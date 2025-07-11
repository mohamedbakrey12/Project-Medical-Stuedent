import os

# 🗂️ تعريف هيكل المجلدات
folders = [
    "data/raw",
    "data/processed",
    "scripts",
    "models/embedding_model",
    "vectorstores/arabic_faiss",
    "utils"
]

# 📄 تعريف الملفات الأساسية
files = {
    "requirements.txt": """langchain
openai
streamlit
python-docx
faiss-cpu
tiktoken
transformers
sentence-transformers
python-dotenv
""",
    ".env": "# API keys هنا لو هتستخدم OpenAI أو OpenRouter",
    "README.md": "# Arabic RAG System\n\nمشروع لاسترجاع وإجابة الأسئلة من بيانات نصية عربية باستخدام LangChain وFAISS.",
    "utils/file_loader.py": "# ⬅️ دوال قراءة ملفات txt و docx",
    "utils/cleaner.py": "# ⬅️ دوال تنظيف النصوص",
    "utils/splitter.py": "# ⬅️ دوال تقسيم النصوص إلى chunks",
    "scripts/1_extract_data.py": "# ⬅️ سكربت لاستخراج النصوص من ملفات raw",
    "scripts/2_clean_and_split.py": "# ⬅️ سكربت لتنظيف النصوص وتقسيمها",
    "scripts/3_build_vectorstore.py": "# ⬅️ سكربت لإنشاء FAISS vectorstore",
    "scripts/4_load_rag_chain.py": "# ⬅️ سكربت لتحميل RAG chain",
    "scripts/5_run_interface.py": "# ⬅️ واجهة Streamlit"
}

# إنشاء المجلدات
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# إنشاء الملفات
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ تم إنشاء هيكل المشروع بنجاح!")
