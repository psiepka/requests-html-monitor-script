import os
import smtplib, ssl
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


load_dotenv()

def senf_offer_on_mail(search_name, receiver_emails, dictonary_with_offers):
    port = int(os.environ.get('SMTP_PORT'))
    smtp_server = os.environ.get('SMTP_SERVER')
    sender_email = os.environ.get('EMAIL_ADRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Nowe offerty pracy w '{search_name}' na stronie pracuj.pl !"
    message["From"] = sender_email

    offers_num = len(dictonary_with_offers)
    text = f"Pojawiło się {offers_num} ofert na stronie  https://www.pracuj.pl/praca/{search_name}!!!"
    html_start = f"""
    <html>
    <body>
        <p>Pojawiło się <b>{offers_num}</b> ofert na stronie <a href="https://www.pracuj.pl/praca/{search_name}">pracuj.pl</a></p>!!!
        <br>
        <br>
        Lista ofert :
    """
    html_list = ''
    for key, offer in dictonary_with_offers.items():
        html_list += f"""
            <br>
            <a href="{offer.get('link')}" style='text-decoration: none; color: black'>
                <div style="border-style: ridge; margin:10px">
                    <h4 style="margin:2px">
                        {offer.get('title')}
                    </h4>
                    <small style="margin:2px">
                        {offer.get('company')}
                    </small>
                    <p style="margin:2px">
                        {offer.get('date')}
                    </p>
                </div>
            </a>
            """
    html_end = f"""
        </small>
            </u>
                Wysłano za pomocą skryptu napisanego w <b>Pythonie</b>
            </u>
        </small>
    </body>
    </html>
    """
    html = html_start + html_list + html_end
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    for receiver_email in receiver_emails.split():
        message["To"] = receiver_email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

# d = {
#     'title': 'Junior ściemniacz M E G A developer',
#     'company': 'Firma Nowy KRZAK',
#     'date': '17 marca 1995',
#     'link':'google.com',
# }

# d_list1 =  {}
# for i in range(3):
#     d_list1[i] = d


# d_list2 =  {}
# for i in range(2):
#     d_list2[i] = d


# d_list3 =  {}
# for i in range(1):
#     d_list3[i] = d

# t1 = time.perf_counter()

# print()
# print('0')
# print()
# senf_offer_on_mail('python', "patrykeo001@gmail.com", d_list1)
# print()
# print('1')
# print()
# senf_offer_on_mail('python', "patrykeo001@gmail.com", d_list2)
# print()
# print('2')
# print()
# senf_offer_on_mail('python', "patrykeo001@gmail.com", d_list3)
# print()
# print('3')
# print()
# t2 = time.perf_counter()

# print(f'zajeło to {t2-t1} sec')