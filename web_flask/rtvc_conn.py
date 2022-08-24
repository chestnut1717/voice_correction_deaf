import requests
import json
import numpy as np

url = "http://localhost/encoder/inference/"
def get_wav(wav, sr, text):
    wav = wav.tolist()
    # print("\n\n-----\n{}\n\n-----\n\n".format(type(wav)))
    wav_json = json.dumps({
        "wav": wav,
        "sr": sr,
        "text": text
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=wav_json)
    wav = np.array(response.json())
    sr = 16000
    return wav, sr