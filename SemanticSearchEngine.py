import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.decomposition import TruncatedSVD, PCA, LatentDirichletAllocation as LDiA
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
class SemanticSearchEngine:
    """
    @norm - l1, l2, cosine
    @vector_kind - bow, tfidf, word2vec
    @decomposition_algorithm - svd, pca, ldia
    @number_of_components - (1..n)
    """
    def __init__(self, distance, vector_kind, decomposition_algorithm, number_of_components):
        self.distance = lambda x, y : pairwise_distances(x, y, distance)
        if vector_kind == 'bow':
            self.vectorizer = CountVectorizer()
        elif vector_kind == 'tfidf':
            self.vectorizer = TfidfVectorizer()
        elif vector_kind == 'word2vec':
            pass

        if decomposition_algorithm == 'svd':
            self.da = TruncatedSVD(n_components=number_of_components)
        elif decomposition_algorithm == 'pca':
            self.da = PCA(n_components=number_of_components)
        elif decomposition_algorithm == 'ldia':
            self.da = LDiA(n_components=number_of_components)

        self.corpus = []
        self.labels = []
        self.corpusVect = []
        self.topics = []
        self.question = ''

    def loadData(self, corpus, labels):
        self.corpus = [corpus]
        self.labels = labels

        self.corpusVect = self.vectorizer.fit_transform(corpus).toarray()
        self.topics = self.da.fit_transform(self.corpusVect)

    def askQuestion(self, question):
        question = [question]
        questionVect = self.vectorizer.transform(question).toarray()
        questionTopic = self.da.transform(questionVect)

        indexOfNearestTopic = -1
        minDistance = float('inf')
        for index, topic in enumerate(self.topics):
            dist = self.distance(topic.reshape(1, -1), questionTopic.reshape(1, -1))
            if(dist < minDistance):
                minDistance = dist
                indexOfNearestTopic = index

        return self.labels[indexOfNearestTopic]

