import jinja2

class TemplateEngine(object):

	def __init__(self, template_path):
		self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            extensions=[ 
            	'jinja2.ext.autoescape', 
            	'jinja2.ext.i18n', 
            	'jinja2.ext.do', 
            	'jinja2.ext.loopcontrols', 
            	'jinja2.ext.with_'
            	],
            autoescape=True)

	def render(self, path, values):
		return self.environment.get_template(path).render(values)