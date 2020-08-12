import csv
import os
import pandas

# Cria um arquivo csv com o corpora da BBC.
# Cada documento do corpora esta contido em uma linha do arquivo.
# A sequência das linhas preserva a ordem original dos documentos do corpora.
def BBC():
    corpus = os.listdir("../bbc")
    csvFile = open("bbc.csv", "w", encoding = "utf-8", newline = '')
    writer = csv.writer(csvFile)
    writer.writerow(["<text>"])
    for folder in corpus:
        subfolder = os.listdir(folder)
        for file in subfolder:
            sentence = open(folder + "/" + file, "r")
            content = sentence.read()
            writer.writerow([content])
    csvFile.close()
    dataSet = pandas.read_csv("bbc.csv")
    dataSet.to_csv("bbc_input.csv", index = False)
    pass

BBC()