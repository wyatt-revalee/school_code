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
# customers = get_customers()
products = get_products()
# tax_rates = get_tax_rates()
# expenses = get_expenses()
all_sales = get_monthly_sales()

grossProductPrices = {}
productQuantities = {}

#Make two dicts, one being {product : price-cost} and the other {product : []}
# with [] being an empty list to be filled with tuples of sales, in the format (month of sale, quantity sold)
for i in range(len(products)):
    grossProductPrices.update({products[i]["ProductId"] : float(products[i]["Price"]) - float(products[i]["Cost"])})
    productQuantities.update({products[i]["ProductId"]: []})

#Fill product quantities 'value' list with tuples of sales in format (month, quantity)
for i in range(12):
    for j in all_sales[i].items():
        for k in productQuantities:
            if(j[1]["ProductId"] == k):
                key = j[1]["ProductId"]
                productQuantities[key].append(tuple((i, int(j[1]["Quantity"]))))

#Initialize list of monthly profits, with indexes matching up to months (0 = January)
monthyProfit = []
for i in range(12):
    monthyProfit.append(0)

#Loop through all sales of each item, keep adding the gross product price (price-cost) * the quantity to the corresponding monthly gross profit
for i in productQuantities.items():
    for j in grossProductPrices.items():
        if(i[0] == j[0]):
            for k in i[1]:
                key = k[0]
                monthyProfit[key] += k[1] * j[1]


maxRev = 0
maxMonth = 0
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


for i in range(len(monthyProfit)):
    if(monthyProfit[i] > maxRev):
        maxRev = monthyProfit[i]
        maxMonth = months[i]


print(f"{maxMonth} had the most gross profit with $ {maxRev:,.2f}.")
