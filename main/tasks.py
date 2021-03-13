# Create your tasks here
from .models import *

from celery.decorators import task

import requests
from bs4 import BeautifulSoup
import pandas as pd

@task
def get_hb_data():
    URL = 'https://www.legis.state.pa.us/cfdocs/legis/bi/BillIndx.cfm?sYear=2021&sIndex=0&bod=H'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('table', class_='DataTable')

    bill_links = []

    for a in results.find_all('a', href=True):
        bill_links.append(a['href'])

    for b in bill_links:
        new_house_bill = HouseBills()
        bill_url = 'https://www.legis.state.pa.us' + b
        bill_page = requests.get(bill_url)
        bill_soup = BeautifulSoup(bill_page.content, 'html.parser')

        bill_number = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('Bill')[1].strip()

        if HouseBills.objects.filter(bill_number=bill_number):
            pass
        else:
            new_house_bill.bill_number = int(bill_number)

            history_url = bill_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
            history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
            history_page = requests.get(history_url)
            history_soup = BeautifulSoup(history_page.content, 'html.parser')

            try:
                bill_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
                bill_date_introduced = bill_date_introduced.split()
                bill_date_introduced = ' '.join(bill_date_introduced[-3:])
                new_house_bill.date_introduced = bill_date_introduced
            except:
                bill_date_introduced = None

            bill_all_sponsors = history_soup.find('div', class_='BillInfo-PrimeSponsor').find('div', class_='BillInfo-Section-Data').find_all('a', href=True)
            all_sponsors_list = []
            for s in bill_all_sponsors:
                all_sponsors_list.append(s.text)
            all_sponsors_list = ', '.join(all_sponsors_list)
            new_house_bill.all_sponsors = all_sponsors_list

            bill_session = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('House')[0].strip()
            new_house_bill.session = bill_session

            bill_short_title = bill_soup.find('div', class_='BillInfo-ShortTitle').find('div', class_='BillInfo-Section-Data').text.strip()
            new_house_bill.short_title = bill_short_title

            bill_prime_sponsor = bill_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True).text.strip()
            new_house_bill.prime_sponsor = bill_prime_sponsor

            bill_prime_sponsor_url = bill_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True)['href'].strip()
            new_house_bill.prime_sponsor_url = bill_prime_sponsor_url

            try:
                bill_last_action = bill_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
                new_house_bill.last_action = bill_last_action
            except:
                bill_last_action = None

            try:
                bill_memo_title = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True).text.strip()
                new_house_bill.memo_title = bill_memo_title
            except:
                bill_memo_title = None

            try:
                bill_memo_url = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True)['href'].strip()
                new_house_bill.memo_url = bill_memo_url
            except:
                bill_memo_url = None

            try:
                bill_text = bill_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
                new_house_bill.bill_text = 'https://www.legis.state.pa.us' + bill_text
            except:
                bill_text = None

            new_house_bill.save()

@task
def get_hr_data():
    URL = 'https://www.legis.state.pa.us/cfdocs/legis/bi/BillIndx.cfm?sYear=2021&sIndex=0&bod=H'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_='DataTable')[1]

    resolution_links = []

    for a in results.find_all('a', href=True):
        resolution_links.append(a['href'])

    for r in resolution_links:
        new_house_res = HouseResolutions()
        res_url = 'https://www.legis.state.pa.us' + r
        res_page = requests.get(res_url)
        res_soup = BeautifulSoup(res_page.content, 'html.parser')
        
        res_number = res_soup.find('h2', class_='BillInfo-BillHeader').text.split('Resolution')[1].strip()

        if HouseResolutions.objects.filter(resolution_number=res_number):
            pass
        else:
            new_house_res.resolution_number = int(res_number)

            history_url = res_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
            history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
            history_page = requests.get(history_url)
            history_soup = BeautifulSoup(history_page.content, 'html.parser')

            try:
                res_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
                res_date_introduced = res_date_introduced.split()
                res_date_introduced = ' '.join(res_date_introduced[-3:])
                new_house_res.date_introduced = res_date_introduced
            except:
                res_date_introduced = None

            res_all_sponsors = history_soup.find('div', class_='BillInfo-PrimeSponsor').find('div', class_='BillInfo-Section-Data').find_all('a', href=True)
            all_sponsors_list = []
            for s in res_all_sponsors:
                all_sponsors_list.append(s.text)
            all_sponsors_list = ', '.join(all_sponsors_list)
            new_house_res.all_sponsors = all_sponsors_list

            res_session = res_soup.find('h2', class_='BillInfo-BillHeader').text.split('House')[0].strip()
            new_house_res.session = res_session

            res_short_title = res_soup.find('div', class_='BillInfo-ShortTitle').find('div', class_='BillInfo-Section-Data').text.strip()
            new_house_res.short_title = res_short_title

            res_prime_sponsor = res_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True).text.strip()
            new_house_res.prime_sponsor = res_prime_sponsor

            res_prime_sponsor_url = res_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True)['href'].strip()
            new_house_res.prime_sponsor_url = res_prime_sponsor_url

            try:
                res_last_action = res_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
                new_house_res.last_action = res_last_action
            except:
                res_last_action = None

            try:
                res_memo_title = res_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True).text.strip()
                new_house_res.memo_title = res_memo_title
            except:
                res_memo_title = None

            try:
                res_memo_url = res_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True)['href'].strip()
                new_house_res.memo_url = res_memo_url
            except:
                res_memo_url = None

            try:
                res_text = res_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
                new_house_res.resolution_text = 'https://www.legis.state.pa.us' + res_text
            except:
                res_text = None

            new_house_res.save()

