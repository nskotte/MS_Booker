from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns
from flask import Flask, render_template, request, make_response
from io import BytesIO


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
	pdf = generate_pdf(data_filename=filename, csv_data=csv_data)
	response = make_response(pdf)
	response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
	response.mimetype = 'application/pdf'
	return response


@app.route('/download', methods=['POST'])
def download():
	with open('./data/test.csv') as f:
		csv = f.read()
	response = make_response(csv)
	response.headers['Content-Disposition'] = "inline; filename='example_sequence.csv"
	response.mimetype = 'text/csv'
	return response


def generate_pdf(data_filename, csv_data, template_file='templates/card_template.tex'):

	# Read / Validate CSV Sequence File
	df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
	metadata = dict([el.strip().lstrip() for el in item.split(':')] for item in df['Comment'][0].split(','))

	# Render to PDF Card via Latex
	options = {
		'Project': metadata['Project'],
		'BatchID': 1,
		'Date': datetime.now().strftime('%d.%m.%Y'),
		'Filename': path.basename(data_filename),
		'df': df,
		'Comments': metadata,
		'Researcher': metadata['Researcher'],
	}

	with open(template_file) as f:
		tex = latex.render_templated_tex(tex=f.read(), **options)
		return latex.pdflatex(tex=tex)


if __name__ == '__main__':
	app.run(debug=True)