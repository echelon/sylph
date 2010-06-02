from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import URIRef, Literal, BNode, RDF
from rdflib import Namespace as NS

from sylph.utils.Intermediary import Intermediary

from cStringIO import StringIO

class RdfParser(object):
	"""A basic wrapper for RdfLib's RDF parser.
	This class aims to accomplish easier parsing, extraction of Models,
	etc."""

	def __init__(self, rdf, format='guess'):
		"""Init the parser with the graph string."""
		self.graph = Graph()
		if format == 'guess':
			format = self.__guess_format(rdf)
			print 'RdfParser guesses format to be: %s' % format
		self.graph.load(StringIO(rdf), format=format)

	def extract(self, datatype):
		"""Extract all of the data of a given datatype."""
		data = []
		ns = Intermediary.NAMESPACES['sylph'] # TODO: Awkward.
		for sub in self.graph.subjects(RDF.type, ns[datatype]):
			idx = str(sub)
			item = {'uri': idx}
			for pred, obj in self.graph.predicate_objects(sub):
				if pred == RDF.type:
					continue
				if obj == ns['None']:
					obj = None
				if type(obj) == Literal:
					obj = str(obj)
				predstr = str(pred).rpartition('#')[2].rpartition('/')[2]
				item[predstr] = obj
			data.append(item)
		return data

	@staticmethod
	def __guess_format(st):
		"""Guess the format of the input string."""
		# TODO: At present, it can only guess between XML and n3, even
		# then this is a vague heuristic.
		if st.startswith('<'):
			return 'xml'
		return 'n3'

