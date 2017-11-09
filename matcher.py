#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
import random
from pprint import pprint

NA = list()
EU = list()
INTL = list()
# DON'T FORGET TO SET THESE!
FROMADDR = ""
PASSWORD = ""
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
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROMADDR, PASSWORD)
    try:
        for person in people:
            partner = person['partner']
            msg = EMAIL_BODY.format(partner['name'], partner['discord'], partner['address'], partner['gift'], person['name'], partner['email'])
            server.sendmail(FROMADDR, person['email'], msg)
            print "sent mail to {0}".format(person['email'])
    except:
        print "error occurred while sending mail"
        print "Gifter: {0}".format(person['name'])
        print "Giftee: {0}".format(person['partner']['name'])
        server.quit()
    finally:
        server.quit()

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
send_mail(EU_PAIRED)
send_mail(INTL_PAIRED)

