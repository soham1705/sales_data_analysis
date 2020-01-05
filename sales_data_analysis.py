#!/usr/bin/env python
# coding: utf-8

columns = []
data = [[],[],[],[],[]]

# for ordering months correctly while displaying 
month_name = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

def insert_row(data,l):
    for i in range(len(l)):
        data[i].append(l[i])
    return data

def month_from_date(date):
    return month_name[date.split('-')[1]]

def year_from_date(date):
    return date.split('-')[0]

with open('sales-data.txt','r') as f:
    columns = f.readline().strip('\n').split(',')
    for row in f.readlines():
        data_row = (row.strip('\n').split(','))
        data = insert_row(data, data_row)

dataset = dict(zip(columns,data))

rowNum = len(dataset['Date'])

# Converting to numeric

dataset['Unit Price'] = [float(item) for item in dataset['Unit Price']]
dataset['Quantity'] = [int(item) for item in dataset['Quantity']]
dataset['Total Price'] = [float(item) for item in dataset['Total Price']]

print()

# 1. Total sales of store

print("Total sales of store: "+str(sum(dataset['Total Price'])))
print()

# 2. Month wise sales totals

# adding a new column to the dataset called Month
dataset['Month'] = [month_from_date(date) for date in dataset['Date']]
dataset['Year'] = [year_from_date(date) for date in dataset['Date']]

dataset['month_year'] = []

for row in range(rowNum):

	dataset['month_year'].append(dataset['Month'][row] + ' ' + dataset['Year'][row])

month_list = list(set(dataset['month_year']))

total_sales_monthly = {month:0 for month in month_list}

for row in range(rowNum):
    month = dataset['month_year'][row]
    total_sales = dataset['Total Price'][row]
    total_sales_monthly[month]+=total_sales

for month in month_list:
    # month = month_name[month_numeric]
    print(("Total sales for {} : {}").format(month,total_sales_monthly[month]))

print()

# 3. Most popular item (most quantity sold) in each month

monthly_item_sales = {month:{} for month in month_list}

for row in range(rowNum):
    
    month = dataset['month_year'][row]
    item = dataset['SKU'][row]
    qty = dataset['Quantity'][row]

    if item not in monthly_item_sales[month].keys():
        monthly_item_sales[month][item] = 0

    monthly_item_sales[month][item] += qty


for month in month_list:
    #month = month_name[month_numeric]
    most_popular_item = max(monthly_item_sales[month], key = monthly_item_sales[month].get)
    print("Most popular item of {} : {}".format(month, most_popular_item))

print()

# 4. Items generating most revenue in each month.

monthly_item_revenues = {month:{} for month in month_list}


for row in range(rowNum):
    
    month = dataset['month_year'][row]
    item = dataset['SKU'][row]
    revenue = dataset['Total Price'][row]

    if item not in monthly_item_revenues[month].keys():
        monthly_item_revenues[month][item] = 0

    monthly_item_revenues[month][item] += revenue

for month in month_list:
    # month = month_name[month_numeric]
    most_revenue_item = max(monthly_item_revenues[month], key = monthly_item_revenues[month].get)
    print("Item generating most revenue in {} : {}".format(month, most_revenue_item))

print()

#5. For the most popular item, find the min, max and average number of orders each month.

total_item_sales = {item:0 for item in list(set(dataset['SKU']))}

# print(total_item_sales)

for row in range(rowNum):
    
    item = dataset['SKU'][row]
    qty = dataset['Quantity'][row]

    total_item_sales[item] += qty

# print(total_item_sales)

most_popular_item = max(total_item_sales, key = total_item_sales.get)
most_popular_item_sales_monthly = {month:[] for month in month_list}

# print(most_popular_item_sales_monthly)

for row in range(rowNum):
    
    month = dataset['month_year'][row]
    item = dataset['SKU'][row]
    qty = dataset['Quantity'][row]
    
    if item == most_popular_item:
        most_popular_item_sales_monthly[month].append(qty)

# print(most_popular_item_sales_monthly)

print("Most popular item: "+most_popular_item)

for month in month_list:

    # month = month_name[month_numeric]
    monthly_sales = most_popular_item_sales_monthly[month]
    print(month,monthly_sales)
    
    minimum = min(monthly_sales)
    maximum = max(monthly_sales)
    average = round(sum(monthly_sales)/len(monthly_sales),2)

    print("\n{} sales in {}:".format(most_popular_item,month))
    print("Minimum number of orders: "+str(minimum))
    print("Maximum number of orders: "+str(maximum))
    print("Average number of orders: "+str(average))

print()