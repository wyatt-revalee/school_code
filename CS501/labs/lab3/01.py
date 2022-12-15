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
customers = get_customers_unfixed()
# products = get_products()
# tax_rates = get_tax_rates()
# expenses = get_expenses()
# all_sales = get_monthly_sales()

emptyCount = 0
customerCount = 0
for i in customers:
    if(customers[i]["FirstName"] == ''):
        emptyCount += 1
    customerCount += 1

emptyPercentage = (emptyCount/customerCount) * 100
emptyPercentage = "{:.2f}".format(emptyPercentage)
print(f"{emptyPercentage} % missing \"FirstName\" fields.")
