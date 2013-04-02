#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Depends on the PyPDF2( https://github.com/knowah/PyPDF2/ )
import PyPDF2


# Exclude the right and left blank
#   @param in_pdf original pdf file path
#   @param out_pdf output pdf file path
#   @param leftBlankWidth the left blank width
#   @param rightBlankWidth the right blank width 
def cropPdfBlank( in_pdf, out_pdf, leftBlankWidth = 0, rightBlankWidth = 0 ):
    i = PyPDF2.PdfFileReader( file(in_pdf,"rb"))
    o = PyPDF2.PdfFileWriter()

    for page in i.pages:
        page.mediaBox.upperRight = (
            page.mediaBox.getUpperRight_x() - rightBlankWidth,
            page.mediaBox.getUpperRight_y()
        )

        page.mediaBox.lowerLeft = (
            page.mediaBox.getLowerLeft_x() + leftBlankWidth,
            page.mediaBox.getLowerLeft_y()
        )

        o.addPage(page)

    outstream = file( out_pdf, "wb")
    o.write(outstream)



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: {0} <in_pdf> <out_pdf> <leftBlankWidth> <rightBlankWidth>".format(sys.argv[0])
        print "     in_pdf:  original pdf file path"
        print "     out_pdf:   output pdf file path"
        print "     leftBlankWidth:  the left blank width, example: 50"
        print "     rightBlankWidth:   the right blank width, example: 50"
        sys.exit()

    cropPdfBlank(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))


