#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
import random
from pprint import pprint

NA = list()
EU = list()
INTL = list()
EMAIL_BODY = "Hello {4},\n\n" \
             "I'm contacting  you because you volunteered to be a part of our " \
             "secret santa. Here's all the information you need about the " \
             "person you've been assigned.\n" \
             "NOTE: This is not a pairing. This person is not gifting to you. " \
             "Someone else is.\n\n" \
             "Name: {0}\n" \
             "Discord User Name: {1}\n" \
             "Address: {2}\n" \
             "Gift Ideas: {3}\n" \
             "Email: {5} (You shouldn't normally need to contact them)\n\n" \
             "Love,\nMiniac"

def generate_pairs(people):
    paired = list()
    for x in range (0, len(people)):
        if x == len(people) - 1:
            paired.insert(len(people) - 1, people[len(people) - 1])
            paired[len(people) - 1]['partner'] = people[0]
        else:
            paired.insert(x, people[x])
            paired[x]['partner'] = people[x+1]
    return paired

def send_mail(people):
    for person in people:
        partner = person['partner']
        #email = MIMEText(EMAIL_BODY.format(partner['name'], partner['discord'], partner['address'], partner['gifts']))
        print EMAIL_BODY.format(partner['name'].title(), partner['discord'],
        partner['address'], partner['gift'], person['name'].title() ,partner["email"])
        #email['From'] = 'sdubist@gmail.com'
        #email['To'] = person['email']
        #email['Subject'] = "Minipainting Discord Secret Santa!"
        #s = smtplib.SMTP('localhost')
        #s.sendmail(email)
        #s.quit

with open('responses.tsv') as f:
    lines = f.readlines()
    for line in lines:
        timestamp, zone, name, discord, email, address, gift, rematcher = line.split('\t')
        person = {
                'address': address,
                'discord': discord,
                'email': email,
                'gift': gift,
                'name': name,
                'rematcher': rematcher,
                'zone': zone,
        }
        if "North" in zone:
            NA.append(person)
        if "Europe" in zone:
            EU.append(person)
        if "International" in zone:
            INTL.append(person)

random.shuffle(NA)
random.shuffle(EU)
random.shuffle(INTL)
NA_PAIRED = generate_pairs(NA)
EU_PAIRED = generate_pairs(EU)
INTL_PAIRED = generate_pairs(INTL)

send_mail(NA_PAIRED)
