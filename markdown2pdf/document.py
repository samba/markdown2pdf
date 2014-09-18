
import re
import os
import sys
import markdown2
import template
import cStringIO
import ho.pisa as pisa




def codestyle(name = 'github'):
	return os.path.join(os.path.dirname(__file__), 'pygments-css', name + '.css');

def prepare(*markdown_files, **kwargs):
	base = Document(*markdown_files, **kwargs)
	base.add_stylesheet(codestyle('default'))
	return base


def write_pdf(html_text, output):
	content = cStringIO.StringIO(html_text)
	return not (pisa.CreatePDF(content, output)).err



class Document(object):

	# Load the core structural style for page layout, etc.
	__template_origin = os.path.join(os.path.dirname(__file__), 'config')
	__default_style = 'style.css'
	__default_template = 'template.html'

	@classmethod
	def render_markdown(cls, filename, safe_mode = False):
		extras = ['fenced-code-blocks', 'cuddled-lists']
		return markdown2.markdown(
			open(filename).read(), 
			extras = extras, 
			safe_mode = safe_mode
		)


	def __init__(self, *markdown_file, **options):
		self.macros = {}
		self.pages = list(markdown_file)
		self.stylesheets = [ os.path.join(self.__template_origin, self.__default_style) ]
		self.template_engine = template.TemplateEngine(self.__template_origin)
		self.template_file = self.__default_template
		self.title = options.pop('title', None)


	def use_template(self, template_file):
		if os.path.isfile(os.path.join(self.__template_origin, template_file)):
			self.template_file = template_file

	def add_stylesheet(self, filename):
		if os.path.isfile(filename):
			self.stylesheets.append(filename)

	def fill_macro(self, match):
		return self.macros.get(match.group(1), "/** unknown */")

	@property
	def style(self):
		translate = re.compile(r'\{\{\s*([a-z0-9\-_]+)\s*\}\}')
		for x in self.stylesheets:
			yield translate.sub(self.fill_macro, open(x).read())


	@property
	def html(self):
		return self.template_engine.render(self.template_file, {
				'title': self.title,
				'styles': self.style,
				'header': '',
				'footer': '',
				'pages': [ self.render_markdown(p) for p in self.pages ]
			})



	def render(self, output_buffer = None):
		return write_pdf(self.html, output_buffer or sys.stdout)

	def __str__(self):
		placeholder = cStringIO.StringIO()
		self.render(placeholder)
		return placeholder.getvalue()