class Ingredient:
    """ A class which bundles attributes of an ingredient.
        It can only have attributes, which are specified in Ingredient.allowedAttris,
        which correspond to cueML recipeIngredient Element, and must have the words,
        as well as their absolute position in the recipe, which are tagged as an ingredient.
        When an ingredient doesn't specify an attribute, this attribute does not exist in the object.
    """
    # {attriName: cueMLName} these two can be different. E.G. yield is a cueML name, but not a valid identifier for python
    allowedAttris = {"ref":"ref", 
                     "target":"target", 
                     "quantity":"quantity", 
                     "atLeast":"atLeast", 
                     "atMost":"atMost",
                     "unit":"unit", 
                     "altGrp":"altGrp",
                     "optional":"optional",
                     "ingYield":"yield"}

    def __init__(self, d, words, positionInRecipe):
        """ d is a dictionary of cueML attris.
            words are the words of the ingredient as list.
            positionInRecipe is the absolute (start and end) position of the words in the recipe, ignoring punctuation - 
                E.g. in "Suppe von Sago und..." it would be (2,2) for "Sago".
        """
        self.words = words # nice for debugging
        self.positionInRecipe = positionInRecipe # important for evaluation
        for attriName, value in d.items():
            if attriName not in Ingredient.allowedAttris:
                raise Exception("According to cueML {} is not a valid attribute name".format(attriName))
            
            if value: setattr(self, attriName, value)
    
    def __str__(self):
        entries = []
        for prop, value in self.__dict__.items():
            if value:
                entries.append("{}={}".format(prop, value))
                
        return "Ingredient: {}".format(", ".join(entries))
    
    def __eq__(self, other):
#         for k, v in self.__dict__.items(): # for debugging
#             if v != other.__dict__.get(k):
#                 print(k, v)
#                 print(k, other.__dict__.get(k))
        return self.__dict__ == other.__dict__ # compares all attris cause classes are basically dicts in python :)

    