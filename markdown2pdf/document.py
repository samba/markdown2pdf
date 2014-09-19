
import re
import os
import yaml
import markdown2
import template
import cStringIO
from xhtml2pdf.document import pisaDocument
import hashlib

def mask_pisa_logging_error(active = True):
	if active:
		import logging
		class nullLogger(logging.Handler):
			level = 0
			def emit(self, record):
				pass
		logging.getLogger('xhtml2pdf').addHandler(nullLogger())
		logging.getLogger('ho.pisa').addHandler(nullLogger())


mask_pisa_logging_error(True)

def load(config_file):
	config = Objectify(yaml.load(open(config_file)))


def prepare(*markdown_files, **options):
	base = Document(*markdown_files, **options)
	base.stylesheets.append(base.codestyle('default'))
	return base

def asset_paths(cwd = None):
	_local = os.path.dirname(__file__)
	return [
		cwd or os.getcwd(),
		os.path.join(_local, 'config'),
		os.path.join(_local, 'pygments-css')
	]



class Objectify(object):
    def __init__(self, base = None):
        if isinstance(base, dict):
            self.update(base)

    def update(self, *data, **options):
        for elem in data:
            if isinstance(elem, dict):
                self.__dict__.update(elem)
        self.__dict__.update(options)
        for key, value in self.__dict__.iteritems():
            if isinstance(value, dict):
                self.__dict__[key] = Objectify(value)
            elif isinstance(value, list):
                self.__dict__[key] = [ (isinstance(elem, dict) and Objectify(elem) or elem) for elem in value ]



class Document(markdown2.Markdown):

	# Load the core structural style for page layout, etc.
	__default_style = 'default_page.css'
	__default_template = 'default_page.html'

	default_extras = [
		'fenced-code-blocks',
		'cuddled-lists',
		'header-ids',
		'metadata',
		'toc' # This will override the PDF table of content magic
	]

	@classmethod
	def codestyle(cls, name = 'default'):
		for path in asset_paths():
			if os.path.isfile(os.path.join(path, name + '.css')):
				return name + '.css'


	def __init__(self, *pages, **options):
		self.page_files = pages
		self.context = {
			"author": options.get('author', None),
			"title": options.get('title', None),
			"subject": options.get('subject', None),
			"footer": options.get('footer', ''),
			"header": options.get('header', '')
		}
		self.stylesheets = [ self.__default_style ]
		self.link_patterns = None
		self.template_file = options.get('template', self.__default_template)

		super(Document, self).__init__(
			safe_mode = True,
			extras = self.default_extras,
			link_patterns = self.link_patterns,
			use_file_vars = True
		)

	def translate(self, text, *context, **options):
		default = options.pop('default', None)
		_pattern = re.compile(r'\{\{\s*([\w\d_\-]+)\s*\}\}')
		def _translate(match):
			for c in context:
				if match.group(1) in c:
					return c.get(match.group(1))
			return (default is None) and (match.group(0)) or default 
		return _pattern.sub(_translate, text)



	@property 
	def pages(self):
		context = {}
		context.update(self.context)
		for filename in self.page_files:
			content = self.convert(open(filename).read())
			context.update(content.metadata)
			# This translation runs here to support file-local variables before it reaches Jinja
			text = self.translate(str(content), context)
			yield text, context


	@property
	def html(self):

		t_engine = template.TemplateEngine(*asset_paths())

		root_context = self.context

		pages, context = [], None
		for page, context in self.pages:
			pages.append(page)
			for k, v in context.iteritems():
				if not (root_context.get(k, None)):
					root_context[k] = v


		root_context.update({
			"styles": self.stylesheets,
			"pages": pages
		})
		
		return t_engine.render(self.template_file, root_context)


	def fix_anchor_name(self, text):
		pattern = re.compile(r'<([hH][0-9])\s+id="([^\"]+)"([^>]*)>(.*?)</\1>')
		return pattern.sub(r'<a name="\g<2>">\n\g<0></a>', text)


	def render_pdf(self, output_buffer):
		return not pisaDocument(cStringIO.StringIO(self.html), output_buffer).err

	def __str__(self):
		_buffer = cStringIO.StringIO()
		self.render_pdf(_buffer)
		return _buffer.getvalue()





