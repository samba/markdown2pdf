#!/usr/bin/env python

import sys
import argparse
from document import prepare

def parse_args(args = sys.argv):
	parser = argparse.ArgumentParser(description = 'Generate PDF documents from Markdown files')
	parser.add_argument('-i', '--input', type = str, action = 'append', required = True)
	parser.add_argument('-o', '--output', type = str, action = 'store', default = None, required = False)
	parser.add_argument('--html', action = 'store_true')
	return parser.parse_args(args)


def main(args):
	
	output = args.output and open(args.output, 'wb') or sys.stdout
	document = prepare(*args.input)

	if args.html:
		output.write(document.html)
	else:
		output.write(str(document))

	return 0


if __name__ == '__main__':
	sys.exit(main(parse_args(sys.argv[1:])))