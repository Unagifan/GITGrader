import sklearn as sk
from sklearn import datasets as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

trainPath = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\TrainingDataset"
testPath = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\TestingDataset"

gradeTrain = ds.load_files(trainPath,load_content = True,encoding = 'utf-8')
gradeTest = ds.load_files(testPath,load_content= True,encoding = 'utf-8')
grade3CertainPath = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\Grade-Certain\Grade3-Certain.txt"
grade4CertainPath = "C:\\Users\Facebook\Desktop\Fred Hutch Internship\ClinicalNotesReader\Grade-Certain\Grade4-Certain.txt"
grade3CertainList = []
grade4CertainList = []

#['Grade 1 or 2', 'Grade 3', 'Grade 4', 'Non-Existent'] - target_names
# CountVectorizer- Turn text in matrix of token counts
# Tfidf - Calculate term frequency times inverse document frequency


'''Create and train a classifier'''
def trainClf():
    global clf
    # Pipeline to quickly train classifier
    clf = Pipeline([('vect',CountVectorizer()),
                     ('tfidf',TfidfTransformer()),
                     ('clf',MultinomialNB())])

    clf = clf.fit(gradeTrain['data'],gradeTrain['target'])


'''Predict on Test Data set'''
def predictTest():
    predicted = clf.predict(gradeTest['data'])
    certain = checkCertain(gradeTest['data'])
    for change in certain:
        predicted[change[0]] = change[1]
    print("TOTAL ACCURACY: " + str(accuracy_score(gradeTest['target'],predicted)))
    for x in range(len(predicted)):
        index = gradeTest['target'][x]
        pIndex = predicted[x]
        print(gradeTest['data'][x] + "| ACTUAL:" +
              gradeTest['target_names'][index] + " PREDICTED: "
              + gradeTest['target_names'][pIndex])

'''Loads/Maps the text files containing the words which determines the grade'''
def loadCertain(path,list):
    rObject = open(path, 'r')
    for line in rObject:
        line = line.strip()
        line = line.lower()
        list.append(line)

'''Checks if the data passed in contains terms that are specific to a certain grade'''
def checkCertain(data):
    certain = []
    #certain indicator - (index,grade)
    for x in range(len(data)):
        temp = ()
        for indicator in grade3CertainList:
            if indicator in data[x]:
                temp = (x,1)
        for i in grade4CertainList:
            if i in data[x]:
                print(i)
                temp = (x,2)
        if temp:
            certain.append(temp)
    return certain

loadCertain(grade3CertainPath,grade3CertainList)
loadCertain(grade4CertainPath,grade4CertainList)

trainClf()
predictTest()