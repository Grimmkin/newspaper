import logging
import json

from pprint import pprint

from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def extract_documents():
    with open("all_links.json", "r") as file:
        data = json.load(file)

        for document in data:
            yield document

docs = list(extract_documents())

print(len(docs))
print(docs[0])

# Split the documents into tokens
tokenizer = RegexpTokenizer(r'\w+')
for idx in range(len(docs)):
    docs[idx] = docs[idx].lower() # Convert to lowercase
    docs[idx] = tokenizer.tokenize(docs[idx]) # Split into words.

# Remove words that are only one character
docs = [[token for token in doc if len(token) > 1] for doc in docs]

# Lemmatize the documents.
lemmatizer = WordNetLemmatizer()
docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]

# Only trying this - i don't think it is needed--------------------------------------------------------------------------------------------------------------

# Compute bigrams

# bigram = Phrases(docs, min_count=20)
# for idx in range(len(docs)):
#     for token in bigram[docs[idx]]:
#         if '_' in token:
#             # Token is a bigram, add to document
#             docs[idx].append(token)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

dictionary = Dictionary(docs)

dictionary.filter_extremes(no_below=20, no_above = 0.5) # <-- Here needs tweaking!

# Bag-of-words representation of the documents.
corpus = [dictionary.doc2bow(doc) for doc in docs]

print(f'Number of unique tokens: {len(dictionary)}')
print(f'Number of documents: {len(corpus)}')

# Train LDA model----------------------------------------------------------------------------------------------------------------------------------------------
num_topics = 10 # <------ Tweaking needed!
chunksize = 3000 # <------ To fit all our docs
passes = 20 # <----- Tweaking needed
iterations = 400 # <------ Tweaking needed
eval_every = 1 #<------ The goal is to set the number high enough that all the documents converge...Then set to None after optimal iteration and passes values are found

# Make an index to word dictionary
temp = dictionary[0] # This is only to "load" the dictionary
id2word = dictionary.id2token

model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)

top_topics = model.top_topics(corpus)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
avg_topic_coherence = sum([t[1] for t in top_topics])/num_topics
print(f'Average topic coherence: {avg_topic_coherence}.')

pprint(top_topics)