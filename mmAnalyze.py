from Analyze import organizeHutchNERData
from Analyze import getListofProblems
from Analyze import getListofTests
from Analyze import getListofTreatments
import NotesReader
from OriginalMetamap import MetaMap

Meta = MetaMap("C:\\Users\\Facebook\\Documents\\public_mm_lite")
organizeHutchNERData(NotesReader.readXmlFile())

# store = Meta.map_concepts(["stomach pain","Rambutan","Spinal Surgery","Brain Cancer"])
store = Meta.map_concepts(getListofProblems())
for word in store:
    print(word + " : " + str(store[word]))
