from typing import List

import yake


def get_keywords(text: str, max_ngram: int = 5, n_keywords: int = 5) -> List[str]:
    keywords = yake.KeywordExtractor(
        lan="en",
        n=max_ngram,
        dedupLim=0.3,
        top=n_keywords,
    ).extract_keywords(text)
    return [s[0].title() for s in keywords]
