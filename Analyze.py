import NotesReader

listOfGITRelatedTerms = []
listOfProblems = []
listOfTreatments = []
listOfTests = []
GI = [] #List of tuples which are composed of (problem,negation,context)

#Parent function
def organizeHutchNERData(notProcessedData):
    global listOfProblems
    global listOfTests
    global listOfTreatments
    #Clean up of HutchNER Data
    for x in range(len(notProcessedData)):
        temp = list(notProcessedData[x].values())
        for x in range(len(temp)):
            tokenList = temp[x]['NER_labels']
            listOfProblems.append(joinLabeledTerms("problem",tokenList))
            listOfTreatments.append(joinLabeledTerms("treatment",tokenList))
            listOfTests.append(joinLabeledTerms("test",tokenList))

#Importing GIT related Terms from Txt file
def organizeGITrelatedTerms(path):
    # Clean up of HutchNER Data
    global listOfGITRelatedTerms
    #PATH TO GIT RELATED TERMS from Txt file
    rObject = open(path,'r')
    for line in rObject:
        line = line.strip()
        line = line.lower()
        listOfGITRelatedTerms.append(line)


# Combine adajacent labeled terms
def joinLabeledTerms(label,tokenList):
    labeled =[]
    y = 0
    while y < len(tokenList):
        counter = 0
        if tokenList[y]['label'] == label:
            #PROBLEM WITH WHEN DOCUMENT DOES NOT END IN NON-PROBLEM
            while tokenList[y + counter + 1]['label'] == label:
                counter += 1
            negation = ""
            if 'negation' in tokenList[y]:
                negation = tokenList[y]['negation']
            temp = tokenList[y]['text']
            for z in range(counter):
                temp = temp + " " + tokenList[y + z + 1]['text']
            temp = temp.lower()
            dic = {temp:negation}
            labeled.append(dic)
        y += 1 + counter
    return labeled

#Hard codingly compare listed problems with those
def isGIrelated():
    global GI
    for problem in listOfProblems[0]:
        for token in listOfGITRelatedTerms:
            if token in str(problem.keys()):
                temp = (token,list(problem.items())[0][1],list(problem.items())[0][0])
                GI.append(temp)
    for treatment in listOfTreatments[0]:
        for token in listOfGITRelatedTerms:
            if token in str(treatment.keys()):
                temp = (token,list(treatment.items())[0][1],list(treatment.items())[0][0])
                GI.append(temp)
    for test in listOfTests[0]:
        for token in listOfGITRelatedTerms:
            if token in str(test.keys()):
                temp = (token,list(treatment.items())[0][1],list(treatment.items())[0][0])
                GI.append(temp)
    #removes duplicates
    GI = list(set(GI))

def clear():
    global listOfProblems
    global listOfTreatments
    global listOfTests
    global GI
    listOfProblems = []
    listOfTreatments = []
    listOfTests = []
    GI = []

def getListofProblems():
    return listOfProblems

def getListofTreatments():
    return listOfTreatments

def getListofTests():
    return listOfTests

def getGIrelated():
    return GI

def getListOfGITRelatedTerms():
    return listOfGITRelatedTerms

def getAll():
    mergedList = listOfTreatments + listOfTests + listOfProblems
    return mergedList

#Should always occur to generate list of GIT related terms
organizeGITrelatedTerms("C:\\Users\\Facebook\\Documents\\ClinicalNotes\\GITRelatedTerms.txt")

# NotesReader.openF
# TEST of HutchNER labeling problems
# for doc in listOfProblems:
#     for prob in doc:
#         print(prob)
# for doc in listOfTests:
#     for test in doc:
#         print(test)
# for doc in listOfTreatments:
#     for treatment in doc:
#         print(treatment)

# Test GITrelated terms
# for token in GI:
#      print(token)




