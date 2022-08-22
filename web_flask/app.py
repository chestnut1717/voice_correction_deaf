# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils import preprocessing, phonemize, result


#Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/') # 접속하는 url
def index():
  return render_template('index.html',user="반원",data={'level':60,'point':360,'exp':45000})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    # db에 저장하는 코드 들어온다
    # return redirect(~~~)
    pass
  elif request.method == 'GET':
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # db와 사용자 데이터가 일치하는지 확인
    # 일치 안하면 alert 보내고 다시 그 창 머무르기
    # 일치하면 service창이든 뭐든 redirect 하기
    pass
  
  elif request.method == "GET":
    return render_template('login.html')



@app.route('/home',  methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('home.html')
  else:
    return redirect(url_for("record"))


@app.route('/record', methods=["GET", "POST"])
def record():
  print(request.headers)
  if request.method == "GET":
    return render_template('record.html', question = '안뇽')

  else:
    print(dir(request))

  # phoneme변환
  ## -------------------------------------------------##
    audio, _ = preprocessing.blob_to_wav(request)

    model, tokenizer = phonemize.load_model(), phonemize.load_tokenizer()
    ans_transcription = "Hello, my name is Ryan"
    ans_phoneme = phonemize.text_to_phoneme(ans_transcription, is_stress=False)

    # 음성파일 -> text -> phoneme
    deaf_transcription, deaf_phoneme = phonemize.speak_to_phoneme(audio, tokenizer, model, is_stress=False)

    lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))
    accuracy, score = result.calculate_acc(ans_phoneme, lcs)

    data = {"answer" : [ans_transcription, ans_phoneme],
           "deaf" : [deaf_transcription, deaf_phoneme],
           "result": [accuracy, score] }
  ## -------------------------------------------------##
    return data





if __name__=="__main__":
  # host 등을 직접 지정하고 싶다면
  app.run(host="127.0.0.1", port="5000", debug=True)