from flask import Flask, render_template, make_response, request
app = Flask(__name__)
 
@app.route('/', methods=['GET', "POST"])
def hello():
  if request.method == "POST":
    input = request
    print(input)
    return {"name" : '선홍', 'age': 25}
  else:
    return render_template('example.html')
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port = 80, debug = True)
