# importation of modules
import PyPDF2
from tkinter import filedialog
from tkinter import *
import csv
import HutchNERCall
import xml.etree.ElementTree as ET
import os


# List of dictionaries which store the clinical note files
collection = []
pathNames = []
listOfFiles = []
# Select Certain PDFS to read
def readPdf(num):
    file = listOfFiles[num]
    # create a pdf file object
    pdfFileObj = open(file, 'rb')
    # create a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Read and extract all the data from the pdf
    # Iterates through the pages
    # Store the data as Strings inside collection
    total = ""
    for x in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        data = pageObj.extractText()
        # Get rid of escape keys
        data = data.replace("\n", "")
        total = total + data
    temp = {file: total}
    collection.append(temp)
    return HutchNERcall()

def readCsv():
    listOfFiles = openFiles()
    for file in listOfFiles:
        csvReader = csv.reader(file)
        for row in csvReader:
            print(row)

def readTxtFile(num):
    file = listOfFiles[num]
    readObject = open(file,'r')
    listOftext = ""
    for line in readObject:
        listOftext = listOftext + line
    temp = {file:listOftext}
    collection.append(temp)
    return HutchNERcall()

def readXmlFile(num):
    file = listOfFiles[num]
    tree = ET.parse(file)
    root = tree.getroot()
    data = root.find('TEXT')
    temp = {file:data.text}
    collection.append(temp)
    return HutchNERcall()

#Allows user to choose which files to open
#Returns a list of strings directing the path to the file
def openFiles():
    global listOfFiles
    root = Tk()
    files = filedialog.askopenfilenames(parent=root, title='Choose a file')
    listOfFiles = root.tk.splitlist(files) 
    # Recording the file names without the extension
    for x in range(len(listOfFiles)):
        pathNames.append(os.path.splitext(os.path.basename(listOfFiles[x]))[0])

def HutchNERcall():
    unanalyzedData = []
    for file in collection:
        unanalyzedData.append(HutchNERCall.callToHutchNer(file))
    return unanalyzedData

def getPathNames():
    return pathNames

def clear():
    global collection
    collection = []






