import psycopg2
import datetime 
import os
from pathlib import Path
def current_time():

	current_time = datetime.datetime.now() 
	list = []
	list.extend((str(current_time.year),str(current_time.month),str(current_time.day)))
	day = "-".join(list)
	list = []
	list.extend((str(current_time.hour),str(current_time.minute),str(current_time.second)))
	time = ":".join(list)
	return day,time



os.system("./server_download.sh")
os.system("gcc -o create_table create_table.c -I/usr/include/postgresql -lpq -std=c99")
os.system("./create_table")
conn = psycopg2.connect(database = "fpdb", user = "postgres", password = "power12515@", host = "127.0.0.1", port = "5432")
cur = conn.cursor()
day,time = current_time()

directory = "Query_Result/" + day + "/" + time
Path(directory).mkdir(parents = True,exist_ok = True)

cur.execute('''	SELECT DISTINCT ON (province) province,product_id,SUM(has_sold) AS sales,(SUM(quantity*price))/SUM(quantity) AS average_price
				FROM fp_stores_data
				GROUP BY province,product_id
				ORDER BY province,SUM(has_sold) DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "most_product_sold_in_every_province.csv"
f= open(file_path,"w+")
f.write("province,product_id,total_sales,price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "\n")

cur.execute('''	SELECT DISTINCT ON (market_id) market_id,product_id,SUM(has_sold) AS sales,(SUM(quantity*price))/SUM(quantity) AS average_price
				FROM fp_stores_data
				GROUP BY market_id,product_id
				ORDER BY market_id,SUM(has_sold) DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "most_product_sold_in_every_market.csv"
f= open(file_path,"w+")
f.write("market_id,product_id,total_sales,price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "\n")

cur.execute('''	SELECT market_id,SUM(has_sold*price) AS sales_price
				FROM fp_stores_data
				GROUP BY market_id
				ORDER BY sales_price DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "total_sales_price_in_every_market.csv"
f= open(file_path,"w+")
f.write("market_id,total_sales_price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "\n")

cur.execute('''SELECT province,SUM(has_sold*price) AS sales_price
				FROM fp_stores_data
				GROUP BY province
				ORDER BY sales_price DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "total_sales_price_in_every_province.csv"
f= open(file_path,"w+")
f.write("province,total_sales_price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "\n")

cur.execute('''SELECT market_id,total_sales_price
				FROM fp_store_aggregation
				ORDER BY total_sales_price DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "total_sales_price_in_every_market_in_last_half_hour.csv"
f= open(file_path,"w+")
f.write("market_id,total_sales_price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "\n")

cur.execute('''SELECT city,SUM(has_sold*price) AS total_sales_price
				FROM fp_stores_data
				GROUP BY city
				ORDER BY total_sales_price DESC;''')
file_path = "Query_Result/" + day + "/" + time + "/" + "total_sales_price_in_every_city.csv" 
f= open(file_path,"w+")
f.write("city,total_sales_price\n")
rows = cur.fetchall()
for row in rows:
	f.write(str(row[0]) + "," + str(row[1]) + "\n")
cur.close()

conn.commit()
conn.close()

