import json
# convert csv to json for seeding db

master_names = open("./sample.txt", "r")

# this will be a list of json name objects
names = []
pk = 1
for line in master_names:
    data = line.split(",")
    gender = data[0]
    name = data[1]

    length = len(data)
    # get the last item
    origin = data[length-1]
    # trim off the '\n'
    origin = origin[0:len(origin)-1]

    # check for commas in the meaning itself
    if length == 4:
        meaning = data[2]
    else:
        meaning = ",".join(data[3:length-1])

    # there's no point in the db having names we can't use
    if meaning != "unknown":

        new_name = {
            "model": "babynamebook.name",
            "pk": pk,
            "fields": {
                "gender": gender,
                "first_name": name,
                "meaning": meaning,
                "origin": origin,
            }

        }
        names.append(new_name)

        pk += 1

print(len(names))
with open('names.json', 'w') as outfile:
    json.dump(names, outfile)

master_names.close()
