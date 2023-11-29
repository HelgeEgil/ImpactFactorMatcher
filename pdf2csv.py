import pandas as pd
import camelot
import pprint
import re

def pdf2csv():
	# Found from https://impactfactorforjournal.com/jcr-impact-factor-2022/
	filename = "Impact-Factor-2023-PDF.pdf"
	pages = list()

	# PDF coordinate space
	# A4: 595 by 842, each unit 1/72 inch

	# (x1,y1) left top
	# (x2,y2) right bottom

	# first page, in mms
	# size 694 x 986 px
	x1mm = 42
	y1mm = 163
	x2mm = 596
	y2mm = 935

	x1 = int(x1mm * 595 / 694)
	x2 = int(x2mm * 595 / 694)
	y1 = int(842 - y1mm * 842 / 986)
	y2 = int(842 - y2mm * 842 / 986)

	area = f"{x1},{y1},{x2},{y2}"
	tables = camelot.read_pdf(filename, pages="1", flavor='stream', table_areas=[area])

	pages.append(tables[0].df)

	# now page size is 608 * 860

	x1mm = 32
	y1mm = 45
	x2mm = 529
	y2mm = 808

	x1 = int(x1mm * 595 / 608)
	x2 = int(x2mm * 595 / 608)
	y1 = int(842 - y1mm * 842 / 860)
	y2 = int(842 - y2mm * 842 / 860)

	area = f"{x1},{y1},{x2},{y2}"

	tables = camelot.read_pdf(filename, pages="2-end", flavor='stream', table_areas=[area])
	for table in tables:
		pages.append(table.df)

	common_frame = pd.concat(pages, ignore_index=True)
	common_frame.to_csv("impactFactor.csv", header=False, index=False, sep=";")

if __name__ == "__main__":
	pdf2csv()