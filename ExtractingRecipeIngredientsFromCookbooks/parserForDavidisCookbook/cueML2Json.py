from parserForDavidisCookbook.XmlParser import XmlParser,\
    parseXml2PlainTextRecipe, getIngsFromNode
from xml.dom.minidom import parse, parseString
import json
import copy
from parserForDavidisCookbook.xmlHelper import getElems

def getJsonRcps(pathToCueMLFile, rcpIds, hack=False):
    dictRcps = dict()
    
    xmlRcps = (XmlParser(parse(pathToCueMLFile))).getXmlRecipes(rcpIds)
    for xmlRcp in xmlRcps:
        dictRcp = xmlRcp2dictRcp(xmlRcp)
        t = dictRcp["type"]
        if t in dictRcps: dictRcps[t].append(dictRcp)
        else: dictRcps[t] = [dictRcp]
        
    # hack for using our manual tagged soups:
    if hack:
        # take B-1 to B-68 from golden standard and B-69 to B-93 from pathToCueMLFile
        pathToGoldenStandard = "/home/torsten/Desktop/MyMasterThesis/docs/DavidisesKochbuch/GoldenStandard.xml"
        xmlRcps = (XmlParser(parse(pathToGoldenStandard))).getXmlRecipes(["B-{}".format(i) for i in range(1, 69)]) \
           + (XmlParser(parse(pathToCueMLFile))).getXmlRecipes(["B-{}".format(i) for i in range(69, 94)])
        soups = [xmlRcp2dictRcp(xmlRcp) for xmlRcp in xmlRcps]
        dictRcps["Suppen"] = soups

    return json.dumps(dictRcps)

def xmlRcp2dictRcp(xmlRcp):
    plainTextRcp = parseXml2PlainTextRecipe(xmlRcp)
    dictRcp = dict()
    
    dictRcp["rcp-id"] = plainTextRcp.rcpId
    dictRcp["type"] = plainTextRcp.rcpType.replace("_", " ")[:-1]  # remove . at the end - important for bootstrap valid id!!
    dictRcp["name"] = plainTextRcp.name
    dictRcp["instructions"] = getInstructionText(xmlRcp, "p") + getInstructionText(xmlRcp, "note")
    dictRcp["ingredients"] = mergeIngs(getIngsFromNode(xmlRcp))
    dictRcp["cueAlts"] = [altElems.attributes["target"].value.split() for altElems in getElems(xmlRcp, "alt")]
        
    return dictRcp

def getInstructionText(node, elemName):
    result = []
    for instruction in getElems(node, elemName):
        result.append("\n".join(instruction.toprettyxml().split("\n")))
    return "".join(result)

def mergeIngs(ings):
    newIngs = []
    for ing in ings:
        if "ref" not in ing.__dict__:
            if all(not ingWithNoRefEqualExeptForPosiInRcp(ing, iPrime) for iPrime in newIngs): newIngs.append(ing)
            continue
        
        ref = ing.__dict__["ref"]
        added = False
        for iPrime in newIngs:
            if "ref" not in iPrime.__dict__:
                continue
            else:
                if ref == iPrime.__dict__["ref"]:
                    iPrime.__dict__.update(ing.__dict__)
                    added = True
                    break
        if not added:
            newIngs.append(ing)
            
    return [i.__dict__ for i in newIngs]

def ingWithNoRefEqualExeptForPosiInRcp(i1, i2):
    if "ref" in i1.__dict__ or "ref" in i2.__dict__:
        return False
    
    i1Prime = copy.deepcopy(i1)
    i1Prime.positionInRecipe = None
    i2Prime = copy.deepcopy(i2)
    i2Prime.positionInRecipe = None
    
    return i1Prime == i2Prime
    
                    
                    
if __name__ == '__main__':
    #pathToCueMLFile = "/home/torsten/Desktop/erg.xml"
    pathToCueMLFile = "/home/torsten/Desktop/MyMasterThesis/docs/DavidisesKochbuch/Rezepte automatisch mit cueML ausgezeichnet.xml"
    pathToErg = "/home/torsten/Desktop/MyMasterThesis/docs/Rezepte/Rezepte.json"
    with open(pathToErg, "w") as f:
        f.write("rcps={}".format(getJsonRcps(pathToCueMLFile, [], hack=True))) 

    
    
    
    