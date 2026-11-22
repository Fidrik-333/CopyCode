EXPERIMENT:-1
AIM :- Load and display an image using OpenCV and perform basic operations like resizing, cropping, and rotation
PROGRAM :-

import cv2
from google.colab import files
from google.colab.patches import cv2_imshow
uploaded = files.upload()
img = cv2.imread("example.jpg")
# Display original image
print("Original Image")
cv2_imshow(img)
resized = cv2.resize(img, (500, 300))
print("Resized Image (500, 300)")
cv2_imshow(resized)
cropped = img[50:250, 50:250]
print("Cropped Image")
cv2_imshow(cropped)
h, w = img.shape[:2]
centre = (w // 2, h // 2)
matrix = cv2.getRotationMatrix2D(centre, 45, 1.0)
rotated = cv2.warpAffine(img, matrix, (w, h))
print("Rotated Image (45 Degrees)")
cv2_imshow(rotated)








-------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 2
AIM :-  Apply edge detection by Sobel thresholding technique on grayscale and color images. 
PROGRAM :- 


import cv2
import numpy as np
import matplotlib.pyplot as plt

uploaded = files.upload()
img = cv2.imread("example.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def show_image(img, title):
    h, w = img.shape[:2]
    plt.imshow(img, cmap="gray")
    plt.title(title, fontsize=16)
    plt.axis("off")
    plt.show()
show_image(gray, "Gray Scale")
sobel_x = cv2.Sobel(
    gray,
    cv2.CV_64F,
    1,
    0,
    ksize=3
)
sobel_x_abs = cv2.convertScaleAbs(sobel_x)
show_image(sobel_x_abs, "Gx Horizontal Edges")
sobel_y = cv2.Sobel(
    gray,
    cv2.CV_64F,
    0,
    1,
    ksize=3
)
sobel_y_abs = cv2.convertScaleAbs(sobel_y)
show_image(sobel_y_abs, "Gy Vertical Edges")
sobel_combined = cv2.magnitude(
    sobel_x,
    sobel_y
)
sobel_combined = cv2.convertScaleAbs(sobel_combined)
show_image(
    sobel_combined,
    "Combined Edges"
)





------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 3
AIM :-  Implement image filtering operations: Gaussian, Median, and Bilateral filters.
PROGRAM :- 

import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Upload image
uploaded = files.upload()
filename = next(iter(uploaded))

# Read image in grayscale
i = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

# Gaussian Filtering
g = cv2.GaussianBlur(i, (3, 3), sigmaX=1.0)

# Median Filtering
m = cv2.medianBlur(i, ksize=3)

# Bilateral Filtering
b = cv2.bilateralFilter(i, d=9, sigmaColor=75, sigmaSpace=75)

# Display Original Image
plt.figure(figsize=(15, 8))
plt.imshow(i, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()

# Display Gaussian Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(g, cmap='gray')
plt.title('Gaussian Filtered Image')
plt.axis('off')
plt.show()

# Display Median Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(m, cmap='gray')
plt.title('Median Filtered Image')
plt.axis('off')
plt.show()

# Display Bilateral Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(b, cmap='gray')
plt.title('Bilateral Filtering')
plt.axis('off')
plt.show()




------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 4
AIM :-  Perform object detection using contour detection and bounding boxes
PROGRAM :- 

import cv2
import matplotlib.pyplot as plt
from google.colab import files

# Upload image
uploaded = files.upload()

# Get uploaded filename
filename = next(iter(uploaded))

# Read image
img = cv2.imread(filename)

# Check whether image was read successfully
if img is None:
    print("Error: Image could not be read.")
else:
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, binary = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY
    )

    # Find contours
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Copy original image
    output = img.copy()

    # Draw bounding boxes
    count = 0

    for contour in contours:

        # Calculate contour area
        area = cv2.contourArea(contour)

        # Ignore small noise
        if area > 50:

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Draw rectangle
            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            count += 1

    # Convert BGR to RGB
    output_rgb = cv2.cvtColor(
        output, cv2.COLOR_BGR2RGB
    )

    # Display result
    plt.figure(figsize=(8, 6))
    plt.imshow(output_rgb)
    plt.title("Detected Objects with Bounding Boxes")
    plt.axis("off")
    plt.show()

    print("Number of objects detected:", count)







------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 5
AIM :-  Detect faces using Haar Cascade or DNN-based pre-trained models in OpenCV.
PROGRAM :- 
import cv2
from google.colab import files
from google.colab.patches import cv2_imshow

# Upload image
uploaded = files.upload()

# Get uploaded file name
filename = next(iter(uploaded))

# Read image
img = cv2.imread(filename)

# Check whether image was read successfully
if img is None:
    print("Error: Could not read the image.")
else:
    # Load Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    # Draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display results
    print("Number of faces detected:", len(faces))
    cv2_imshow(img)




------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 6
AIM :-  Preprocess text data (tokenization, stopword removal, stemming, lemmatization) using NLTK/spaCy
PROGRAM :- 
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = input("Enter a sentence or paragraph: ")

print("\nOriginal Text:")
print(text)

# 1. Tokenization
tokens = word_tokenize(text)

print("\n1. Tokenization:")
print(tokens)

# 2. Stop Word Removal
stop_words = set(stopwords.words('english'))

filtered_words = []

for word in tokens:
    if word.lower() not in stop_words:
        filtered_words.append(word)

print("\n2. After Stop Word Removal:")
print(filtered_words)

# 3. Stemming
stemmer = PorterStemmer()

stemmed_words = []

for word in filtered_words:
    stemmed_words.append(stemmer.stem(word))

print("\n3. After Stemming:")
print(stemmed_words)

# 4. Lemmatization
lemmatizer = WordNetLemmatizer()

lemmatized_words = []

for word in filtered_words:
    lemmatized_words.append(lemmatizer.lemmatize(word))

print("\n4. After Lemmatization:")
print(lemmatized_words)


-----------------------------------------------------------
OUTPUT :-
-----------------------------------------------------------
Enter a sentence or paragraph:
The cats are playing happily in the gardens.

Original Text:
The cats are playing happily in the gardens.

1. Tokenization:
['The', 'cats', 'are', 'playing', 'happily', 'in', 'the', 'gardens', '.']

2. After Stop Word Removal:
['cats', 'playing', 'happily', 'gardens', '.']

3. After Stemming:
['cat', 'play', 'happili', 'garden', '.']

4. After Lemmatization:
['cat', 'playing', 'happily', 'garden', '.']







------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 7
AIM :- Implement Part-of-Speech (POS) tagging and Named Entity Recognition (NER) using spaCy
PROGRAM :-

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
    print(f"{token.text:15} {token.pos_:10} ({spacy.explain(token.pos_)})")

# NAMED ENTITY RECOGNITION (NER)
print("\nNAMED ENTITY RECOGNITION (NER)")
if len(doc.ents) == 0:
    print("No named entities found.")
else:
    for ent in doc.ents:
        print(f"{ent.text:20} {ent.label_:10} ({spacy.explain(ent.label_)})")



If using Google Colab
First run:
pip install spacy
python -m spacy download en_core_web_sm
Then run the main code above.



--------------------------------------------------------
OUTPUT :-
--------------------------------------------------------
Enter a sentence or paragraph: RAMU EATS BANANA
Original Text:
RAMU EATS BANANA
PART-OF-SPEECH (POS) TAGGING
RAMU            PROPN      proper noun
EATS            VERB       verb
BANANA          PROPN      proper noun
NAMED ENTITY RECOGNITION (NER)
RAMU EATS BANANA    ORG        Companies, agencies, institutions, etc.





------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 8
AIM :- Build a simple sentiment analysis classifier using bag-of-words or TF-IDF and Naïve Bayes.
PROGRAM :-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training reviews
reviews = [
    "This movie is good",
    "I love this movie",
    "This movie is wonderful",
    "The product is amazing",
    "I enjoy this service",
    "This movie is bad",
    "I hate this movie",
    "This movie is worst",
    "This movie is boring",
    "This product is terrible",
    "The service is poor"
]

# Sentiment labels
labels = [
    "positive", "positive", "positive",
    "positive", "positive",
    "negative", "negative", "negative",
    "negative", "negative", "negative"
]

# Convert text into TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(reviews)

# Train Naive Bayes classifier
model = MultinomialNB()
model.fit(X, labels)

print("Model Training Completed")

# Get user review
user_review = input("Enter your review: ")

# Convert user review into TF-IDF features
review_vector = vectorizer.transform([user_review])

# Predict sentiment
prediction = model.predict(review_vector)

print("\nYour Review:", user_review)
print("Predicted Sentiment:", prediction[0])


--------------------------------------------------------
OUTPUT :-
--------------------------------------------------------
Model Training Completed
Enter your review: i like this movie alot
Your Review: i like this movie alot
Predicted Sentiment: positive




------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 9
AIM :- Perform topic modeling using Latent Dirichlet Allocation (LDA).
PROGRAM :-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Collection of documents
documents = [
    "Python Java programming computer software",
    "Python programming coding software development",
    "Java computer programming language",
    "Cricket football sports players match",
    "Football cricket players stadium sports game",
    "Cricket match players stadium sports",
    "Football sports game players"
]

# Convert documents into word frequency matrix
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Apply LDA algorithm
lda = LatentDirichletAllocation(
    n_components=2,
    random_state=42
)

lda.fit(X)

# Display topics
words = vectorizer.get_feature_names_out()

for topic_index, topic in enumerate(lda.components_):
    print(f"\nTopic {topic_index + 1}:")
    top_words = topic.argsort()[-5:][::-1]
    print(" ".join([words[i] for i in top_words]))


--------------------------------------------------------
OUTPUT :-
--------------------------------------------------------

Topic 1:
players sports cricket football match
Topic 2:
programming python computer java software







------------------------------------------------------------------------------------------------------------------------------------------------------
EXPERIMENT :- 10
AIM :- Extract text from an image using Optical Character Recognition (OCR) with Tesseract and perform text summarization.
PROGRAM :-

# Install and import required libraries
!apt-get install -y tesseract-ocr
!pip install pytesseract opencv-python-headless nltk

import cv2
import pytesseract
import nltk
import re
from google.colab import files
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Upload an image
print("Upload an image containing text:")
uploaded = files.upload()

image_path = next(iter(uploaded))

# Read image
img = cv2.imread(image_path)

# Extract text using OCR
text = pytesseract.image_to_string(img)

print("\nExtracted Text:\n")
print(text)

# Sentence tokenization
sentences = sent_tokenize(text)

# Clean extracted text
clean_text = re.sub(r'[^a-zA-Z\s]', '', text)

words = clean_text.lower().split()

# Remove stopwords
stop_words = set(stopwords.words('english'))

filtered_words = [
    word for word in words
    if word not in stop_words
]

# Calculate word frequency
frequency = FreqDist(filtered_words)

# Calculate sentence scores
scores = {}

for sentence in sentences:
    score = 0
    for word in sentence.lower().split():
        word = re.sub(r'[^a-zA-Z]', '', word)

        if word in frequency:
            score += frequency[word]

    scores[sentence] = score

# Generate summary
summary = sorted(
    scores,
    key=scores.get,
    reverse=True
)[:2]

# Display summary
print("\n===== Text Summary =====\n")

if summary:
    for sentence in sorted(summary, key=sentences.index):
        print(sentence)
else:
    print("No text found for summarization.")

print("\n===== Program Completed =====")



--------------------------------------------------------
OUTPUT :-
--------------------------------------------------------

Upload an image containing text:
sample_image.png

Extracted Text:

understanding and This chapter describes the field
of natural language and introduces some basic
distinctions.

Section 1.1 discusses how natural language
understanding research fits into the study of
language in general.

1.2 discusses some applications of natural
language understanding systems.

===== Text Summary =====

Section 1.1 discusses how natural language
understanding research fits into the study of
language in general.

1.2 discusses some applications of natural
language understanding systems.

===== Program Completed =====
------------------------------------------------------------------------------------------------------------------------------------------------------
