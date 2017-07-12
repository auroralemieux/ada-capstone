from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import operator
import collections
import os

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
# title = book_data["title"]
pageinfo = "babynamebook"

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT/2.0, "My Baby Name Book")
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()
    canvas.showPage()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def go(book_data):
    # save_name = os.path.join(os.path.expanduser("~"), "Desktop/testbabynamebook.pdf")
    doc = SimpleDocTemplate("media/babynamebook.pdf")
    Story = [Spacer(1,2*inch)]

    reg_style = styles["Normal"]
    header1_style = styles["Heading1"]
    title_style = styles["Title"]
    header4_style = styles["Heading4"]
    header2_style = styles["Heading2"]
    italic_style = styles["Italic"]

    Story.append(Paragraph("Girl Names", title_style))
    Story.append(Spacer(1,0.2*inch))
    print("BOOK DATA KEYS: ")
    print(book_data.keys())
    girls_list = book_data["girls"]
    girls_list = collections.OrderedDict(sorted(girls_list.items()))
    for letter in girls_list:
        # print(letter)
        Story.append(Paragraph(letter, header1_style))
        # Story.append(Spacer(1,0.2*inch))
        for name_dict in girls_list[letter]:

            whole_line = "<b>%s</b>  <i>(%s)</i>  %s" % (name_dict["first_name"], name_dict["origin"], name_dict["meaning"])
            # print(whole_line)
            Story.append(Paragraph(whole_line, reg_style))
        Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Boy Names", title_style))
    Story.append(Spacer(1,0.2*inch))
    boys_list = book_data["boys"]
    boys_list = collections.OrderedDict(sorted(boys_list.items()))

    for letter in boys_list:
        # print(letter)
        Story.append(Paragraph(letter, header1_style))
        # Story.append(Spacer(1,0.2*inch))
        for name_dict in boys_list[letter]:
            whole_line = "<b>%s</b>  <i>(%s)</i>  %s" % (name_dict["first_name"], name_dict["origin"], name_dict["meaning"])
            # print(whole_line)
            Story.append(Paragraph(whole_line, reg_style))
        Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Stats", title_style))
    Story.append(Spacer(1,0.2*inch))

    stats_chunk = book_data["stats"]
    top_female = stats_chunk["top_female"]
    top_male = stats_chunk["top_male"]
    top_origin = stats_chunk["top_origin"]
    top_last = stats_chunk["top_last"]
    pop_female = stats_chunk["pop_female"]
    pop_male = stats_chunk["pop_male"]

    Story.append(Paragraph("Most Common Girl Names", header2_style))
    # Story.append(Spacer(1,0.2*inch))
    for p in top_female:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Boy Names", header2_style))
    # Story.append(Spacer(1,0.2*inch))
    for p in top_male:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Name Origins", header2_style))
    # Story.append(Spacer(1,0.2*inch))
    for p in top_origin:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Most Common Last Names", header2_style))
    # Story.append(Spacer(1,0.2*inch))
    for p in top_last:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Popular Girl Names In Your Tree", header2_style))
    Story.append(Paragraph("(Based on SSA 2016 most popular names)", reg_style))

    # Story.append(Spacer(1,0.2*inch))
    for p in pop_female:
        Story.append(Paragraph(p, reg_style))
    Story.append(Spacer(1,0.2*inch))

    Story.append(Paragraph("Popular Boy Names In Your Tree", header2_style))
    Story.append(Paragraph("(Based on SSA 2016 most popular names)", reg_style))

    # Story.append(Spacer(1,0.2*inch))
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
