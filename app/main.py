from flask import Flask, request

app= Flask(__name__, static_url_path='/build')

@app.route('/')
def index():
  return app.send_static_file('./index.html')
