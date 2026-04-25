import os
import tempfile
import hashlib
from typing import Union, Tuple, Optional


# ----------------------------------------
# 📤 SAVE UPLOADED FILE (STREAMLIT)
# ----------------------------------------
def save_uploaded_file(uploaded_file) -> str:
    """
    Save a Streamlit UploadedFile to a temp file and return its path.
    """
    suffix = _infer_suffix(uploaded_file.name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


# ----------------------------------------
# 📦 SAVE BYTES TO FILE
# ----------------------------------------
def save_bytes_to_file(data: bytes, suffix: str = ".bin") -> str:
    """
    Save raw bytes to a temp file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        return tmp.name


# ----------------------------------------
# 📥 READ FILE AS BYTES
# ----------------------------------------
def read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


# ----------------------------------------
# 🧾 READ FILE AS TEXT
# ----------------------------------------
def read_file_text(path: str, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding, errors="ignore") as f:
        return f.read()


# ----------------------------------------
# 🗑️ SAFE DELETE FILE
# ----------------------------------------
def safe_delete(path: Optional[str]) -> bool:
    """
    Safely delete a file if it exists.
    """
    try:
        if path and os.path.exists(path):
            os.remove(path)
            return True
    except Exception:
        pass
    return False


# ----------------------------------------
# 🧹 CLEANUP MULTIPLE FILES
# ----------------------------------------
def cleanup_files(paths):
    """
    Delete multiple temp files.
    """
    results = []
    for p in paths:
        results.append(safe_delete(p))
    return all(results)


# ----------------------------------------
# 🔐 FILE HASH (FOR CACHING / DEDUP)
# ----------------------------------------
def file_hash_from_bytes(data: bytes) -> str:
    """
    Create SHA256 hash from bytes.
    """
    return hashlib.sha256(data).hexdigest()


def file_hash_from_path(path: str) -> str:
    """
    Create SHA256 hash from file content.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------
# 🏷️ FILE INFO
# ----------------------------------------
def get_file_info(path: str) -> dict:
    """
    Return basic file metadata.
    """
    if not os.path.exists(path):
        return {"exists": False}

    return {
        "exists": True,
        "size_bytes": os.path.getsize(path),
        "filename": os.path.basename(path),
        "extension": os.path.splitext(path)[1],
    }


# ----------------------------------------
# 🔎 HELPER: INFER SUFFIX
# ----------------------------------------
def _infer_suffix(filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return ext if ext else ".tmp"


# ----------------------------------------
# 🧠 FRONT/BACK PAIR SAVE
# ----------------------------------------
def save_front_back(front_file, back_file) -> Tuple[str, str]:
    """
    Save two uploaded files (front/back PCB) and return paths.
    """
    front_path = save_uploaded_file(front_file)
    back_path = save_uploaded_file(back_file)
    return front_path, back_path
