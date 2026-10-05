import spacy

# Load English spaCy model
nlp = spacy.load("en_core_web_sm")

# Get input from user
text = input("Enter a sentence or paragraph: ")

print("\nOriginal Text:")
print(text)

# Process text
doc = nlp(text)

# POS TAGGING
print("\nPART-OF-SPEECH (POS) TAGGING")
for token in doc:
    print(f"{token.text:15} {token.pos_:10} {spacy.explain(token.pos_)}")

# NAMED ENTITY RECOGNITION (NER)
print("\nNAMED ENTITY RECOGNITION (NER)")
if len(doc.ents) == 0:
    print("No named entities found.")
else:
    for ent in doc.ents:
        print(f"{ent.text:20} {ent.label_:10} "
              f"{spacy.explain(ent.label_)}")







If using Google Colab
First run:
!pip install spacy
!python -m spacy download en_core_web_sm
Then run the main code above.


Input :
Enter a sentence or paragraph: 
RAMU EATS BANANA



Output : 
Original Text:
RAMU EATS BANANA
PART-OF-SPEECH (POS) TAGGING
RAMU            PROPN      proper noun
EATS            PROPN      proper noun
BANANA          PROPN      proper noun

NAMED ENTITY RECOGNITION (NER)
No named entities found.
