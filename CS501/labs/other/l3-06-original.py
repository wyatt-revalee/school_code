#!/usr/bin/env python3


#This code, unfortunately, takes a while (~30 seconds) to compute, but it does work!. It is probably very ineffecient and I am sure there is a much faster way to achieve the same result.
#Nonetheless, it works. Just too many nested loops. All of the nesting and data just scrambled my brain a bit
#After giving it some more thought, instead of looping through each month, i could probably just assign a tuple with the customer id, quantity, AND month of purchase, so that I only need to loop through monthlySales once, rather than 12 times
#Not sure if I have the time to do that, so the code may remain as is for now.


# Equations
# Revenue = Price * Quantity * (1 + State Tax Rate)
# Gross Profit = (Price - Cost) * Quantity)
# Net Profit = Gross Profit - Expenses

# Customer Data Stats
# 01. Given the customers.csv data file, what percent of FirstName fields are left blank?
# 02. Given the customers.csv data file, what percent of LastName fields are left blank?
# 03. Given the customers.csv data file, what percent of Zip fields are left blank?
# 04. Given the customers.csv data file, what percent of State fields are left blank?
# 05. Given the customers.csv data file, what percent of Zip and State fields switched?

# Sales Data - Monthly
# 06. Which month saw the largest total revenue, and what was the value?
# 07. Which month saw the largest gross profit, and what was the value?
# 08. Which month saw the largest net profit, and what was the value?
# 09. Which month saw the smallest total revenue, and what was the value?
# 10. Which month saw the smallest gross profit, and what was the value?
# 11. Which month saw the smallest net profit, and what was the value?

# Sales Data - Annual
# 12. What product generated the most revenue over the entire year (Price * Quantity * ( 1 + State Sales Tax Rate )), and what was the amount?
# 13. What product sold the best in terms of quantity (Total Quantity Sold), and what was the number?
# 14. What product was the most profitable over the entire year (Gross Profit), and what was the amount?
# 15. What product generated the least revenue over the entire year (Price * Quantity * ( 1 + State Sales Tax Rate )), and what was the amount?
# 16. What product sold the worst in terms of quantity (Total Quantity Sold), and what was the number?
# 17. What product was the least profitable over the entire year (Gross Profit), and what was the amount?

# Files
# https://cs.indstate.edu/~lmay1/assets/sales-data/customers.csv
# https://cs.indstate.edu/~lmay1/assets/sales-data/expenses.csv
# https://cs.indstate.edu/~lmay1/assets/sales-data/products.csv
# https://cs.indstate.edu/~lmay1/assets/sales-data/tax.csv
# https://cs.indstate.edu/~lmay1/assets/sales-data/sales-01.csv

from utils import *

# From your utils file, uncomment as needed
customers = get_customers()
products = get_products()
tax_rates = get_tax_rates()
# expenses = get_expenses()
all_sales = get_monthly_sales()

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
#Dictionary credit to https://gist.github.com/rogerallen/1583593

#Create a dictionary with format {product: [(state, quantity), (..., ...)...]}
stateSales = {}

#Create a list of tuples in the format (product, price)
prices = []
for i in range(len(products)):
    prices.append(tuple((products[i]["ProductId"], products[i]["Price"])))
    stateSales.update({products[i]["ProductId"] : []})

#Create dictionary of dictionaries, each is a month with a dictionary of products, which each have corresponding lists containing how many have been sold in each state.
monthlySales = {}
for i in range(12):
    monthlySales.update({i: {}})

    #initialize months as keys and products as dictionaries, with id's being the key
    #{month: {product id: []} and an empty list (for the states and units sold)
    for j in range(len(prices)):
        monthlySales[i].update({prices[j][0]: []})


# Loop through each month of sales, update monthlySales products data (list) with a tuple containing the customer's id and quantity purchased
for i in range(12):
    for j in range(len(all_sales[i])):
        for product in monthlySales[i].items():
            if(product[0] == all_sales[i][j]["ProductId"]):
                product[1].append(tuple((all_sales[i][j]["CustomerId"], all_sales[i][j]["Quantity"])))

#Create new dictionary of sales, with the information parsed into a more calculable format (i.e. turning the customerId's into states into the tax rates)
for i in range(12):
    for product in monthlySales[i].items():
        for k in range(len(product[1])):
            for j in range(len(customers)):
                if(customers[j]["CustomerId"] == product[1][k][0]):
                    key = str(product[0])
                    if(customers[j]["State"] != '' and len(customers[j]["State"]) != 5):
                        key2 = customers[j]["State"]
                    for l in range(50):
                        if(tax_rates[l]["State"] == abbrev_to_us_state[key2]):
                            stateSales[key].append(tuple((i, tax_rates[l]["Rate"], product[1][k][1])))

#Initialize list of monthly revenues, with indexes matching up to months (0 = January)
monthlyRevenue = []
for i in range(12):
    monthlyRevenue.append(0)

#Add values into months by multiplying price*quantity*taxRate
for i in stateSales.items():
    for j in i[1]:
        for k in range(len(prices)):
            if(i[0] == prices[k][0]):
                key = j[0]
                monthlyRevenue[key] += (float(prices[k][1]) * float(j[2]) * ( (float(j[1][:-1]) / 100) + 1 ))

#Initialze a few variables, maxRev to find the highest revenue, maxMonth to keep track of what month the highest revenue occured in, and months to match up with the maxMonth index for printing purposes
maxRev = 0
maxMonth = 0
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#Iterate through list of revenues for each month, find the largest rev and print it and its corresponding month
for i in range(len(monthlyRevenue)):
    if(monthlyRevenue[i] > maxRev):
        maxRev = monthlyRevenue[i]
        maxMonth = months[i]


print(f"{maxMonth} had the most revenue with $ {maxRev:,.2f}.")
