import os, re
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html", message="Hello Flask!")

@app.route('/search', methods = ['POST'])
def search():
	search_sequences = request.form['squence']

	# save search_sequences to a text file
	f = open('./input.txt', 'w')
	f.write(search_sequences)
	f.close()
	search_sequences = search_sequences.split('\r\n')

	# CALL Desirae's code to put this into a FASTA FILE
	os.system('Rscript ./search_engine/R_script_Desirae.R')

	# RUN BLAST
	os.system('./search_engine/blastp -threshold 14 -query queryout.txt -db ./database/demo.fasta -out blast_results.txt')

	# parse output
	outputs = parse_BLAST_output('blast_results.txt')
	print(outputs)

	return(render_template("output.html", outputs = outputs))

	

def parse_BLAST_output(filename):
	start_recording = False
	entry = '' 	 # will convert to html syntax
	entries = [] # list of entry
	for line in open(filename):
		# find if this is start of recording 
		if 'Query=' in line:
			start_recording = True
		# stop recording if hit the lambda line
		if 'Lambda' in line:
			start_recording = False
		if start_recording:
			if 'Query=' in line:
				# append to output
				if entry != '':
					entries.append(entry)
				# start a new entry
				entry = '<pre>' + line.replace('\n', '') + '</pre>'  # for displaying in html
			else:
				# append to current entry
				if line == '\n':
					entry = entry + '<br>'
				else:
					entry = entry + '<pre>' + line.replace('\n', '') + '</pre>'
	return entries


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)