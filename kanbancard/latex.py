"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.
"""
import sys
import jinja2
import subprocess
import tempfile
from os import path


def render_templated_tex(tex, **options):
    r"""
    Renders latex code template with data from the options dict, lookcing for \VAR{} and \BLOCK{} in the template.

    Arguments:
        -tex (str): the templated latex code to be filled in

    Approach taken from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
    """
    env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
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


def pdflatex(tex):
    """
    Returns the pdf bytestring from pdflatex's rendering of the 'tex' string.
    (Auxillary files are stored in temporary directory and deleted.)
    """
    shell = True if sys.platform == 'linux' else False
    with tempfile.TemporaryDirectory() as output_dir:
        subprocess.run(r'pdflatex -output-directory {dir}'.format(dir=output_dir), input=tex.encode(), shell=shell)
        with open(path.join(output_dir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
            return pdf
