
import string
import re
from pprint import pprint

import sys

def query( stream ): return [x for x in stream]


def table( tuple_stream, outf=sys.stdout ): 
	def find_length( tvalues, i ): 
		lens = [len(str(t[i])) for t in tvalues]
		return max(lens)

	table_values = query(tuple_stream)
	if len(table_values) > 0: 
		indices = range(len(table_values[0]))
		lengths = [ find_length(table_values, i) for i in indices ]
		for tup in table_values:
			for i in indices: 
				if i > 0: outf.write('\t')
				outf.write(str(tup[i]).ljust(lengths[i], ' '))
			outf.write('\n')

def tuples( keys, object_stream ): 
	kk = keys
	for obj in object_stream: 
		if not kk: kk = obj.keys()
		yield tuple( obj[k] for k in kk )

def objects( keys, tuple_stream ): 
	for tup in tuple_stream: 
		yield { keys[i]: tup[i] for i in range(len(keys)) }

def tuple_project( indices, tuple_stream ): 
	for tup in tuple_stream: 
		yield tuple( tup[i] for i in indices )

def object_project( keys, object_stream ): 
	for obj in object_stream: 
		yield { k: obj[k] for k in keys }

def object_subtract( keys, object_stream ): 
	for obj in object_stream: 
		yield { k: obj[k] for k in obj.keys() if not k in keys }

def filter( pred, stream ): 
	for value in stream: 
		if pred(value):
			yield value

def group_tuples_by( index, stream ): 
	keyed = {}
	for tup in stream: 
		if not tup[index] in keyed: keyed[tup[index]] = []
		keyed[tup[index]].append(tup)
	return [ (k, keyed[k]) for k in keyed.keys() ]

def group_objects_by( key, stream ): 
	keyed = {}
	for obj in stream: 
		if not obj[key] in keyed: keyed[obj[key]] = []
		keyed[obj[key]].append(obj)
	return [ (k, keyed[k]) for k in keyed.keys()]

def count( stream ): 
	for (k, values) in stream: 
		yield (k, len(values))
