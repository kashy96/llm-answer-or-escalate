"""TF-IDF search over every abstract passage in the corpus.

The retrieved condition deliberately searches all 1,000 abstracts rather
than the question's own one, so the model sometimes gets evidence from the
wrong study. That is closer to how a real assistant works.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class PassageIndex:
    def __init__(self, items):
        self.passages = []  # (owner_id, section, text)
        for it in items:
            for section, text in zip(it.sections, it.contexts):
                self.passages.append((it.id, section, text))
        self.vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True, ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(p[2] for p in self.passages)

    def search(self, query, k=3):
        scores = linear_kernel(self.vectorizer.transform([query]), self.matrix).ravel()
        top = scores.argsort()[::-1][:k]
        return [(*self.passages[i], float(scores[i])) for i in top]
