from parserForDavidisCookbook.XmlParser import XmlParser
from xml.dom.minidom import parse, parseString
from informationExtraction.IngredientExtractor import IngredientExtractor
from informationExtraction.UnitExtractor import UnitExtractor
import time
from informationExtraction.Extractor import Extractor
from informationExtraction.dictBasedExtractor import dictBasedEnrichment
from informationExtraction.ruleBasedExtractor import applyRulesToWordProperties
 
ergFilePath = "erg.xml" 
   
if __name__ == '__main__':
    startTime = time.time()    
     
    cookbook = XmlParser(parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/recipes extracted.xml"))
    ingE = IngredientExtractor(parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/listIngredients.xml"))
    unitE = UnitExtractor(parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/cueML/cueML_v0.5.rng")) 
     
    rcpIds = ["B-{}".format(i) for i in range(1,2)]
    recipes = cookbook.getPlainTextRecipes(rcpIds)
    extractor = Extractor(ingE, unitE)
    extractor.extractRecipesToXml(recipes, ergFilePath)




