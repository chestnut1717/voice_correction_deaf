import requests
import json
import numpy as np
from utils.mysql_connect import mysql_connect

# url1 = "http://localhost/encoder/inference/"
url1 = "https://better-encoder.herokuapp.com/inference/"
url2 = "https://better-synthesizer.herokuapp.com/inference/"
url3 = "https://better-vocoder.herokuapp.com/inference/"

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

    # encoder -> syn
    response1 = requests.request("GET", url1, headers=headers, data=wav_json)
    print(response1)
    print('response1 완료')

    encoder_request_data = json.dumps({
        "embed": response1.json(),
        "text": text
    })

    #syn -> vocoder
    response2 = requests.request("GET", url2, headers=headers, data=encoder_request_data)
    print(response2)

    print('response2 완료')

    vocoder_request_data = json.dumps({
        "spec": response2.json(),
        "sr": sr
    })

    # vocoder -> wav
    response3 = requests.request("GET", url3, headers=headers, data=vocoder_request_data)
    print(response3)

    print("response3 완료")


    # data from DB
    conn = mysql_connect()
    wav_list = conn.get_wav()
    print(len(wav_list))


    wav = np.array(wav_list)
    sr = 16000
    print(len(wav))
    return wav, sr