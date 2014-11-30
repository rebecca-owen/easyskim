import mendeley
import json

def query(metadata):
	j = json.loads(metadata)
	doi = j["DOI"]
	Author = j["Author"]
	print doi
	print Author
	print "Number of Mendeley Readers: " + session.catalog.by_identifier(doi, view='stats').reader_count
	print "Other Papers by Author in Catalogue: " + session.catalog.advanced_search(author=Author)
	print "Full citation: " + session.catalog.by_identifier(doi, view='bib')

	return None

f = open("metadata.met")
print query(f.read())