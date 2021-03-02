from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create your views here.
def home(request):
    s_bills = SenateBills.objects.count()

    context = {
        's_bills':s_bills,
    }
    return render(request, 'main/index.html', context)

class SenateBillsList(ListView):
    model = SenateBills
    paginate_by = 10
    ordering = ['-bill_number']

@login_required
def get_sb_data(request):
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
        new_senate_bill.bill_number = int(bill_number)

        history_url = bill_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
        history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
        history_page = requests.get(history_url)
        history_soup = BeautifulSoup(history_page.content, 'html.parser')

        bill_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
        bill_date_introduced = bill_date_introduced.split()
        bill_date_introduced = ' '.join(bill_date_introduced[-3:])
        new_senate_bill.date_introduced = bill_date_introduced

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

        bill_last_action = bill_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
        new_senate_bill.last_action = bill_last_action

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

        bill_text = bill_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
        new_senate_bill.bill_text = 'https://www.legis.state.pa.us' + bill_text

        new_senate_bill.save()

    return redirect("/")

class RenderSBData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        s_bills = SenateBills.objects.all().values()
        sb_df = pd.DataFrame(list(s_bills))

        prime_sponsor = sb_df['prime_sponsor'].value_counts()[:10]
        sb_prime_labels = list(prime_sponsor.index)
        sb_prime_data = list(prime_sponsor)

        data = {
            "sb_prime_labels":sb_prime_labels,
            "sb_prime_data":sb_prime_data,
        }

        return Response(data)

def sb_analysis(request):
    return render(request, 'main/sb_analysis.html')

def sb_dashboard(request):
    return render(request, 'main/sb-dashboard.html')