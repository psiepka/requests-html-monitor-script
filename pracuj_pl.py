import os
import smtplib
from requests_html import HTMLSession
from mail import senf_offer_on_mail


def collect_offers(search_name):
    """Function which collect existing offers on pracuj.pl/<search_name>/
    Arguments:
        search_name {str} -- searching keyword which scripts send get requests
    Returns:
        [list] -- list of offers existing on page.
    """

    print('Monitor script start collecting existing offers..')
    session = HTMLSession()
    r = session.get(f'https://www.pracuj.pl/praca/{search_name}')
    print(f'Starting monitor pracuj.pl with keyword {r.url}')
    title = r.html.find('.offer-details__title-link')
    list_of_titles = []
    pagination = r.html.find('ul.pagination_list > li.pagination_element-page')
    r.close()
    session.close()
    if pagination:
        max_pag = int(pagination[-1].text)
        for i in range(1, max_pag+1):
            new_session = HTMLSession()
            req = new_session.get(f'https://www.pracuj.pl/praca/{search_name}', params={'pn':i})
            wait = req.html.render(wait=0.2,  keep_page=True)
            new_session.close()
            req.close()
            result_item = req.html.find('li.results__list-container-item')
            for result in result_item:
                title = result.find('h3.offer-details__title', first=True).text
                company = result.find('span.offer-company__wrapper', first=True).text
                offer = f'{title} ({company})'
                list_of_titles.append(offer)
        print(f'Collected {len(list_of_titles)} offers.')
        return list_of_titles
    else:
        result_item = r.html.find('li.results__list-container-item')
        for result in result_item:
            title = result.find('h3.offer-details__title', first=True).text
            company = result.find('p.offer-company', first=True).text
            offer = f'{title} ({company})'
            list_of_titles.append(offer)
        print(f'Collected {len(list_of_titles)} offers.')
        return list_of_titles

def check_offers(list_offers, seach_name):
    """Function whch monitor page pracuj.pl/<search_name>/,
    function that check first element on page is in list_offers - if is not in list send mail with information about offfer.
    Arguments:
        list_offers {[list]} -- list which contain existing on page offers
        search_name {str} -- searching keyword which scripts send get requests
    Returns:
        [type] -- [description]
    """
    session = HTMLSession()
    r = session.get(f'https://www.pracuj.pl/praca/{search_name}')
    new_offers = {}
    pagination = r.html.find('ul.pagination_list > li.pagination_element-page')
    session.close()
    r.close()
    if pagination:
        max_pag = int(pagination[-1].text)
        for i in range(1, max_pag+1):
            new_session = HTMLSession()
            req = new_session.get(f'https://www.pracuj.pl/praca/{search_name}', params={'pn':i})
            wait = req.html.render(wait=0.2,  keep_page=True)
            new_session.close()
            req.close()
            result_item = req.html.find('li.results__list-container-item')
            for i, result in enumerate(result_item):
                title = result.find('h3.offer-details__title', first=True).text
                company = result.find('span.offer-company__wrapper', first=True).text
                offer = f'{title} ({company})'
                if offer not in list_offers:
                    title = result.find('h3.offer-details__title', first=True).text
                    company = result.find('span.offer-company__wrapper', first=True).text
                    link = r.html.find('a.offer-details__title-link', first=True).absolute_links.pop()
                    date = result.find('.offer-actions__date', first=True).text
                    offer = f'{title} ({company})'
                    description = {
                        'title': title,
                        'company': company,
                        'date': date,
                    }
                    new_offers[i] = description
                    list_offers.append(offer)
                else:
                    return new_offers
        len(list_offers)
        return new_offers
    else:
        result_item = r.html.find('li.results__list-container-item')
        for result in result_item:
            if result not in list_offers:
                title = result.find('h3.offer-details__title', first=True).text
                company = result.find('p.offer-company', first=True).text
                offer = f'{title} ({company})'
                description = {
                        'title': title,
                        'company': company,
                        'date': date,
                    }
                new_offers[i] = description
                list_of_titles.append(offer)
            else:
                return new_offers
        return new_offers

# app command to start

print('Welcome to monitor pracuj.pl script')

search_name = input('Please type search keyword :\n-')
if not search_name:
    search_name = input('Please type search keyword :\n-')

receiver_emails = input('Please type reciver mail :\n-')
if not receiver_emails:
    receiver_emails = input('Please type reciver mail :\n-')

print(f'\nNew offers will be send to {receiver_emails} ')

list_of_titles = collect_offers(search_name)

numbers_of_new_offers = 0
print(f'Scirpt start to monitor new offers on pracuj.pl with keyword {search_name}')
while True:
    try:
        new_offers = check_offers(list_of_titles, search_name)
        if new_offers:
            numbers_of_new_offers += len(new_offers)
            senf_offer_on_mail(search_name, receiver_emails, new_offers)
            new_offers = None
            print(f'Since start added {numbers_of_new_offers} offers! :)')
            print('If you want to monitor website, dont turn off script... ;)')
    except KeyboardInterrupt:
        raise "\n Turning off the dummy script"
        break
