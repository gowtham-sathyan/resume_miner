from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import requests
import os
import re
import time
from extract_text import extract
stanza.download('en')
app = Flask(__name__)
cors = CORS(app)

@app.route('/resume',methods=['POST'])
@cross_origin()
def get_results():
	f=request.files['file']
	filename=str(time.time())+".pdf"
	f.save(filename)
	payload=extract(filename)
	# pdf_text=extract_text(filename)
	return(jsonify(payload))

if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)
	# app.run(debug=True)