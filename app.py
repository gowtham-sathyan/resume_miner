from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import requests
import subprocess
import time
from extract_text import extraction
app = Flask(__name__)
cors = CORS(app)

@app.route('/resume',methods=['POST'])
@cross_origin()
def get_results():
	f=request.files['file']
	filename=str(time.time())+".pdf"
	f.save(filename)
	payload=pdf_extractor.extract(filename)
	subprocess.run(["rm",filename])
	# pdf_text=extract_text(filename)
	return(jsonify(payload))

pdf_extractor=extraction()
if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)
	# app.run(debug=True)