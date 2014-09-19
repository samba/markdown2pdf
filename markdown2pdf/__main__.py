#!/usr/bin/env python

import sys
import argparse
from document import prepare, load

def parse_args(args = sys.argv):
	parser = argparse.ArgumentParser(description = 'Generate PDF documents from Markdown files')
	parser.add_argument('-i', '--input', type = str, action = 'append', required = False)
	parser.add_argument('-o', '--output', type = str, action = 'store', default = None, required = False)
	parser.add_argument('-c', '--config', type = str, action = 'store', default = None, required = False)
	parser.add_argument('-t', '--toc', action = 'store_true', default = False, required = False)
	parser.add_argument('--author', type = str, action = "store", default = "", required = False)
	parser.add_argument('--title', type = str, action = "store", default = "", required = False)
	parser.add_argument('--html', action = 'store_true')
	return parser.parse_args(args)


def main(args):
	
	output = args.output and open(args.output, 'wb') or sys.stdout

	if args.config:
		document = load(args.config)
	else:
		document = prepare(
			*args.input, 
			author = args.author,
			title = args.title,
			enable_toc = args.toc,
			section_break = True # TODO: make this configurable
		)

	if args.html:
		output.write(document.html)
	else:
		output.write(str(document))

	return 0


if __name__ == '__main__':
	sys.exit(main(parse_args(sys.argv[1:])))