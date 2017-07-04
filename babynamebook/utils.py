from .models import Book, Person
import codecs, os, re, sys
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET


def parse_ged(ged_file):
    # with open(ged_file, 'r') as ged:
    ged = codecs.open(ged_file, encoding="cp437")
    xml = ""
    xml += "#<?xml version='1.0'?>\n"
    xml += "<gedcom>"
    sub = []
    errors = []
    for s in ged:
        s = s.strip()
        m = re.match(r"(\d+) (@(\w+)@ )?(\w+)( (.*))?", s)
        if m is None:
            errors.append("Error: unmatched line:", s)
        else:
            level = int(m.group(1))
            id = m.group(3)
            tag = m.group(4)
            data = m.group(6)
        while len(sub) > level:
            xml += "</%s>\n" % (sub[-1])
            sub.pop()
        if level != len(sub):
            errors.append("Error: unexpected level:", s)
        sub += [tag]
        if id is not None:
            xml += "<%s id=\"%s\">" % (tag, id)
        else:
            xml += "<%s>" % (tag)
        if data is not None:
            m = re.match(r"@(\w+)@", data)
            if m:
                xml += m.group(1)
            elif tag == "NAME":
                m = re.match(r"(.*?)/(.*?)/$", data)
                if m:
                    xml += "<forename>%s</forename><surname>%s</surname>" % (escape(m.group(1).strip()), escape(m.group(2)))
                else:
                    xml += escape(data)
            elif tag == "DATE":
                m = re.match(r"(((\d+)?\s+)?(\w+)?\s+)?(\d{3,})", data)
                if m:
                    if m.group(3) is not None:
                        xml += "<day>%s</day><month>%s</month><year>%s</year>" % (m.group(3), m.group(4), m.group(5))
                    elif m.group(4) is not None:
                        xml += "<month>%s</month><year>%s</year>" % (m.group(4), m.group(5))
                    else:
                        xml += "<year>%s</year>" % m.group(5)
                else:
                    xml += escape(data)
            else:
                xml += escape(data)
    while len(sub) > 0:
        xml += "</%s>" % sub[-1]
        sub.pop()
    xml += "</gedcom>\n"
    ged.close()
    return xml


def parse_xml(xml):

    tree = ET.parse(xml)
    root = tree.getroot()

    new_book = []
    counter = 0

    for indi in root.findall('INDI'):
        counter += 1
        new_person = {}
        if indi.find('BIRT') is not None:
            birth = indi.find('BIRT')


            if birth.find('DATE') is not None:
                if len(birth.find('DATE')) == 0:
                    birthdate = birth.find('DATE').text
                    year = birthdate[6:]
                else:
                    birthdate = birth.find('DATE')

                    if birthdate.find('year') is not None:
                        year = birthdate.find('year').text
                    else:
                        year = "unknown"

            new_person["birth_year"] = "%s" % (year)
        else:
            new_person["birth_year"] = "unknown"


        name = indi.find('NAME')
        if name.find('forename') is not None:
            new_person["first_name"] = name.find('forename').text
        else:
            new_person["first_name"] = "unknown"

        if name.find('surname') is not None:
            new_person["last_name"] = name.find('surname').text
        else:
            new_person["last_name"] = "unknown"

        if indi.find("SEX") is not None:
            sex = indi.find('SEX').text
        else:
            sex = "unknown"

        new_person["sex"] = sex

        new_book.append(new_person)

    # now new_book is full of person hashes
    return new_book
