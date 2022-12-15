#!/usr/bin/env python3

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


#Initialize dictionaries with names of products for later uses

#sales to store sales for each product, salesNTax to later convert customerId's to tax rates
sales = {}
salesNTax = {}

#annRevs to store annual revenues of each product
annRevs = {}

#prices to store prices of each product (in an easier to iterate format compared to products)
prices = {}

for i in products.items():
    sales.update({i[1]["ProductId"] : []})
    salesNTax.update({i[1]["ProductId"] : []})
    annRevs.update({i[1]["ProductId"] : 0})
    prices.update({i[1]["ProductId"] : i[1]["Price"]})

#make dictionary states to store the states of customers by their id's
states = {}
#make rates to later store the tax rates of customers by their id's
rates = {}
for i in customers.items():
    key = i[1]["State"]
    states.update({i[1]["CustomerId"] : abbrev_to_us_state[key] })

#fill dictionary rates with format {customer  ID, state tax rate}
for customer in states.items():
    cState = customer[1]
    for i in tax_rates.values():
        if( i["State"] == cState):
            rates.update({customer[0] :  (( float(i["Rate"][:-1]) / 100) + 1)})

#Fill keys of dictionary 'sales' with sales format (quantity, customerId) for each sale corresponding to each product
for i in range(12):
    for j in all_sales[i].items():
        key = j[1]["ProductId"]
        key2 = j[1]["CustomerId"]
        sales[key].append(tuple((j[1]["Quantity"], rates[key2])))

#iterate through sales of each item, add revenue for corresponding product to its index in annRevs
for product in sales.items():
    key = product[0]
    for i in product[1]:
            annRevs[key] += ( float(i[0]) * float(prices[key]) * float(i[1]) )

mostProduct = 0
mostRev = 0
for i in annRevs.items():
    if(i[1] > mostRev):
        mostRev = i[1]
        mostProduct = i[0]

print(f"The \"{mostProduct}\" had the most annual revenue with $ {mostRev:,.2f}.")
