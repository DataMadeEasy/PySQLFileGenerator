'''
Created on Nov 29, 2018

@author: tlrausch33
'''
import credentials, sqlqueries, emailconfig
import json, time, threading,urllib2, urllib, datetime, psycopg2, csv, smtplib, os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import glob


def CreateSQLResultFile():
    
    try:
        dbconnection = psycopg2.connect( host=credentials.AWSDbCredentials['hostname'], user=credentials.AWSDbCredentials['username'], password=credentials.AWSDbCredentials['password'], dbname=credentials.AWSDbCredentials['database'], connect_timeout=1 )
        print "Connected to DB"

    except:
        print "Unable to connect to db"
        print credentials.AWSDbCredentials['hostname'] + credentials.AWSDbCredentials['username']+ credentials.AWSDbCredentials['password'] + credentials.AWSDbCredentials['database']
    
    for strQueryName, strQuery in sqlqueries.sqlqueries.items():    
           
        
        cur = dbconnection.cursor()
        cur.execute(strQuery)
        dsresult = cur.fetchall()
        
        
        
        c = csv.writer(open("/home/tlrausch33/Documents/SQLQueries/"+strQueryName+".csv","wb"), lineterminator="\n")
        c.writerow([i[0] for i in cur.description])
        c.writerows(dsresult)  



def EmailFiles():
    
    
 

    ##Pull Email Credenitals
    user= credentials.EmailCredentials['user']
    password = credentials.EmailCredentials['password']
    
    
    #Pull Email configuration
    smtpserver = smtplib.SMTP(emailconfig.smtpinfo['server'],emailconfig.smtpinfo['port'])
    
    
    
    filelocation = emailconfig.attachmentlocation
    filelist = glob.glob(filelocation + '*')
    print filelist
  
    strdistributionlist =';'.join(emailconfig.distributionlist)
    
    
    msg = MIMEMultipart()
    msg['From'] = credentials.EmailCredentials['user']
    msg['To'] = strdistributionlist 
    msg['Subject'] = emailconfig.emailtemplate['subject']

    message = emailconfig.emailtemplate['message']
    msg.attach(MIMEText(message, 'plain'))
    
    for strfile in filelist:
        filename = os.path.basename(strfile)
        attachment = open(strfile, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
        msg.attach(part)

    
    
    
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(user, password)
    
    #header = 'To:' + sendto + '\n' + 'From: ' + user + '\n' + 'Subject:' + emailconfig.emailtemplate['subject'] + ' \n' + 'MIME-Version: 1.0' +' \n' + 'Content-Type: multipart/mixed; boundary=%s' + ' \n' + '--%s' % (marker, marker)
    #print header
    #msgbody = header + '\n' + emailconfig.emailtemplate['message']
    #smtpserver.sendmail(user, sendto, msgbody)
    
    
    text = msg.as_string()
    smtpserver.sendmail(user, emailconfig.distributionlist, text)
    smtpserver.quit()
    
    
    
    
    print 'done!'
    smtpserver.close()