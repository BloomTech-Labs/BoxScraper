from gensim.summarization.summarizer import summarize


def summary(text: str, word_count: int = 150) -> str:
    error_text = "No Summary Available"
    try:
        output = summarize(
            text,
            word_count=word_count,
        ).replace("\n", " ").strip()
        return output or error_text
    except ValueError:
        return error_text
