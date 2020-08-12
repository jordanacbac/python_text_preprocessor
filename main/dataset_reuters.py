import csv
import os
import pandas

# Cria um arquivo csv com o corpora da Reuters.
# Cada documento do corpora esta contido em uma linha do arquivo.
# A sequência das linhas preserva a ordem original dos documentos do corpora.
def Reuters():
    corpus = os.listdir("../reuters")
    csvFile = open("reuters.csv", "w", encoding = "utf-8", newline = '')
    writer = csv.writer(csvFile)
    writer.writerow(["<text>"])
    for folder in corpus:
        subfolder = os.listdir(folder)
        for file in subfolder:
            sentence = open(folder + "/" + file, "r")
            content = sentence.read()
            if (len(content) > 250):
                writer.writerow([content])
    csvFile.close()
    dataSet = pandas.read_csv("reuters.csv")
    dataSet.to_csv("reuters_input.csv", index = False)
    pass

Reuters()