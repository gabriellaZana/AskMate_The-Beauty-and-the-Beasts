import base64
import csv
import time
from datetime import datetime


def string_to_base64(origin):
    origin_in_bytes = origin.encode('utf-8')
    b64_encoded_bytes = base64.b64encode(origin_in_bytes)
    return b64_encoded_bytes.decode('utf-8')


def base64_to_string(encoded_string):
    decoded_string = base64.b64decode(encoded_string)
    return decoded_string.decode('utf-8')


def print_info(variable):
    print("Original string: {var} ({type})".format(**{
        "var": variable,
        "type": type(variable)
    }))


def import_story(filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    table = []
    for row in reader:
        row[4] = base64_to_string(row[4])
        if filename == "data/question.csv":
            row[5] = base64_to_string(row[5])
        table.append(row)
    return table


def export_story(filename, table):
    file = open(filename, 'w')
    writer = csv.writer(file)
    for row in table:
        row[4] = string_to_base64(row[4])
        if filename == "data/question.csv":
            row[5] = string_to_base64(row[5])
        writer.writerow(row)


def id_generator(csv_filename):
    with open(csv_filename, 'r') as f:
        lastrow = None
        for lastrow in csv.reader(f):
            pass
        if lastrow is None:
            return "1"
        else:
            return str(int(lastrow[0]) + 1)


def append_story(new_question_or_answer, filename):
    with open(str(filename), 'a', newline='') as outputstream:
        writer = csv.writer(outputstream)
        new_question_or_answer[1] = int(time.time())
        new_question_or_answer[4] = string_to_base64(new_question_or_answer[4])
        if filename == "data/question.csv":
            new_question_or_answer[5] = string_to_base64(new_question_or_answer[5])
        writer.writerow(new_question_or_answer)