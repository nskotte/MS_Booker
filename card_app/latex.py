"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.
"""
import sys
import jinja2
import subprocess
import tempfile
from os import path
from io import BytesIO
from PyPDF2 import PdfFileMerger


def render_templated_tex(tex, **options):
    r"""
    Renders latex code template with data from the options dict, lookcing for \VAR{} and \BLOCK{} in the template.

    Arguments:
        -tex (str): the templated latex code to be filled in

    Approach taken from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
    """
    env = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.BaseLoader()
    )
    template = env.from_string(tex)
    rendered_tex = template.render(**options)
    return rendered_tex


def pdflatex(tex, **files):
    """
    Returns the pdf bytestring from pdflatex's rendering of the 'tex' string.
    (Auxillary files are stored in temporary directory and deleted.)

    Files (in BytesIO) can be added to the temporary directory.  The keyword names will be the filename.
    """
    shell = True if sys.platform == 'linux' else False
    with tempfile.TemporaryDirectory() as output_dir:
        for name in files:
            with open(name, 'wb') as f:
            # with open(path.join(output_dir, name), 'wb') as f:
                f.write(files[name])
        subprocess.run(r'pdflatex -output-directory {dir} -include-directory={dir}'.format(dir=output_dir), input=tex.encode(), shell=shell)
        with open(path.join(output_dir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
            return pdf


def merge_pdfs(*pdf_data):
    """Returns a joined pdf version of any number of pdf data arguments."""
    pdf_merger = PdfFileMerger()
    for pdf in pdf_data:
        pdf_merger.append(BytesIO(pdf))

    with BytesIO() as f:
        pdf_merger.write(f)
        f.seek(0)
        return f.read()