@task
def get_sb_data():
    URL = 'https://www.legis.state.pa.us/cfdocs/legis/bi/BillIndx.cfm?sYear=2021&sIndex=0&bod=S'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('table', class_='DataTable')

    bill_links = []

    for a in results.find_all('a', href=True):
        bill_links.append(a['href'])

    for b in bill_links:
        new_senate_bill = SenateBills()
        bill_url = 'https://www.legis.state.pa.us' + b
        bill_page = requests.get(bill_url)
        bill_soup = BeautifulSoup(bill_page.content, 'html.parser')

        bill_number = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('Bill')[1].strip()

        if SenateBills.objects.filter(bill_number=bill_number):
            pass
        else:
            new_senate_bill.bill_number = int(bill_number)

            history_url = bill_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
            history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
            history_page = requests.get(history_url)
            history_soup = BeautifulSoup(history_page.content, 'html.parser')

            try:
                bill_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
                bill_date_introduced = bill_date_introduced.split()
                bill_date_introduced = ' '.join(bill_date_introduced[-3:])
                new_senate_bill.date_introduced = bill_date_introduced
            except:
                bill_date_introduced = None

            bill_all_sponsors = history_soup.find('div', class_='BillInfo-PrimeSponsor').find('div', class_='BillInfo-Section-Data').find_all('a', href=True)
            all_sponsors_list = []
            for s in bill_all_sponsors:
                all_sponsors_list.append(s.text)
            all_sponsors_list = ', '.join(all_sponsors_list)
            new_senate_bill.all_sponsors = all_sponsors_list

            bill_session = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('Senate')[0].strip()
            new_senate_bill.session = bill_session

            bill_short_title = bill_soup.find('div', class_='BillInfo-ShortTitle').find('div', class_='BillInfo-Section-Data').text.strip()
            new_senate_bill.short_title = bill_short_title

            bill_prime_sponsor = bill_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True).text.strip()
            new_senate_bill.prime_sponsor = bill_prime_sponsor

            bill_prime_sponsor_url = bill_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True)['href'].strip()
            new_senate_bill.prime_sponsor_url = bill_prime_sponsor_url

            try:
                bill_last_action = bill_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
                new_senate_bill.last_action = bill_last_action
            except:
                bill_last_action = None

            try:
                bill_memo_title = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True).text.strip()
                new_senate_bill.memo_title = bill_memo_title
            except:
                bill_memo_title = None

            try:
                bill_memo_url = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True)['href'].strip()
                new_senate_bill.memo_url = bill_memo_url
            except:
                bill_memo_url = None

            try:
                bill_text = bill_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
                new_senate_bill.bill_text = 'https://www.legis.state.pa.us' + bill_text
            except:
                bill_text = None

            new_senate_bill.save()

@task
def get_sr_data():
    URL = 'https://www.legis.state.pa.us/cfdocs/legis/bi/BillIndx.cfm?sYear=2021&sIndex=0&bod=S'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_='DataTable')[1]

    resolution_links = []

    for a in results.find_all('a', href=True):
        resolution_links.append(a['href'])

    for r in resolution_links:
        new_senate_res = SenateResolutions()
        res_url = 'https://www.legis.state.pa.us' + r
        res_page = requests.get(res_url)
        res_soup = BeautifulSoup(res_page.content, 'html.parser')

        res_number = res_soup.find('h2', class_='BillInfo-BillHeader').text.split('Resolution')[1].strip()

        if SenateResolutions.objects.filter(resolution_number=res_number):
            pass
        else:
            new_senate_res.resolution_number = int(res_number)

            history_url = res_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
            history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
            history_page = requests.get(history_url)
            history_soup = BeautifulSoup(history_page.content, 'html.parser')

            try:
                res_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
                res_date_introduced = res_date_introduced.split()
                res_date_introduced = ' '.join(res_date_introduced[-3:])
                new_senate_res.date_introduced = res_date_introduced
            except:
                res_date_introduced = None

            res_all_sponsors = history_soup.find('div', class_='BillInfo-PrimeSponsor').find('div', class_='BillInfo-Section-Data').find_all('a', href=True)
            all_sponsors_list = []
            for s in res_all_sponsors:
                all_sponsors_list.append(s.text)
            all_sponsors_list = ', '.join(all_sponsors_list)
            new_senate_res.all_sponsors = all_sponsors_list

            res_session = res_soup.find('h2', class_='BillInfo-BillHeader').text.split('Senate')[0].strip()
            new_senate_res.session = res_session

            res_short_title = res_soup.find('div', class_='BillInfo-ShortTitle').find('div', class_='BillInfo-Section-Data').text.strip()
            new_senate_res.short_title = res_short_title

            res_prime_sponsor = res_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True).text.strip()
            new_senate_res.prime_sponsor = res_prime_sponsor

            res_prime_sponsor_url = res_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True)['href'].strip()
            new_senate_res.prime_sponsor_url = res_prime_sponsor_url

            try:
                res_last_action = res_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
                new_senate_res.last_action = res_last_action
            except:
                res_last_action = None

            try:
                res_memo_title = res_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True).text.strip()
                new_senate_res.memo_title = res_memo_title
            except:
                res_memo_title = None

            try:
                res_memo_url = res_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True)['href'].strip()
                new_senate_res.memo_url = res_memo_url
            except:
                res_memo_url = None

            try:
                res_text = res_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
                new_senate_res.resolution_text = 'https://www.legis.state.pa.us' + res_text
            except:
                res_text = None

            new_senate_res.save()

@task
def celery_add(x, y):
    return x + y