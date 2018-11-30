'''
Created on Nov 29, 2018

@author: tlrausch33
'''
import credentials, sqlqueries
import json, time, threading,urllib2, urllib, datetime
import psycopg2, csv

def CreateSQLResultFile():
    
    try:
        dbconnection = psycopg2.connect( host=credentials.AWSDbCredentials['hostname'], user=credentials.AWSDbCredentials['username'], password=credentials.AWSDbCredentials['password'], dbname=credentials.AWSDbCredentials['database'], connect_timeout=1 )
        print "Connected to DB"

    except:
        print "Unable to connect to db"


    
    for strQueryName, strQuery in sqlqueries.sqlqueries.items():    
           
        
        cur = dbconnection.cursor()
        cur.execute(strQuery)
        dsresult = cur.fetchall()
        
        
        
        c = csv.writer(open("/home/tlrausch33/Documents/SQLQueries/"+strQueryName+".csv","wb"), lineterminator="\n")
        c.writerow([i[0] for i in cur.description])
        c.writerows(dsresult)  




