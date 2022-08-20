from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from phonemizer import phonemize
import torch
import numpy as np

def load_tokenizer():
    # model과 tokenizer pre-trained된 것 가져오기

    tokenizer = Wav2Vec2Tokenizer.from_pretrained("C:/Users//User1//Desktop//project//voice_correction_deaf//web_flask//tokenizer")
    # tokenizer.save_pretrained("/tokenizer")

    return tokenizer

def load_model():
    model = Wav2Vec2ForCTC.from_pretrained("C:/Users//User1//Desktop//project//voice_correction_deaf//web_flask//model")
    # model.save_pretrained("/model")
    return model


def speak_to_phoneme(audio, tokenizer, model, is_stress=False):
    assert type(audio) == np.ndarray
    # 유저 발화 파일 tokenizer에 넣기
    input_values = tokenizer(audio, return_tensors = "pt").input_values

    # 모델을 통해 logit값 출력(non_normalized)
    logits = model(input_values).logits

    # argmax를 통해 가장 가능성 높은 logits 들을 예측 logits으로
    prediction = torch.argmax(logits, dim = -1)

    # decoeding해서 text로 변환
    transcription = tokenizer.batch_decode(prediction)[0]

    print(transcription)

    phoneme = text_to_phoneme(transcription, is_stress)
    return transcription, phoneme


# text -> 음소
def text_to_phoneme(transcription, is_stress=False):
    assert type(transcription) == str
    # 라이브러리를 활용해서 phoneme 변환
    phoneme = phonemize(transcription, with_stress=is_stress).rstrip()
    return phoneme

