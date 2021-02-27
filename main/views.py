from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .models import *

# Create your views here.
def home(request):
    return render(request, 'main/index.html')

def get_data(request):

    URL = 'https://www.legis.state.pa.us/cfdocs/legis/bi/BillIndx.cfm?sYear=2021&sIndex=0&bod=S'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('table', class_='DataTable')

    bill_links = []

    for a in results.find_all('a', href=True):
        bill_links.append(a['href'])

    for b in bill_links[:2]:
        new_senate_bill = SenateBills()
        bill_url = 'https://www.legis.state.pa.us' + b
        bill_page = requests.get(bill_url)
        bill_soup = BeautifulSoup(bill_page.content, 'html.parser')

        bill_number = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('Bill')[1].strip()
        new_senate_bill.bill_number = int(bill_number)

        bill_session = bill_soup.find('h2', class_='BillInfo-BillHeader').text.split('Senate')[0].strip()
        new_senate_bill.session = bill_session

        bill_short_title = bill_soup.find('div', class_='BillInfo-ShortTitle').find('div', class_='BillInfo-Section-Data').text.strip()
        new_senate_bill.short_title = bill_short_title

        bill_prime_sponsor = bill_soup.find('div', class_='BillInfo-PrimeSponsor').find('a', href=True).text.strip()
        new_senate_bill.prime_sponsor = bill_prime_sponsor

        bill_last_action = bill_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
        new_senate_bill.last_action = bill_last_action

        bill_memo_title = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True).text.strip()
        new_senate_bill.memo_title = bill_memo_title

        bill_memo_url = bill_soup.find('div', class_='BillInfo-CosponMemo').find('a', href=True)['href'].strip()
        new_senate_bill.memo_url = bill_memo_url

        bill_text = bill_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
        new_senate_bill.bill_text = 'https://www.legis.state.pa.us' + bill_text

        new_senate_bill.save()

    return redirect("/")