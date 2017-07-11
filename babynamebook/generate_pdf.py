from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Baby Name Book"
pageinfo = "platypus example"

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT/2.0, Title)
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
    doc = SimpleDocTemplate("phello.pdf")
    Story = [Spacer(1,2*inch)]
    style = styles["Normal"]
    # for i in range(100):
    #     bogustext = ("Paragraph number %s. " % i) *20
    #     p = Paragraph(bogustext, style)
    #     Story.append(p)
    #     Story.append(Spacer(1,0.2*inch))
    for letter, namelist in book_data["boys"]:
        Story.append(letter)
        Story.append(Spacer(1,0.2*inch))

        for name in namelist:
            whole_line = "%s (%s) %s" % (name["first_name"], name["origin"], name["meaning"]
            p = Paragraph(whole_line, style)
            Story.append(p)
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

# if __name__ == "__main__":
#     go()
book_data = {
    "title": "Aurora's tree",
    "stats": [
        {"top_female": ["one", "two", "three"]},
        {"top_male": ["four", "five", "six"]},
        {"top_origin": ["english", "french", "latin"]},
        {"pop_female": ["one", "two", "three"]},
        {"pop_male": ["one", "two", "three"]},

    ],
    "boys": {
        "A": [
            {
                "first_name": "Abel",
                "origin": "Hebrew",
                "meaning": "somethingorother",
            },
            {
                "first_name": "Andrew",
                "origin": "French",
                "meaning": "no idea",
            },
        ],
        "B": [
            {
                "first_name": "Bart",
                "origin": "Hebrew",
                "meaning": "doesn't matter",
            },
            {
                "first_name": "Benjamin",
                "origin": "Hebrew",
                "meaning": "ben jammin'",
            },
        ],
    },
    "girls": {
        "A": [
            {
                "first_name": "Alice",
                "origin": "Hebrew",
                "meaning": "somethingorother",
            },
            {
                "first_name": "Aurora",
                "origin": "French",
                "meaning": "no idea",
            },
        ],
        "B": [
            {
                "first_name": "Beatrice",
                "origin": "Hebrew",
                "meaning": "doesn't matter",
            },
            {
                "first_name": "Belinda",
                "origin": "Hebrew",
                "meaning": "ben jammin'",
            },
        ],
    },
}
go(book_data)
