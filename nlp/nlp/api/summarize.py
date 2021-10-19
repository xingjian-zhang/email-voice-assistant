'''
API for text summarization

Let's use deepAI developed API
https://docs.deepaffects.com/docs/text-summary-api.html
'''

import requests
import base64

url = "https://proxy.api.deepaffects.com/text/generic/api/v1/async/summary"

def summarize(text, verbose=False):
    '''
    text:       raw text string to be summarized
    returns:    a string containing the summary
    '''

    querystring = {"apikey":"<API_KEY>", "webhook":"<WEBHOOK_URL>"}

    payload = {"summaryType": "abstractive", "model": "iamus", "summaryData": [{"speakerId":"spk", "text":"text blob for speaker"}]}

    headers = {
        'Content-Type': "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    if verbose:
        print(response.text)

    return response.text