from flask import Flask, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.debug=True
load_dotenv()
client = OpenAI()
client.api_key=os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['POST'])
def home():
    mymessage = request.get_json()["prompt"]
    assistant_id ="asst_JTCSfhHOOtm0DgMEZTTWxsX8"

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=mymessage
    )
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
    )
    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    for mess in messages:
      if(mess.role=="assistant"):
         myresponse=mess.content[0].text.value
      break

    print(myresponse)
    return jsonify("response",myresponse)
if __name__ == '__main__':
    app.run()