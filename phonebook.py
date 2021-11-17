# читаем адресную книгу в формате CSV в список phone_book_data
from collections import defaultdict
import csv
import re

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_book = []

for cl in contacts_list:
    phone_book_list = []
    fio_p = "[\w]+"
    telephone_p = re.compile(r"(\+7|8)?[- .]?((\()?((?:\d{2,3})))(\))?[-"
                             r" .]?(\d{3})[- .]?(\d{2})(\D|\S)?(\d{2})")
    telephone_add_p = re.compile(r"(\+\d\D+\d+\S+)\D+(\d{4})(\)*)")
    fio = re.findall(fio_p, str(cl[0:3]), re.U)
    telephone = telephone_p.sub(r"+7 (\4)\6-\7-\9", cl[5])
    telephone_add = telephone_add_p.sub(r"\1 доб.\2", telephone)
    phone_book_list.append(fio[0])
    try:
        phone_book_list.append(fio[1])
        phone_book_list.append(fio[2])
    except IndexError:
        phone_book_list.append('')
    phone_book_list.append(cl[3])
    phone_book_list.append(cl[4])
    phone_book_list.append(telephone_add)
    phone_book_list.append(cl[6])
    phone_book.append(phone_book_list)

contact_data = defaultdict(list)

for info in phone_book:
    key = tuple(info[:2])
    for item in info:
        if item not in contact_data[key]:
            contact_data[key].append(item)

phone_book_data = list(contact_data.values())

with open("phonebook.csv", "w", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phone_book_data)

