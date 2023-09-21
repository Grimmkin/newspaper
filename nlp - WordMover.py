import logging
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk import download

# Initialize logging.
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentence_first = 'The National Emergency Management Agency (NEMA) has donated relief materials worth over N80million to victims of flood and landslide in Abia to cushion the effects of the disaster. He said that the beneficiaries were victims of flood and landslide disasters in Umuokom community in Ikwuano LGA, Umunkpeyi-Nvosi in Isiala Ngwa South LGA and Amaeke-Ibeku in Umuahia North. Other items donated include: 1,000 pieces of foam, 1,000 pieces of blankets, 1,000 pieces of mosquito nets and 1,000 pieces of nylon mats, among others. Ugoh said the distribution of the relief materials was officially launched on Aug. 28 and concluded on Sept. 4. I want to confirm to you that the Owerri Operations office on behalf of the Director General of NEMA, Mohammed Mohammed, has concluded distribution of the relief items to victims of landslide and flood in Abia.'
sentence_second = 'The government plan to distribute N8,000 to 12 million poor households over six months as palliative support will benefit an estimated 64.88 million individuals out of 132.93 million poor people. They will receive ₦5 billion, ₦4.4 billion, ₦4.1 billion, ₦3.9 billion, and ₦3.4 billion, respectively. FCT, Abia, Edo, Ondo, and Borno are the five states receiving the lowest palliative funds. Due to their low number of poor households, they will receive ₦888 million, ₦912 million, ₦1.05 billion, ₦1.13 billion, and ₦1.5 billion, respectively. Data reveals a hurdle in fair fund distribution because individuals without bank accounts outnumber poor households.'

download('stopwords')  # Download stopwords list.
stop_words = stopwords.words('english')

def preprocess(sentence):
    return [w for w in sentence.lower().split() if w not in stop_words]

sentence_first = preprocess(sentence_first)
sentence_second = preprocess(sentence_second)

model = api.load('word2vec-google-news-300')

distance = model.wmdistance(sentence_first, sentence_second)
print(f'distance = {distance}')