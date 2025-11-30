# api/utils.py

def clean_text(text: str) -> str:
    """Remove unwanted characters and extra spaces."""
    if not text:
        return ""
    text = text.replace("\r", "").strip()
    return text


def split_into_chunks(text: str, max_length: int = 1500) -> list:
    """Splits long text into safe chunks for PDF formatting."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
