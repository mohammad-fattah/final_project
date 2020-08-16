#include <stdio.h>
#include <stdlib.h>
#include <postgresql/libpq-fe.h>
#include <string.h>
#include <dirent.h>
#include <malloc.h>

void do_exit(PGconn *conn, PGresult *res) {
    
    fprintf(stderr, "%s\n", PQerrorMessage(conn));    

    PQclear(res);
    PQfinish(conn);    
    
    exit(1);
}

int main(int argc, char **argv) {
   
	char *array [100];
    
    PGconn *conn = PQconnectdb("user=postgres password=power12515@ dbname=fpdb");

	if (PQstatus(conn) == CONNECTION_BAD) {
        
        fprintf(stderr, "Connection to database failed: %s\n",
        PQerrorMessage(conn));
            
        PQfinish(conn);
        exit(1);
    }
    
 	PGresult *res = PQexec(conn, "CREATE TABLE IF NOT EXISTS fp_stores_data(Id SERIAL PRIMARY KEY," \
        "time NUMERIC, province VARCHAR,city VARCHAR, market_id INT," \
		"product_id INT, price INT,quantity INT,has_sold INT)");
	if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        do_exit(conn, res); 
    }
    
    PQclear(res);

 	res = PQexec(conn, "CREATE TEMP TABLE temp_table(Id SERIAL PRIMARY KEY," \
        "time NUMERIC, province VARCHAR,city VARCHAR, market_id INT," \
		"product_id INT, price INT,quantity INT,has_sold INT)");
	if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        do_exit(conn, res); 
    }
    
    PQclear(res);

    DIR *d;
    struct dirent *dir;
    d = opendir("/tmp/final_project");
    if (d)
    {
        while ((dir = readdir(d)) != NULL)
        {
        char path[200] = "COPY fp_stores_data(time,province,city,market_id,product_id,price,quantity,has_sold) FROM '/tmp/final_project/";
		if(strcmp(dir->d_name,".") == 0 || strcmp(dir->d_name,"..") == 0)
			continue;
		strcat(path,dir->d_name);
		strcat(path,"' DELIMITER ',' CSV");
		res = PQexec(conn, path);
		if (PQresultStatus(res) != PGRES_COMMAND_OK) {
		    do_exit(conn, res); 
		}
		
		PQclear(res);
		char temp_path[200] = "COPY temp_table(time,province,city,market_id,product_id,price,quantity,has_sold) FROM '/tmp/final_project/";
		strcat(temp_path,dir->d_name);
		strcat(temp_path,"' DELIMITER ',' CSV");
		res = PQexec(conn, temp_path);
		if (PQresultStatus(res) != PGRES_COMMAND_OK) {
		    do_exit(conn, res); 
		}
		
		PQclear(res);

        }
        closedir(d);
    }
	res = PQexec(conn, "DROP TABLE IF EXISTS fp_city_aggregation");
	PQclear(res);
	res = PQexec(conn, "SELECT time, city, SUM(quantity) the_whole_product,SUM(has_sold) total_sales,"\
			   "(SUM(quantity*price))/SUM(quantity) AS average_price "\
			   "INTO TABLE fp_city_aggregation "\
			   "FROM temp_table "\
			   "GROUP BY time,city ");
	PQclear(res);

	res = PQexec(conn, "DROP TABLE IF EXISTS fp_store_aggregation");
	PQclear(res);
	res = PQexec(conn, "SELECT market_id,SUM(has_sold) total_sales,"\
			   "SUM(has_sold*price) AS total_sales_price "\
			   "INTO TABLE fp_store_aggregation "\
			   "FROM temp_table "\
			   "GROUP BY market_id ");
	PQclear(res);

	PQfinish(conn);
    return 0;
}





