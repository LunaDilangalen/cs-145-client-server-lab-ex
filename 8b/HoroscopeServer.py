import socket
import json
from datetime import datetime as dt
from datetime import timedelta as td

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
        # 0 : "Saturday",
        # 1 : "Sunday",
        # 2 : "Monday",
        # 3 : "Tuesday",
        # 4 : "Wednesday",
        # 5 : "Thursday",
        # 6 : "Friday",

        6 : "Saturday",
        0 : "Sunday",
        1 : "Monday",
        2 : "Tuesday",
        3 : "Wednesday",
        4 : "Thursday",
        5 : "Friday",


    }[h]

def ZellersRule(month, day, year):
    # alternate
    month -= 2 # shift 2
    if (month == -1):
        month = 11
    if (month == 0):
        month = 12
    year = year - 1
    # # Zeller's Rule
    # if (month == 1) :
    #     month = 13
    #     year = year - 1
    #
    # if (month == 2) :
    #     month = 14
    #     year = year - 1
    k = day
    m = month
    D = year % 100;
    C = year / 100;
    # f = k + 13 * (m + 1) // 5 + D + D // 4 + C // 4 + 5 * C
    # alternate
    f = k + (13 * (m - 1)/5) + D + (D / 4) + (C / 4) - 2 * C
    f = f % 7
    dotw = switch(f)
    return dotw

def getHoroscope(horoscope, date):
    # iterate through the horoscope json data
    # get the start and end months
    # parse start and end dates
    # check if input date is within start and end? return symbol: continue to next

    year_constant = dt.now().year
    date = date.replace(year = year_constant)

    print "date month: %d" %date.month


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

        # Create start date string to parse into a date object
        s_date = s_month + ' ' + str(s_day) + ' ' + str(date.year)

        # Create end date string to parse into a date object
        # Conditions:
        # case 1: if the months aren't January, February, and March, set end dates' year to year constant. Also set input date year to year constant (for easy comparison)
        #
        # case 2: set end dates' year to year constant + 1.
        # case 2.2: for start dates with months after Dec, set year to year constant + 1
        # case 2.1: For the input dates if the input date >= January 1, set year to year_constant + 1, else just set to year_constant



        if (e_month != 'January' and e_month != 'February' and e_month != 'March'):
            # create end date string to parse into a date object
            e_date = e_month + ' ' + str(e_day) + ' ' + str(date.year)
        else:
            # create end date string to parse into a date object
            e_date = e_month + ' ' + str(e_day) + ' ' + str(date.year + 1)

            # update the start date (months after Dec)
            if (s_month != 'December'):
                s_date = s_month + ' ' + str(s_day) + ' ' + str(date.year + 1)

                # set boundary January 1
                boundary = dt.strptime('January 1', "%B %d").replace(year = year_constant + 1)


            # update the input date if it is over dec 31
            if(date.month == 1 or date.month == 2 or date.month == 3):
                date = date.replace(year = year_constant+1)


        # convert them to date objects
        s_date = parseDate(s_date)
        e_date = parseDate(e_date)

        print s_date, date, e_date

        # check if the input date is between start and end
        if (s_date <= date <= e_date):
            sym = i['symbol']
            read = i['reading']
        date = date.replace(year = year_constant)

    return sym, read

horoscope = loadHoroscope('HOROSCOPE.json')
# print horoscope


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 58904))
serversocket.listen(5) # become a server socket, maximum 5 connections
connection, address = serversocket.accept()

while True:
    # connection, address = serversocket.accept()
    # print connection, address
    # while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        print buf
        if(buf == 'q'):
            data = buf
            connection.send(data)
            break
        else:
            date = parseDate(buf[6:])
            # print date
            dotw = ZellersRule(date.month, date.day, date.year)
            symbol, reading = getHoroscope(horoscope, date)
            data = '%s;%s;%s\n'%(dotw, symbol, reading)
            print data
            connection.send(data)
serversocket.close()
