from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SentenceFinder:
    def __init__(self, corpus, k = 1):
        vectorizer = TfidfVectorizer()
        self.tf_idf_model = vectorizer.fit(corpus)
        # This is an sklearn sparse array, NOT a numpy array.
        self.corpus_vectors = self.tf_idf_model.transform(corpus)
        # Note: It is easier to work with a numpy array for text (e.g., for np indexing).
        self.corpus = np.array(corpus)
        self.k = k

    """
    Given the query, return the sentences
    which are similar from the corpus.
    """
    def get(self, query):
        query_vector = self.tf_idf_model.transform([query])
        assert query_vector.shape[0] == 1, f'Transformed query should have one vector, instead has {query_vector.shape[0]}!'
        similarities = 1 - cosine_similarity(query_vector, self.corpus_vectors)
        # The k smallest elements correspond to the closest sentences as
        # determined by their cosine similarity.
        indices = np.argpartition(similarities, self.k-1)[0][:self.k]
        return indices.tolist()
