'''
API for text summarization

https://deepai.org/machine-learning-model/summarization


'''

import requests
import io
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import string

class Summarize():

    def __init__(self, key='061c9c38-576a-458b-b0dd-5b94e6bbcfca'):
        self.key = key
        self.stop_words = ENGLISH_STOP_WORDS.union(set(string.punctuation))

    def tokenize(self, text):
        '''returns tokenized text'''
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        stems = []
        for item in tagged:
            word, tag = item
            if word in self.stop_words:
                continue
            if word.startswith('\''):
                continue
            if tag.startswith('N'):
                #continue
                stems.append(word)
            # stems.append(PorterStemmer().stem(item))
        return stems

    def summarize(self, text, verbose=False):
        '''
        text:       either 'file', 'url' or 'raw', corresponding to a file handle, a url to text, or the raw text respectively
        returns:    a string containing the summary
        '''
        response = requests.post(
            "https://api.deepai.org/api/summarization",
            data={
                'text': text,
            },
            headers={'api-key': self.key}
        )
        summary = response.json()['output']
        if verbose:
            print(summary)
        return summary
    
    def keywords(self, text, k=30):
        '''extract top k keywords from email content'''
        vectorizer = TfidfVectorizer(tokenizer=self.tokenize, lowercase=True, )#stop_words=set(ENGLISH_STOP_WORDS)
        X = vectorizer.fit_transform([text]).toarray().squeeze()
        words = np.array(vectorizer.get_feature_names())
        order = np.argsort(X)[::-1]
        topk_words = words[order[:k]]
        topk_words.sort()
        filtered = [topk_words[0]]
        for i in range(1, len(topk_words)):
            if str(PorterStemmer().stem(topk_words[i])) == str(PorterStemmer().stem(topk_words[i-1])):
                continue
            filtered.append(topk_words[i])
        return filtered

if __name__ == '__main__':
    summarizer = Summarize()
    emails = [
        """The University of Michigan-Ann Arbor is proud to host the 2021 Veterans Week celebration, running Nov. 8-12, 2021. This annual event features a week of programming that educates and celebrates the experiences and sacrifice of those who have served our country. All events are free and are open to the entire university community and to the general public unless otherwise noted. We encourage you to attend as many of these events as you can. Out of an abundance of caution for the health of our community and our veterans, we will be offering all events as either hybrid virtual/in-person formats or entirely virtual formats. Please join us for respectful, educational, and inspirational panels, lectures, and stories via the links below each program. You can also visit the Veterans Week webpage for updates and more information."""
        ]
    text = """Peter, application deadlines are rapidly approaching! If you're ready to apply, head to gradapply.rice.edu. Deadlines vary by program, so be sure to verify the deadlines that pertain to your application.
        Have lingering questions about grad school life or the application process? Join us Thursday, Nov. 18, to chat with our Graduate Student Ambassadors at one of our Coffee Chats - sign up for the time that works for you here!
        To help you decide your plan of action, we've listed some commonly asked questions below, and more are on our website. Not seeing your question? Let us know! Refer to your program of interest for additional application requirements.
        How can I take a campus tour?
        We're happy to share our virtual tour with you! Click on the image below to watch a video about Rice's beautiful, green campus, set in the heart of Houston. You can also virtually visit Rice at one of our upcoming Coffee Chats! Register here.
        Where should my official transcripts be sent?
        Send official transcripts directly to the program to which you intend to apply. You may also upload an unofficial transcript directly within your online application.
        How do I report my GRE or TOEFL scores?
        A reminder that this year the GRE is optional at Rice, excluding programs in the Jones School of Business, though many programs will suggest you submit scores. To officially report your scores, visit the ETS website to order score reports if you did not do so on your test day. The ETS institutional reporting code for Rice University is 6609. Please allow 2-4 weeks for scores to reach Rice.
        I sent my GRE/TOEFL scores, but the application system shows my scores as pending.
        If your scores are not yet showing in your application, you can check with ETS to make sure you sent the scores using the correct code. You can also contact the program you are applying to and make them aware of this. They can open your application and match the scores.
        How are letters of recommendation submitted?
        Letters can be submitted within the application itself using a valid email address for your recommenders. More on this here.
        My recommender didn't get the request. What do I do?
        Please note that it is possible that the email generated by our application system was filtered as spam. You can log back into the application and resend your letter of recommendation.
        Can I edit my application after I submit it?
        Some programs will permit important minor edits to your application; please contact them directly with requests."""
    
    #summarizer.summarize(text, verbose=True)
    keywords = summarizer.keywords(text, k=10)
    print(keywords)

''' documentation

# Example posting a text URL:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example posting a local text file:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    files={
        'text': open('/path/to/your/file.txt', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example directly sending a text string:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_HERE',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


###############################################################################

import base64

# Let's use deepAI developed API
# https://docs.deepaffects.com/docs/text-summary-api.html

url = "https://proxy.api.deepaffects.com/text/generic/api/v1/async/summary"

querystring = {"apikey":"<API_KEY>", "webhook":"<WEBHOOK_URL>"}

payload = {"summaryType": "abstractive", "model": "iamus", "summaryData": [{"speakerId":"spk", "text":"text blob for speaker"}]}

headers = {
    'Content-Type': "application/json",
}

response = requests.post(url, json=payload, headers=headers, params=querystring)


'''