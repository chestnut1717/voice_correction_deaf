# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from utils import preprocessing, phonemize, result
import rtvc_conn
import numpy as np
import noisereduce as nr
import soundfile as sf


#Flask 객체 인스턴스 생성
app = Flask(__name__)


# Home
@app.route('/hello', methods=['GET']) 
def hello():
  return redirect('example')

@app.route('/example', methods=['GET']) 
def example():
  return render_template('example.html')


# Home
@app.route('/', methods=['GET']) 
def index():
  return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    # db에 저장하는 코드 들어온다
    # return redirect(~~~)
    pass
  elif request.method == 'GET':
    return render_template('login.html')





@app.route('/service_qa', methods=["GET", "POST"])
def record():
  global ans_transcription
  # print(request.headers)

  if request.method == "GET":
    
    import pymysql


    host = "betterdatabase.cyooqkxaxvqu.us-east-1.rds.amazonaws.com"
    username = "admin"
    password = "jung0204"
    port = 3306
    database = "better"

    db = pymysql.connect(
                        host=host, 
                        port=port, 
                        user=username, passwd=password, 
                        db=database, charset='utf8'
                        )
    import random
    rdm = random.randint(1, 10)

    sql = f"SELECT * FROM better_context_qa where better_context_qa.context_qa_id =  {rdm}"
    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            result_sql = cur.fetchall()[0]

    global answer       
    context, question, answer = result_sql[1], result_sql[2], result_sql[3]


    
    return render_template('service_qa.html', data={"context" : context,
                                                    "question" : question,
                                                    "answer"  : answer})

    
  else:

  # phoneme변환
  ## -------------------------------------------------##
    audio, sr = preprocessing.blob_to_wav(request)
    # noise reduce code
    audio_reduced = nr.reduce_noise(y=audio, sr=sr)

    sf.write("deaf.wav", audio, sr)

    # 전역변수 사용
    ans_transcription = answer
    wav, sr = rtvc_conn.get_wav(audio, sr, ans_transcription)
    sf.write("answer.wav", wav, sr)


    from scipy.io.wavfile import write

    write("example.wav", sr, wav.astype(np.float32))
    model, tokenizer = phonemize.load_model(), phonemize.load_tokenizer()
    ans_phoneme = phonemize.text_to_phoneme(ans_transcription, is_stress=False)

    # 음성파일 -> text -> phoneme
    deaf_transcription, deaf_phoneme = phonemize.speak_to_phoneme(audio, tokenizer, model, is_stress=False)

    # https://stackoverflow.com/questions/17365289/how-to-send-audio-wav-file-generated-at-the-server-to-client-browser
    lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))
    accuracy, score = result.calculate_acc(ans_phoneme, lcs)
    print(accuracy)

    global data
    data = {"answer" : [ans_transcription, ans_phoneme],
           "deaf" : [deaf_transcription, deaf_phoneme],
           "result": [accuracy, score],
           "wav" : wav.tolist() }

    # result.to_graph(np.array(wav), np.array(audio))
  ## -------------------------------------------------##
    return redirect(url_for('feedback'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
  return render_template('feedback.html', data=data)



if __name__=="__main__":
  # host 등을 직접 지정하고 싶다면
  app.run(host="127.0.0.1", port="5000", debug=True)