#!/usr/bin/env python3

import urllib.request


def read_csv(file_path, field_sep=",", record_sep="\n"):
    with urllib.request.urlopen(file_path) as req:
        data =  req.read().decode("utf-8")
    data = data.split('\n')
    keys = []
    linedData = []

    #Create list from csv file, put the keys in a list names keys, and the rest of the data in separate lines of a list name linedData
    for i in range(len(data)):
        if(i == 0):
            keys = data[i].split(',')
        else:
            linedData.append(data[i].split(','))

#Create an empty dict data (reused name cause it works well, but could be confusing?)
#Loop through the list and create a separate dictionary for each customer using the keys (id, first name, etc.) and their data. Once an entry is complete, store it in another dictionary (data) creating a dictionary of dictionaries.
    data = {}
    for i in range(len(linedData)):
        tempDict = {}
        j = 0
        for line in linedData[i]:
            tempDict.update({keys[j]: line})
            j += 1
            if(j == len(keys)):
                data.update({i: tempDict})
    return data


def get_customers_unfixed():

    data = read_csv("https://cs.indstate.edu/~lmay1/assets/sales-data/customers.csv")
    return data

def get_customers():

    data = read_csv("https://cs.indstate.edu/~lmay1/assets/sales-data/customers.csv")

    #Create dict holding city names and corresponding states with format (City : State)
    cityStates = {}
    for i in data.items():
        if(len(i[1]["State"]) == 2):
            cityStates.update({i[1]["City"] : i[1]["State"]})

    #Loop through customer data and fix any blank states
    for i in data.items():
        if(i[1]["State"] == ''):
            key = i[1]["City"]
            i[1]["State"] = cityStates[key]

    #Loop through customer data and fix any swapped states and zip codes
    for i in data.items():
        if(len(i[1]["State"]) != 2):
            buffer = i[1]["State"]
            i[1]["State"] = i[1]["Zip"]
            i[1]["Zip"] = buffer

    return data

def get_products():
    data = read_csv("https://cs.indstate.edu/~lmay1/assets/sales-data/products.csv")
    return data

def get_tax_rates():
    return read_csv("https://cs.indstate.edu/~lmay1/assets/sales-data/tax.csv")

def get_expenses():
    return read_csv("https://cs.indstate.edu/~lmay1/assets/sales-data/expenses.csv")

def get_monthly_sales():
    data = []
    for i in range(1, 13):
        number = str(i).zfill(2)
        data.append(read_csv(f"https://cs.indstate.edu/~lmay1/assets/sales-data/sales-{number}.csv"))
    return data
