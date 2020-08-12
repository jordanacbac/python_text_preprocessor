import math
from PreProcessor import PreProcessor
from PreProcessor import StopWords
from PreProcessor import Stemmer
from PreProcessor import NGrama

class Representation(object):
    def __init__(self, corpus=[], listPreProcessors=[]):
        super(Representation, self).__init__()
        self.corpus = corpus
        self.listPreProcessors = listPreProcessors
        self.corpusPreprocessed = 0
        self.listOfTerms = 0
        self.transposedMatrix = 0
        self.matrix = self.represent()

    # Efetua o pré-processamento (retorna uma list).
    def preProcessor(self, corpus, listPreProcessors):
        stopWords = StopWords()
        stemmer = Stemmer()
        nGrama = NGrama(nGrama=listPreProcessors[2])
        newCorpus = []
        for document in corpus:
            content = []
            for sentence in corpus[document]:
                sentence = sentence.rstrip("\n")
                sentence = PreProcessor.foldCase(sentence)
                listOfTokens = PreProcessor.tokenize(sentence)
                if(listPreProcessors[0] == 1):
                    listOfTokens = stopWords.process(listOfTokens)
                if(listPreProcessors[1] == 1):
                    listOfTokens = stemmer.process(listOfTokens)
                if(listPreProcessors[2] > 1):
                    listOfTokens = nGrama.process(listOfTokens)
                content.append(listOfTokens)
            newCorpus = content
        return newCorpus

    # Cria uma lista de termos (retorna uma list).
    def termsList(self, corpus=[]):
        terms = []
        for row in corpus:
            for col in row:
                if col not in terms:
                    terms.append(col)
        terms.sort()
        return terms

    # Retorna o número de documentos em que o termo aparece.
    def termFreqDoc(self, corpus, term):
        cont = 0
        for rowCorpus in corpus:
            if term in rowCorpus:
                cont = cont + 1
        return cont

    # Conta o número de vezes que o termo aparece na lista de tokens.
    def tf(self, listOfTokens, term):
        cont = 0
        for token in listOfTokens:
            if token == term:
                cont = cont + 1
        return cont

    # Calcula o idf do termo.
    def idf(self, corpus, term):
        return math.log(len(corpus) / self.termFreqDoc(corpus, term))

    # Realiza o corte dos termos.
    def cleaningTerms(self, corpus, terms, minimal, maximum):
        contOfTerms = []
        listOfIndex = []
        for term in terms:
            contOfTerms.append(self.termFreqDoc(corpus, term))
        minimal = 3
        maximum = round(len(corpus) * maximum)
        cont = 0
        while(cont < len(contOfTerms)):
            if(contOfTerms[cont] <= minimal or contOfTerms[cont] >= maximum):
                listOfIndex.append(cont)
            cont = cont + 1
        cont = len(listOfIndex) - 1
        while(cont >= 0):
            terms.pop(listOfIndex.pop(cont))
            cont = len(listOfIndex) - 1
        pass

    # Retorna a matriz transposta.
    def transposeMatrix(self, matrix):
        newMatrix = []
        for row in zip(*matrix):
            newMatrix.append(list(row))
        return newMatrix

    # Retorna o corpus pré-processado.
    def getCorpus(self):
        return self.corpusPreprocessed

    # Retorna a lista de termos.
    def getListOfTerms(self):
        return self.listOfTerms

    # Retorna a variavel matrix.
    def getMatrix(self):
        return self.matrix

    # Retorna a variavel transposedMatrix.
    def getTransposed(self):
        if self.transposedMatrix == 0:
            self.transposedMatrix = self.transposeMatrix(self.matrix)
            return self.transposedMatrix
        else:
            return self.transposedMatrix

    # Retorna a representação.
    def represent(self):
        pass

# Cria a matriz de representação binária.
class Binary(Representation):
    def __init__(self, corpus=[], listPreProcessors=[]):
        Representation.__init__(self, corpus, listPreProcessors)

    def represent(self):
        # Carrega o corpus e a lista de termos.
        self.corpusPreprocessed = self.preProcessor(self.corpus, self.listPreProcessors)
        self.listOfTerms = self.termsList(self.corpusPreprocessed)
        print("Lista de termos: {}.".format(len(self.listOfTerms)))
        #self.cleaningTerms(self.corpusPreprocessed, self.listOfTerms, 0.05, 0.33)
        #matrix = []
        #for rowCorpus in self.corpusPreprocessed:
        #    row = []
        #    for colTerms in self.listOfTerms:
        #        if colTerms in rowCorpus:
        #            row.append(1)
        #        else:
        #            row.append(0)
        #    matrix.append(row)
        #    row.clear
        #return matrix

# Cria a matriz de representação com frequência de termo.
class TFNorm(Representation):
    def __init__(self, corpus=[], listPreProcessors=[]):
        Representation.__init__(self, corpus, listPreProcessors)

    def represent(self):
        # Carrega o corpus e a lista de termos.
        self.corpusPreprocessed = self.preProcessor(self.corpus, self.listPreProcessors)
        self.listOfTerms = self.termsList(self.corpusPreprocessed)
        #self.cleaningTerms(self.corpusPreprocessed, self.listOfTerms, 0.05, 0.33)
        matrix = []
        for rowCorpus in self.corpusPreprocessed:
            row = []
            for colTerms in self.listOfTerms:
                if colTerms in rowCorpus:
                    row.append(self.tf(rowCorpus, colTerms) / len(rowCorpus))
                else:
                    row.append(0)
            matrix.append(row)
            row.clear
        return matrix

# Cria a matriz de representacao com frequencia de termo e inverso da frequencia nos documentos.
class TFIDFNorm(Representation):
    def __init__(self, corpus=[], listPreProcessors=[]):
        Representation.__init__(self, corpus, listPreProcessors)

    def represent(self):
        # Carrega o corpus e a lista de termos.
        self.corpusPreprocessed = self.preProcessor(self.corpus, self.listPreProcessors)
        self.listOfTerms = self.termsList(self.corpusPreprocessed)
        #self.cleaningTerms(self.corpusPreprocessed, self.listOfTerms, 0.05, 0.33)
        matrix = []
        for rowCorpus in self.corpusPreprocessed:
            row = []
            for colTerms in self.listOfTerms:
                if colTerms in rowCorpus:
                    row.append(self.tf(rowCorpus, colTerms) * self.idf(self.corpusPreprocessed, colTerms) / len(rowCorpus))
                else:
                    row.append(0)
            matrix.append(row)
            row.clear
        return matrix