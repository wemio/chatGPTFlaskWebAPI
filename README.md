# chatGPTFlaskWebAPI

This a chatGPT API of openAI using python flask, HTML,jquery.

## Introduction
This code implements any front-end web static page to call the python version of the chatGPT API, which is convenient for websites to integrate relevant applications into their own business.
The general requirement is this: I have a website, but in the area that chatGPT cannot access, I need to submit a local data request to the proxy server, get the answer, and complete the business logic.

## Question
Here's what happens when we call the openAI API:
1, The questions will wait a long time.
2, Unstable.
3, there is a danger of title.
4, can only be used locally, not remotely called.
5. There are various problems with PHP or other request versions.

## Method
1, python version of openAI installed, using the original module call, faster, better compatibility, and will not be blocked.
2, Use python modules such as flask to publish port web services.
3, Create a static web page by yourself. You can use html+jquery and eventSource to output stream information to the web page from the server.
4, Use stream mode to get openAI's data.

## Preparation
### install openai
> pip install openai
> 
> pip install flask
> 
> pip install flask-cors
### make a flask app with:
```python
from flask import Flask, render_template, request, session
import flask
import os
import openai
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
@app.route("/chatgpt",methods=["POST","GET"])
```
### create a webpage using html/jquery in your website
Use eventSource to push the question
onmessage:meet [done] stop,others continue..
```JAVASCRIPT
var source = new EventSource("http://xxx.xxx.xxx:port/chatgpt?question="+q);
source.onmessage = function(event){
    if(event.data == "[DONE]"){
       //do something..
        source.close()
    }else{
        //show in some divs innerHTML
    }
 }
```
In the flask app,get the question parameter
```python
question = request.args.get("question","")
question = str(question).strip()
```
Create a python function use def to connect openai:
```python
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
```
Then call the function to onload the app:
```python
return render_template('chatpgt-clone.html')
```
Last run the app:
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```
The port you can customize,use 0.0.0.0 to auto fetch.

##CONTACT
Wechat official account:simcode
![image](https://user-images.githubusercontent.com/13219746/231336331-85fca8b9-8674-4bcd-ba91-5b04a2585f13.png)

