from xml.dom.minidom import parseString, parse
import unittest
from informationExtraction.IngredientExtractor import IngredientExtractor
from parserForDavidisCookbook.xmlHelper import buildIngredientDict
from informationExtraction.BFormId import BFormId


class XmlHelperTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        dom = parse("/home/torsten/Desktop/MyMasterThesis/DavidisKochbuch/listIngredients.xml")
        self.ingE = IngredientExtractor(dom)

    def testBuildIngDict(self):
        dom = parseString(' \
<cue:listIngredient xmlns="http://www.tei-c.org/ns/1.0" xmlns:cue="http://cueML/ns"> \
    <cue:ingredient xml:id="Rindkochfleisch" BLSref="U180100"> \
        <cue:prefBasicForm>Rindfleisch</cue:prefBasicForm> \
    </cue:ingredient> \
    <cue:ingredient xml:id="Wurzelwerk" BLSref="G600000"> \
        <cue:prefBasicForm>Wurzelwerk</cue:prefBasicForm> \
        <cue:note>Another possible value for BLSref is "X560003"</cue:note> \
    </cue:ingredient> \
    <cue:ingredient xml:id="Midder" BLSref="V582100"> \
        <cue:prefBasicForm>Midder</cue:prefBasicForm> \
        <cue:altBasicForm>Kalbsmidder</cue:altBasicForm> \
        <cue:altBasicForm>Bries</cue:altBasicForm> \
        <cue:altBasicForm>Kalbsmilch</cue:altBasicForm> \
        <cue:note>"Kalbsmidder ist auch unter dem Synonym: Bries, Kalbsmilch bekannt. Kalbsmilch ist die Thymusdrüse des Kalbes. 100 g frische Kalbsmilch enthalten 99,8 kcal, 3,4 g Fett, 17,2 g Eiweiß, 77,8 g Wasser, 1,91 mg Eisen, 268 mg Cholesterin und 0,42 g Purine. Dieses Organ ist bei Jungtieren voll entwickelt. Bei erwachsenen Tieren bildet sich das Organ zurück. Kalbsmilch wird zur Herstellung von Spezialitäten, wie Suppen, Klöße und Ragout, verwendet." (http://www.cosmiq.de/qa/show/70827/was-ist-kalbsmidder/)</cue:note> \
        <cue:note>2. Note</cue:note> \
    </cue:ingredient> \
</cue:listIngredient>')
        d = buildIngredientDict(dom)
        self.assertEqual([BFormId(bform='Bries', xmlId='Midder')], d["Bries"])
        self.assertEqual([BFormId(bform='Rindfleisch', xmlId='Rindkochfleisch')], d["Rindfleisch"])
        
    def testBuildIngDictBasisCases(self):
        self.assertIsNone(self.ingE.getIngredientCandidates("Gesellschaft"))
        self.assertEqual(1, len(self.ingE.getIngredientCandidates("Rindfleisch")))
        self.assertLess(1, len(self.ingE.getIngredientCandidates("Fleisch")))
    
    def testBuildIngDictKablsklöße(self):
        self.assertIsNotNone(self.ingE.getIngredientCandidates("Kalbsklöße"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()