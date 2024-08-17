import spacy

#nlp = spacy.blank("en")

#doc = nlp("Hello world!")

#token = doc[1]
#print(token.text)

#print()

#span = doc[1:3]
#print(span)

#print()

#for token in doc:
    #print(token.text)

#doc1 = nlp("It costs $5.")

#print("Index: ", [token.i for token in doc1])
#print("Text: ", [token.text for token in doc1])
#print("is_alpha: ", [token.is_alpha for token in doc1])
#print("is_punct: ", [token.is_punct for token in doc1])
#print("like_num: ", [token.like_num for token in doc1])

#nlp = spacy.load("en_core_web_sm")

#doc2 = nlp("She ate the pizza")

#for token in doc2:
    #print(token.text, token.pos_, token.dep_, token.head.text)

#nlp = spacy.load("en_core_web_sm")

#doc3 = nlp("Apple is looking at buying U.K. startup for $1 billion")

#for ent in doc3.ents:
    #print(ent.text, ent.label_)

#spacy.explain("NNP")    #? why spacy.explain not working
