
def import_story(filename="question.csv"):
    file = open(filename, 'r')
    reader = csv.reader(file)
    table = []
    for row in reader:
        table.append(row)
    print(table)
    return table