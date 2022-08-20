# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils import preprocessing, phonemize, result
import io
import soundfile as sf


#Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/') # 접속하는 url
def index():
  return render_template('index.html',user="반원",data={'level':60,'point':360,'exp':45000})


@app.route('/record', methods=["GET", "POST"])
def record():
  if request.method == "GET":
    return render_template('record.html')
  else:

  # phoneme변환
  ## -------------------------------------------------##
    print(request.files, type(request))
    audio_input = request.files['file'].read()
    print(type(audio_input))

    data, samplerate = sf.read(io.BytesIO(audio_input))
    print(data.shape, samplerate)

    model, tokenizer = phonemize.load_model(), phonemize.load_tokenizer()
    ans_transcription = "Hello, my name is Ryan"
    ans_phoneme = phonemize.text_to_phoneme(ans_transcription, is_stress=False)

    print('정답')
    print(ans_transcription)
    print(ans_phoneme, end='\n\n')

    # 음성파일 -> text -> phoneme
    deaf_transcription, deaf_phoneme = phonemize.speak_to_phoneme(data, tokenizer, model, is_stress=False)

    print('발화자')
    print(deaf_transcription)
    print(deaf_phoneme)

    print('result')

    lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))
    accuracy, score = result.calculate_acc(ans_phoneme, lcs)
    print(accuracy, score)
    data = {"answer" : [ans_transcription, ans_phoneme],
           "deaf" : [deaf_transcription, deaf_phoneme],
           "result": [accuracy, score] }
  ## -------------------------------------------------##
    return data





  

if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  app.run(host="127.0.0.1", port="5000", debug=True)