
import re
import os
import sys
import markdown2
import cStringIO
import ho.pisa as pisa

DOCUMENT_TEMPLATE = """
<html>
	<head>
	    <title>{title}</title>
	    <style>
	    	{style}
	    </style>
	</head>
	<body>
		{body}
	</body>
</html>
"""


# Load the core structural style for page layout, etc.
__default_style = os.path.join(os.path.dirname(__file__), 'config', 'style.css')

def codestyle(name = 'github'):
	return os.path.join(os.path.dirname(__file__), 'pygments-css', name + '.css');

def prepare(markdown_file, title = None):
	base = Document(markdown_file, title or markdown_file)
	base.add_stylesheet(__default_style)
	base.add_stylesheet(codestyle('default'))
	return base


def write_pdf(html_text, output):
	content = cStringIO.StringIO(html_text)
	return not (pisa.CreatePDF(content, output)).err



class Document(object):

	@classmethod
	def render_markdown(cls, filename, safe_mode = False):
		extras = ['fenced-code-blocks', 'cuddled-lists']
		return markdown2.markdown(
			open(filename).read(), 
			extras = extras, 
			safe_mode = safe_mode
		)


	def __init__(self, markdown_file, title = '(untitled)', stylesheet = None):
		self.macros = {}
		self.template = DOCUMENT_TEMPLATE
		self.title = title
		self.body_text = self.render_markdown(markdown_file)
		self.style_text = stylesheet or ""


	def add_stylesheet(self, filename):
		if os.path.isfile(filename):
			self.style_text = self.style_text + "\n" + open(filename).read()

	def fill_macro(self, match):
		return self.macros.get(match.group(1), "/** unknown */")

	@property
	def html(self):
		search = r'\{\{\s*([a-z0-9\-_]+)\s*\}\}'
		return self.template.format(
			title = self.title,
			body = self.body_text,
			style = re.sub(search, self.fill_macro, self.style_text))

	def render(self, output_buffer = None):
		return write_pdf(self.html, output_buffer or sys.stdout)

	def __str__(self):
		placeholder = cStringIO.StringIO()
		self.render(placeholder)
		return placeholder.getvalue()