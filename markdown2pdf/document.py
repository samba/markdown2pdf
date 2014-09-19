
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


def prepare(*markdown_files, **options):
	return Document(*markdown_files, **options)



def load(yaml_file):
	basepath = os.path.dirname(yaml_file)
	doc = Document.fromBookConfig(yaml_file, assets = basepath)
	return doc
	





class Document(markdown2.Markdown):

	# Load the core structural style for page layout, etc.
	__default_style = 'default_page.css'
	__default_code_style = 'default'
	__default_template = 'default_page.html'

	default_extras = [
		'fenced-code-blocks',
		'cuddled-lists',
		'header-ids',
		'metadata',
		'toc' # This will override the PDF table of content magic
	]

	@staticmethod
	def paths(cwd = None):
		_local = os.path.dirname(__file__)
		return [
			cwd or os.getcwd(),
			os.path.join(_local, 'config'),
			os.path.join(_local, 'pygments-css')
		]


	@classmethod
	def fromBookConfig(cls, filename, **options):
		config = yaml.load(open(filename))
		book = config.get('book', None)
		if book is not None:
			book.update(options)
			return cls(*book.get('parts', []), **book)


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
			"header": options.get('header', ''),
			"section_break": options.get('section_break', True),
			"enable_toc": options.get('enable_toc', True),
			"enable_placeholders": options.get('enable_placeholders', False)
		}
		self.stylesheets = [ self.__default_style, self.__default_code_style + '.css' ]
		self.link_patterns = None
		self.template_file = options.get('template', self.__default_template)
		self.asset_path = options.get('assets', None)

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

	def resolve_path(self, filename, *paths):
		if os.path.isfile(filename):
			return filename
		for path in paths:
			q = os.path.join(path, filename)
			if os.path.isfile(q):
				return q


	def pages(self, *paths):
		context = {}
		context.update(self.context)
		for filename in self.page_files:
			readpath = self.resolve_path(filename, *paths)
			if readpath:
				content = self.convert(open(readpath).read())
				context.update(content.metadata)
				# This translation runs here to support file-local variables before it reaches Jinja
				text = self.translate(str(content), context)
				yield text, context


	@property
	def html(self):

		search_path = self.paths(self.asset_path)
		t_engine = template.TemplateEngine(*search_path)
		root_context = self.context

		pages, context = [], None
		for page, context in self.pages(*search_path):
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





