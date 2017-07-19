from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import operator
import collections
import os

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
# title = book_data["title"]
pageinfo = "mybabynamebook"

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',16)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',9)
    canvas.drawString(inch, 0.75 * inch, "%d %s" % (doc.page, pageinfo))

    canvas.restoreState()

def go(book_data):
    print(styles)
    reg_style = styles["Normal"]
    header1_style = styles["Heading1"]
    title_style = styles["Title"]
    header4_style = styles["Heading4"]
    header2_style = styles["Heading2"]
    italic_style = styles["Italic"]
    smallCentered = ParagraphStyle(name="centeredStyle", fontSize=12, alignment=TA_CENTER)
    medCentered = ParagraphStyle(name="centeredStyle", fontSize=14, alignment=TA_CENTER)

    doc = SimpleDocTemplate("media/babynamebook.pdf")
    Story = [Spacer(1,2*inch)]
    # Story.append(Spacer(PAGE_WIDTH/2.0, PAGE_HEIGHT/2.0))
    Story.append(Paragraph("%s" % (book_data["title"]), title_style))

    Story.append(Paragraph("a custom baby name book from <link href='http://www.mybabynamebook.com'>mybabynamebook</link>", smallCentered))

    Story.append(Spacer(1,3*inch))

    Story.append(Paragraph("<link href='#girls'>Girl Names</link>", medCentered))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("<link href='#boys'>Boy Names</link>", medCentered))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("<link href='#stats'>Stats</link>", medCentered))

    Story.append(PageBreak())



    Story.append(Paragraph("<a name='girls'/>Girl Names", title_style))
    Story.append(Spacer(1,0.2*inch))

    girls_list = book_data["girls"]
    girls_list = collections.OrderedDict(sorted(girls_list.items()))
    for letter in girls_list:
        Story.append(Paragraph(letter, header1_style))
        for name_dict in girls_list[letter]:

            whole_line = "<b>%s</b>  <i>(%s)</i>  %s" % (name_dict["first_name"], name_dict["origin"], name_dict["meaning"])
            Story.append(Paragraph(whole_line, reg_style))
        Story.append(Spacer(1,0.2*inch))

    Story.append(PageBreak())
    Story.append(Paragraph("<a name='boys'/>Boy Names", title_style))
    Story.append(Spacer(1,0.2*inch))
    boys_list = book_data["boys"]
    boys_list = collections.OrderedDict(sorted(boys_list.items()))

    for letter in boys_list:
        Story.append(Paragraph(letter, header1_style))
        for name_dict in boys_list[letter]:
            whole_line = "<b>%s</b>  <i>(%s)</i>  %s" % (name_dict["first_name"], name_dict["origin"], name_dict["meaning"])
            Story.append(Paragraph(whole_line, reg_style))
        Story.append(Spacer(1,0.2*inch))

    Story.append(PageBreak())
    Story.append(Paragraph("<a name='stats'/>Stats", title_style))
    Story.append(Spacer(1,0.2*inch))

    stats_chunk = book_data["stats"]
    top_female = stats_chunk["top_female"]
    top_male = stats_chunk["top_male"]
    top_origin = stats_chunk["top_origin"]
    top_last = stats_chunk["top_last"]
    pop_female = stats_chunk["pop_female"]
    pop_male = stats_chunk["pop_male"]

    Story.append(Paragraph("Most Common Girl Names", header2_style))
    for p in top_female:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Boy Names", header2_style))
    for p in top_male:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Name Origins", header2_style))
    for p in top_origin:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Last Names", header2_style))
    for p in top_last:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Popular Girl Names In Your Tree", header2_style))
    Story.append(Paragraph("(Based on SSA 2016 most popular names)", reg_style))

    for p in pop_female:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Popular Boy Names In Your Tree", header2_style))
    Story.append(Paragraph("(Based on SSA 2016 most popular names)", reg_style))

    for p in pop_male:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    return doc
#
#

# if __name__ == "__main__":
#     go()

# go(book_data)
