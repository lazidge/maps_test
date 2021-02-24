 # Parser example
# Usage python parser_ex.py 

import sys
from datetime import datetime

from osm_parser import get_default_parser

# The first argument after the python module on the commandline
filename = sys.argv[1]

# Parse the supplied OSM file
start = datetime.now()

parser = get_default_parser(filename)

nodes = 0
for node in parser.iter_nodes():
    nodes += 1

end = datetime.now()

print("The data contains", nodes, "nodes")
print("Parsing the date took", (end - start).total_seconds(), "seconds")
