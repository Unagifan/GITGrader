import Analyze as A
import NotesReader as Notes
import pandas as pd
import os

related = []
all = []
csv = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\InfoExtractOutput-csv"
txt = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\\UnlabeledDatasets"
pathNames = []

def setUp():
    global related
    global pathNames
    global all
    Notes.openFiles()
    pathNames = Notes.getPathNames()
    for x in range(len(pathNames)):
        A.organizeHutchNERData(Notes.readXmlFile(x))
        A.isGIrelated()
        related = A.getGIrelated()
        all = A.getAll()
        mapToTxtFileRelated(x)
        # mapToCsv(x)
        A.clear()
        Notes.clear()

def mapToCsv(num):
    index = A.getListOfGITRelatedTerms()
    # for x in range(len(related)):
    temp = {"probability": pd.Series([""], index=index),
                    "context": pd.Series([""], index=index),
                    }
    df = pd.DataFrame(temp)
    for token in related:
        for prob in index:
            if token[0] == prob:
                df.set_value(prob,'context',token[2])
                df.set_value(prob,'probability',token[1])
        temp = os.path.join(csv,pathNames[num]) + ".csv"
        df.to_csv(temp)

#MAP TERMS ONLY RELATED TO GIT
def mapToTxtFileRelated(num):
    temp = os.path.join(txt,pathNames[num]) + ".txt"
    file = open(temp,'w')
    # ONLY WANT TO WRITE THOSE THAT ARE NOT NEGATED
    newRelated = []
    for token in related:
        if token[1] != "DEFINITE_NEGATED_EXISTENCE" and token[1] != "PROBABLE_NEGATED_EXISTENCE":
            print(token)
            newRelated.append(token[2])
    newRelated = set(tuple(newRelated))
    for token in newRelated:
        file.write(token + "\n")
    file.close()

#ALL TERMS
def mapToTxtFileAll(num):
    temp = os.path.join(txt, pathNames[num]) + ".txt"
    file = open(temp, 'w')
    # ONLY WANT TO WRITE THOSE THAT ARE NOT NEGATED
    for token in all:
        if token[1] != "DEFINITE_NEGATED_EXISTENCE" and token[1] != "PROBABLE_NEGATED_EXISTENCE":
            file.write(token[2] + "\n")
    file.close()
setUp()


