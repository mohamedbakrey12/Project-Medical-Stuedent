import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🗂️ المجلدات
processed_folder = "data/processed"
faiss_folder = "vectorstores/arabic_faiss"

# ✅ تحميل النموذج العربي (Multilingual)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 📄 تقسيم النصوص إلى مقاطع
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n", ".", "،", " "]
)

# 📚 تجميع كل المستندات
all_documents = []

for filename in os.listdir(processed_folder):
    if filename.endswith(".txt"):
        path = os.path.join(processed_folder, filename)
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        split_docs = text_splitter.split_documents(docs)
        all_documents.extend(split_docs)

# 🧠 بناء FAISS vectorstore
print(f"🔢 بناء FAISS vectorstore لعدد: {len(all_documents)} مقطع...")
db = FAISS.from_documents(all_documents, embedding_model)

# 💾 حفظ قاعدة البيانات
db.save_local(faiss_folder)
print("✅ تم حفظ قاعدة FAISS في:", faiss_folder)
