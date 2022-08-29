# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from utils import preprocessing, phonemize, result, link_mysql, rtvc_conn
import soundfile as sf

global answer


#Flask 객체 인스턴스 생성
app = Flask(__name__)


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
    if request.method == "GET":
        global answer       

        context, question, answer = link_mysql.load_context()
        return render_template('service_qa.html', data={"context" : context,
                                                        "question" : question,
                                                        "answer"  : answer})

    elif request.method == 'POST':

        audio, sr = preprocessing.blob_to_wav(request)

        # 전역변수 사용
        ans_transcription = answer

        # real-time voice model로 request
        ans_wav, sr = rtvc_conn.get_wav(audio, sr, ans_transcription)

        # 맞춤형 원어민 발화 데이터 저장
        sf.write("database/audio/answer.wav", ans_wav, sr)
        ans_wav, sr = sf.read('database/audio/answer.wav')

        # text -> phoneme
        model, tokenizer = phonemize.load_model(), phonemize.load_tokenizer()
        ans_phoneme = phonemize.text_to_phoneme(ans_transcription, is_stress=False)
        ans_phoneme_stress = phonemize.text_to_phoneme(ans_transcription, is_stress=True)

        # 음성파일 -> text -> phoneme
        deaf_transcription, deaf_phoneme = phonemize.speak_to_phoneme(audio, tokenizer, model, is_stress=False)

        # 점수 매기고 피드백 부분
        # https://stackoverflow.com/questions/17365289/how-to-send-audio-wav-file-generated-at-the-server-to-client-browser
        lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))
        accuracy, score = result.calculate_acc(ans_phoneme, lcs)

        # highlight
        correct_list = result.highlight(ans_phoneme, lcs)

        # to graph(image)
        result.to_graph(ans_wav, audio, smoothing=True)

        global data
        data = {"answer" : [ans_transcription, ans_phoneme_stress],
            "deaf" : [deaf_transcription, deaf_phoneme.lower()],
            "result": [accuracy, score],
            "correct_list" : correct_list }

        return redirect(url_for('feedback'))


@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html', data=data)

@app.route('/database/<filename>')
def database_download(filename):
    return send_from_directory('database', filename)

# 동영상
@app.route('/database/video/<filename>')
def video_download(filename):
    return send_from_directory('database/video', filename)

@app.route('/database/image/<filename>')
def image_download(filename):
    return send_from_directory('database/image', filename)

# 그래프
@app.route('/database/graph/<filename>')
def graph_download(filename):
    return send_from_directory('database/graph', filename)

# 오디오
@app.route('/database/audio/<filename>')
def audio_download(filename):
    return send_from_directory('database/audio', filename)


# 간이 페이지
@app.route('/service_example', methods=['GET', 'POST'])
def feedback_example():
  if request.method == "GET":
    transcription_list = ["Let's book a holiday!", "She sells ________ by the seashore!", "Can I order burger and chips please?"]
    context = "When she was a teenager, she sold small pieces of dinosaur bones to people that she found. At that time, many people saw her and said, 'She sells on the seashore.'"
    question = "What did people say to her?"
    global answer
    # answer = transcription_list[0]
    answer = transcription_list[1]
    # answer = transcription_list[2]


    
    return render_template('service_qa_example.html', data={"context" : context,
                                                    "question" : question,
                                                    "answer"  : answer})
     # phoneme변환
  ## -------------------------------------------------##
  else:
    # 발화자 목소리

    import librosa
    # audio, sr = librosa.load('example/holiday_male.wav')
    # audio, sr = librosa.load('example/seachells_male.wav') 
    # audio, sr = librosa.load('example/burger_male.wav') 

    # audio, sr = librosa.load('example/holiday_female.wav')
    audio, sr = librosa.load('example/seachells_female.wav') 
    # audio, sr = librosa.load('example/burger_female.wav') 
    print('audio 불러오기 성공!!!!')
    print(type(audio), sr)
    print(answer)

    # sf.write("deaf_ex.wav", audio, sr)

    # 전역변수 사용
    ans_transcription = answer
    ans_wav, sr = rtvc_conn.get_wav(audio, sr, ans_transcription)
    print('맞춤형 오디오 만들기 성공!')
    sf.write("database/audio/answer_ex.wav", ans_wav, sr)
    ans_wav, sr = sf.read('database/audio/answer_ex.wav')

    


    # from scipy.io.wavfile import write

    # write("example.wav", sr, wav.astype(np.float32))
    model, tokenizer = phonemize.load_model(), phonemize.load_tokenizer()
    ans_phoneme = phonemize.text_to_phoneme(ans_transcription, is_stress=False)
    ans_phoneme_stress = phonemize.text_to_phoneme(ans_transcription, is_stress=True)


    # 음성파일 -> text -> phoneme
    deaf_transcription, deaf_phoneme = phonemize.speak_to_phoneme(audio, tokenizer, model, is_stress=False)

    # https://stackoverflow.com/questions/17365289/how-to-send-audio-wav-file-generated-at-the-server-to-client-browser
    lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))
    accuracy, score = result.calculate_acc(ans_phoneme, lcs)
    
    print(accuracy)

    # highlight
    correct_list = result.highlight(ans_phoneme, lcs)
    print(correct_list)

    # to graph(image)
    ## ans_wav, deaf_wav
    result.to_graph(ans_wav, audio, smoothing=True)
    print('그래프 그리기 성공')
    global data
    data = {"answer" : [ans_transcription, ans_phoneme_stress],
           "deaf" : [deaf_transcription, deaf_phoneme.lower()],
           "result": [accuracy, score],
          #  "wav" : wav.tolist(),
          #  "wav_name" : wav_name,
           "correct_list" : correct_list }

    # result.to_graph(np.array(wav), np.array(audio))
  ## -------------------------------------------------##
    return redirect(url_for('feedback')) 



if __name__=="__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)