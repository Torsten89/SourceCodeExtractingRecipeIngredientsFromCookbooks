from xml.dom.minidom import parse
import unittest
from informationExtraction.QuantityExtractor import isQuantity
from informationExtraction.UnitExtractor import UnitExtractor
from informationExtraction.IngredientExtractor import IngredientExtractor
from informationExtraction.dictBasedExtractor import dictBasedEnrichment
from model.WordProperty import WordProperty


class DictBasedExtractorTest(unittest.TestCase):
    
    def setUp(self):
        self.ingE = IngredientExtractor(parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/listIngredients.xml"))
        self.unitE = UnitExtractor(parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/cueML/cueML_v0.5.rng"))

    def testWP0(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)     
        self.assertIsNone(wordProperties[0].properties.get(WordProperty.ingredient))
        self.assertIsNone(wordProperties[0].properties.get(WordProperty.unit))
        self.assertIsNone(wordProperties[0].properties.get(WordProperty.quantity))

    def testQuantity1(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)
        self.assertEqual("24—30", wordProperties[4].properties.get(WordProperty.quantity))
        
    def testQuantity2(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)
        self.assertEqual("8—10", wordProperties[10].properties.get(WordProperty.quantity))
        
    def testIngredient1(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)
        self.assertIsNotNone(wordProperties[8].properties.get(WordProperty.ingredient))
        self.assertEqual(0, len(wordProperties[8].properties.get(WordProperty.ingredient)))
        
    def testIngredient2(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)
        self.assertIsNotNone(wordProperties[12].properties.get(WordProperty.ingredient))
        self.assertIn("Rindkochfleisch", [candi.xmlID for candi in wordProperties[12].properties.get(WordProperty.ingredient)])
    
    def testIngredient3(self):
        s = "Es wird hierzu für 24—30 Personen eine kräftige Bouillon von 8—10 Pfund Rindfleisch mit Wurzelwerk gekocht."
        wordProperties = dictBasedEnrichment(s, self.ingE, self.unitE)
        self.assertIsNotNone(wordProperties[14].properties.get(WordProperty.ingredient))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()