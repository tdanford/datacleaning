#!/usr/local/bin/python

import string
import re
import sys

#GTF format:
# 0: seqname - name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix.
# 1: source - name of the program that generated this feature, or the data source (database or project name)
# 2: feature - feature type name, e.g. Gene, Variation, Similarity
# 3: start - Start position of the feature, with sequence numbering starting at 1.
# 4: end - End position of the feature, with sequence numbering starting at 1.
# 5: score - A floating point value.
# 6: strand - defined as + (forward) or - (reverse).
# 7: frame - One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..
# 8: attribute - A semicolon-separated list of tag-value pairs, providing additional information about each feature.

GTF_HEADER = [ 'seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute' ]

attr_pattern = re.compile('\\s*(\\w+) "([^"]*)"')

def read_lines( filename ): 
	inf = open(filename, 'r')
	for line in inf.readlines(): 
		yield line.rstrip('\n')
	inf.close()

def parse_line_to_object( line ): 
	tokens = [x for x in line.split('\t')]
	if len(tokens) != len(GTF_HEADER): 
		print 'tokens %d != header %d' % ( len(tokens), len(header) )
	obj = { GTF_HEADER[i]: tokens[i] for i in range(len(GTF_HEADER)) }
	return obj

class ParseError( Exception ): 
	def __init__(self, msg): 
		self.msg = msg
	def __repr__(self): self.msg

def parse_attributes( attrs ): 
	def parse_token(token):
		matcher = attr_pattern.match(token)
		if matcher: return ( matcher.group(1), matcher.group(2) )
		else: raise ParseError('Could\'t parse "%s"' % token)
	tokens = [parse_token(t) for t in attrs.split(';') if len(t) > 0]
	obj = { x[0]: x[1] for x in tokens }
	return obj

def append( obj1, obj2 ):
	for k in obj2.keys(): obj1[k] = obj2[k]
	return obj1

def parse_gtf_line( line ): 
	try:
		obj = parse_line_to_object(line)
		if not 'attribute' in obj: print obj
		attrs = obj['attribute']
		del obj['attribute']
		return append( obj, parse_attributes(attrs) )
	except Exception as e: 
		print 'Cannot parse GTF line "%s" with error %s' % ( line, e )

## Central entry point, parses a GTF file and produces one object-per-line
def parse( filename ): 
	for line in read_lines( filename ): 
		if not line.startswith('#'):
			yield parse_gtf_line( line )

def main(args): 
	try: 
		for obj in parse(args[0]): 
			if obj['feature'] == 'gene' and obj['source'] == 'protein_coding': 
				print obj
	except Exception: 
		pass

if __name__=='__main__': main(sys.argv[1:])
