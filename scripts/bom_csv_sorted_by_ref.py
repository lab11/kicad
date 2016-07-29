#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Ungrouped (One component per row) CSV output
#

"""
    @package
    Generate a csv list file.
    Components are sorted by ref
    One component per line
    Fields are (if exist)
    Ref, value, Part, footprint, Datasheet, Manufacturer, Vendor
"""

from __future__ import print_function

# Import the KiCad python helper module
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2] + "_BOM.csv", 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

# override csv.writer's writerow() to support utf8 encoding:
def writerow( acsvwriter, columns ):
    utf8row = []
    for col in columns:
        utf8row.append( str(col) )
    acsvwriter.writerow( utf8row )

components = net.getInterestingComponents()

# Output a field delimited header line
writerow( out, ['Source:', net.getSource()] )
writerow( out, ['Date:', net.getDate()] )
writerow( out, ['Tool:', net.getTool()] )
writerow( out, ['Component Count:', len(components)] )
writerow( out, ['Refs', 'Value', 'Qty', 'Vendor 1', 'Vendor 1 Part Number', 'Bought'] )

grouped_components = {}
for c in components:
    part_num = c.getField("Vendor 1 Part Number")
    if part_num == "":
        if c.getValue() not in grouped_components:
            grouped_components[c.getValue()] = {"refs": "",
                                                "qty": 0,
                                                "Vendor 1": c.getField("Vendor 1"),
                                                "Vendor 1 Part Number": c.getField("Vendor 1 Part Number"), 
                                                "val": c.getValue()}
        grouped_components[c.getValue()]["refs"] += c.getRef() + " "
        grouped_components[c.getValue()]["qty"] += 1
        print("moo")
    else: 
        k = (part_num, c.getField("Vendor 1"))
        print(k)
        if k not in grouped_components:
            grouped_components[k] = {"refs": "",
                                     "qty": 0,
                                     "Vendor 1": c.getField("Vendor 1"),
                                     "Vendor 1 Part Number": c.getField("Vendor 1 Part Number"), 
                                     "val": c.getValue()}
        grouped_components[k]["refs"] += c.getRef() + " "
        grouped_components[k]["qty"] += 1

keys = sorted(grouped_components.keys())
sorted_parts = []
for k in keys:
    sorted_parts.append(grouped_components[k])

sorted_parts = sorted(sorted_parts, key=lambda p:p["refs"])

for g in sorted_parts:
    writerow( out, [g["refs"], g["val"], g["qty"], g["Vendor 1"], g["Vendor 1 Part Number"]])
