import jinja2

from jinja2 import contextfunction, contextfilter


class TemplateEngine(object):

	def __init__(self, *template_paths):
		self.environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(template_paths),
			extensions=[ 
				'jinja2.ext.autoescape', 
				'jinja2.ext.i18n', 
				'jinja2.ext.do', 
				'jinja2.ext.loopcontrols', 
				'jinja2.ext.with_'
				],
			autoescape=True
		)


	def addTemplateFilter(self, method, name = None):
		self.environment.filters[ name or method.__name__ ] = method

	def addTemplateTag(self, method, name = None):
		self.environment.globals[ name or method.__name__ ] = method

	def render(self, path, values):
		return self.environment.get_template(path).render(values)