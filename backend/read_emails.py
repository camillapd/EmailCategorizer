import os
import re

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import RSLPStemmer
except ImportError:
    nltk = None


def download_nltk():
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('rslp')


def read_uploaded_file(uploaded_file):
    filename = uploaded_file.filename
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext == ".txt":
        data = uploaded_file.read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin-1")

    elif ext == ".pdf":
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 não instalado. Rode: pip install PyPDF2")

        # PyPDF2 precisa de um arquivo ou stream
        uploaded_file.stream.seek(0)  # garante que está no início
        reader = PdfReader(uploaded_file.stream)
        my_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                my_text += page_text + "\n"
        return my_text

    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")


def preprocess_text(text):
    if nltk is None:
        raise ImportError("NLTK não instalado. Rode: pip install nltk")

    # Verifica se os recursos estão disponíveis e baixa se necessário
    try:
        stemmer = RSLPStemmer()
        stop_words = set(stopwords.words("portuguese"))
    except LookupError:
        download_nltk()
        stemmer = RSLPStemmer()
        stop_words = set(stopwords.words("portuguese"))

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9çãáàâéêíóôúü\s]", "", text)

    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)

    tokens = [stemmer.stem(t) for t in tokens if t not in stop_words]

    return " ".join(tokens)
