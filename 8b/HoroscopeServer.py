import socket
import json
from datetime import datetime as dt

# load HOROSCOPE.json
def loadHoroscope(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# parse date string
def parseDate(input):
    date = dt.strptime(input, '%B %d %Y')
    return date

# gets the day of the week
def switch(h) :
    return {
        0 : "Saturday",
        1 : "Sunday",
        2 : "Monday",
        3 : "Tuesday",
        4 : "Wednesday",
        5 : "Thursday",
        6 : "Friday",
    }[h]

def ZellersRule(month, day, year):
    # Zeller's Rule
    if (month == 1) :
        month = 13
        year = year - 1

    if (month == 2) :
        month = 14
        year = year - 1
    q = day
    m = month
    k = year % 100;
    j = year // 100;
    h = q + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j
    h = h % 7
    dotw = switch(h)
    return dotw

def getHoroscope(horoscope, date):
    # iterate through the horoscope json data
    # get the start and end months
    # parse start and end dates
    # check if input date is within start and end? return symbol: continue to next

    for i in horoscope:
        # print i['start']['month'], i['end']['month']

        # start date
        s_month = i['start']['month']
        s_day = i['start']['day']

        # end date
        e_month = i['end']['month']
        e_day = i['end']['day']

        # special case: if end month is Jan
        # add 1 year

        # start and end dates as strings
        s_date = s_month + ' ' + str(s_day) + ' ' + str(date.year)
        if (e_month != 'January'):
            e_date = e_month + ' ' + str(e_day) + ' ' + str(date.year)
        else:
            e_date = e_month + ' ' + str(e_day) + ' ' + str(date.year + 1)

        # convert them to date objects
        s_date = parseDate(s_date)
        e_date = parseDate(e_date)

        # print s_date, e_date

        # check if the input date is between start and end
        if (s_date <= date <= e_date):
            symbol = i['symbol']
            reading = i['reading']

    return symbol, reading










horoscope = loadHoroscope('HOROSCOPE.json')
# print horoscope


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 58900))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    # print connection, address
    # while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        # print buf
        date = parseDate(buf[6:])
        dotw = ZellersRule(date.month, date.day, date.year)
        symbol, reading = getHoroscope(horoscope, date)
        data = '%s;%s;%s'%(dotw, symbol, reading)
        connection.send(data)
        break
