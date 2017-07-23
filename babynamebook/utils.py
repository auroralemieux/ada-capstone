import codecs, os, re, sys
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import urllib.request


def parse_ged(ged_file):

    with urllib.request.urlopen("https://s3-us-west-2.amazonaws.com/babynamebooktestbucket/media/" + ged_file) as response:
       ged = response.read()
    #    THIS WORKS!!!!

    ged = ged.decode("utf-8")
    print("BREADCRUMB # 4.1. READ THE GED OFF S3.")
    print("GED FILE type: ",type(ged))


    # THIS WAS THE LOCALHOST LINE
    # ged = codecs.open("media/" + ged_file, encoding="cp437")

    # xml = codecs.open("media/" + ged_file + ".xml", "w", "utf8")
    xml = ""
    print("BREADCRUMB # 4.2. READ THE XML OFF S3. ??")

    # xml.write("""<?xml version='1.0'?>\n""")
    # xml.write("<gedcom>")
    xml += ("""<?xml version='1.0'?>\n""")
    xml += ("<gedcom>")
    sub = []
    errors = []
    ged = ged.split("\n")
    for s in ged:
        s = s.strip()
        m = re.match(r"(\d+) (@(\w+)@ )?(\w+)( (.*))?", s)
        if m is None:
            errors.append("Error: unmatched line: " +s)
        else:
            level = int(m.group(1))
            id = m.group(3)
            tag = m.group(4)
            data = m.group(6)
        while len(sub) > level:
            # xml.write("</%s>\n" % (sub[-1]))
            xml += ("</%s>\n" % (sub[-1]))

            sub.pop()
        if level != len(sub):
            errors.append("Error: unexpected level: " + s)
        sub += [tag]
        if id is not None:
            # xml.write("<%s id=\"%s\">" % (tag, id))
            xml += ("<%s id=\"%s\">" % (tag, id))

        else:
            # xml.write("<%s>" % (tag))
            xml += ("<%s>" % (tag))

        if data is not None:
            m = re.match(r"@(\w+)@", data)
            if m:
                # xml.write(m.group(1))
                xml += (m.group(1))

            elif tag == "NAME":
                m = re.match(r"(.*?)/(.*?)/$", data)
                if m:
                    # xml.write("<forename>%s</forename><surname>%s</surname>" % (escape(m.group(1).strip()), escape(m.group(2))))
                    xml += ("<forename>%s</forename><surname>%s</surname>" % (escape(m.group(1).strip()), escape(m.group(2))))

                else:
                    # xml.write(escape(data))
                    xml += (escape(data))

            elif tag == "DATE":
                m = re.match(r"(((\d+)?\s+)?(\w+)?\s+)?(\d{3,})", data)
                if m:
                    if m.group(3) is not None:
                        # xml.write("<day>%s</day><month>%s</month><year>%s</year>" % (m.group(3), m.group(4), m.group(5)))
                        xml += ("<day>%s</day><month>%s</month><year>%s</year>" % (m.group(3), m.group(4), m.group(5)))

                    elif m.group(4) is not None:
                        # xml.write("<month>%s</month><year>%s</year>" % (m.group(4), m.group(5)))
                        xml += ("<month>%s</month><year>%s</year>" % (m.group(4), m.group(5)))

                    else:
                        # xml.write("<year>%s</year>" % m.group(5))
                        xml += ("<year>%s</year>" % m.group(5))

                else:
                    # xml.write(escape(data))
                    xml += (escape(data))

            else:
                # xml.write(escape(data))
                xml += (escape(data))

    while len(sub) > 0:
        # xml.write("</%s>" % sub[-1])
        xml += ("</%s>" % sub[-1])

        sub.pop()
    # xml.write("</gedcom>\n")
    xml += ("</gedcom>\n")

    ged.close()
    # xml.close()
    # xml_filename = "media/" + ged_file + ".xml"
    # return xml_filename
    return xml


def parse_xml(xml_string):

    # tree = ET.parse(xml_filename)
    # root = tree.getroot()

    root = ET.fromstring(xml_string)
    print("BREADCRUMB 4.3: created root in parse xml")
    new_book = []

    for indi in root.findall('INDI'):
        new_person = {}
        if indi.find('BIRT') is not None:
            birth = indi.find('BIRT')


            if birth.find('DATE') is not None:
                if len(birth.find('DATE')) == 0:
                    birthdate = birth.find('DATE').text
                    year = birthdate[6:]
                    if len(year) is 4 and year.isdigit():
                        year = int(year)
                    else:
                        year = 0
                else:
                    birthdate = birth.find('DATE')

                    if birthdate.find('year') is not None:
                        year = birthdate.find('year').text
                        if len(year) is 4 and year.isdigit():
                            year = int(year)
                        else:
                            year = 0
                    else:
                        year = 0

            new_person["birth_year"] = "%s" % (year)
        else:
            new_person["birth_year"] = 0


        name = indi.find('NAME')
        if name.find('forename') != None:
            first_name = name.find('forename').text
            if first_name is not None:
                if " " in first_name:
                    name_split = str.split(first_name)
                    new_person["first_name"] = name_split[0].capitalize()
                    new_person["middle_name"] = name_split[1].capitalize()
                else:
                    new_person["first_name"] = first_name.capitalize()
            else:
                new_person["first_name"] = "unknown"
        else:
            new_person["first_name"] = "unknown"
        # print(new_person["first_name"])
        if name.find('surname') is not None:
            new_person["last_name"] = name.find('surname').text
        else:
            new_person["last_name"] = "unknown"

        if indi.find("SEX") is not None:
            sex = indi.find('SEX').text
        else:
            sex = "x"

        new_person["sex"] = sex

        new_book.append(new_person)
    print("in xml parser length of new book is", len(new_book))
    # now new_book is full of person hashes
    return new_book
