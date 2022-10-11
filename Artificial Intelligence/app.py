from flask import *;
from Questions import *;
from nltk import tokenize;
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.secret_key = 'your secret key here'


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('home.html')

@app.route('/index', methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["POST", "GET"])
def about():
    return render_template('about.html')

@app.route('/convert', methods=['POST'])
def convert():
    text= request.form['text']
    type= request.form['type']
    print(type)
    text=tokenize.sent_tokenize(text)
    pprint(text)
    response={
            'output':[]
        }
    for i in text:
        payload={"input_text": i}
        
        if (type=="0"):
            response['output'].append(mcq_questions(payload))
        if (type=="1"):
            response['output'].append (faq_questions(payload))
        if (type=="2"):
            response['output'].append(paraphrasing_questions(payload, 5))
        if (type=="3"):
            response['output'].append( boolean_questions(payload))
        # else:
        #     response= {"error": "Invalid type"}
        # response=mcq_questions(payload)
        # boolean_questions(payload)
        # faq_questions(payload)
        # response={'message':'success'}
    pprint(response)
    return response,200


@app.route('/questionType', methods=["POST", "GET"])
def questionType():
    return render_template('questions.html')

@app.route('/ytToText', methods=['POST'])
def ytToText():
    link= request.form['link']
    # print(link)
    vid_id = link[32:]
    text= getTranscript(vid_id)
    response={'message': text}
    return response,200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)