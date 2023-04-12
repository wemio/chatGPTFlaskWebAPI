from flask import Flask, render_template, request, session
import flask
import os
import openai
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
@app.route("/chatgpt",methods=["POST","GET"])
def chatgpt():
    question = request.args.get("question","")
    question = str(question).strip()
    data = ''
    if question:
        def stream():
            openai.api_key = "YOUR API-KEY"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "user", "content": question}
                ],
                temperature=0,
                #max_tokens=1000,
                stream=True,
                #top_p=1,
                #frequency_penalty=0,
                #presence_penalty=0,
                #user='Wemio机器人'
            )
            for trunk in response:
                if trunk['choices'][0]['finish_reason'] is not None:
                    data = '[DONE]'
                else:
                    data = trunk['choices'][0]['delta'].get('content','')
                yield "data: %s\n\n" % data.replace("\n","<br>")
        return flask.Response(stream(),mimetype="text/event-stream")
    return render_template('chatpgt-clone.html')

app.run(host="0.0.0.0", port=5000, debug=True)
