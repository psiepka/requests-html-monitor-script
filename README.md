# Monitoring pracuj.pl script

Monitor web scraper that is grabing informations rendered. Script also send information about new offers on web page on type in consola emails.

<hr>

<h5>Quickstart</h5>
<br>
<b>Work in Python 3.7.0</b>
If you want to try funtionallity of script, go a head all what you have to do go to script directory and create .env file with variable: 

SMTP_PORT - port of your smtp mail 
SMTP_SERVER - smtp server of your mail 
EMAIL_ADRESS - your email adress which will send mails 
EMAIL_PASSWORD -  password to email which will send mails
 
 then open terminal in python cript directory and type
 >>> pip install -r requirements
 >>> python pracuj_pl.py
