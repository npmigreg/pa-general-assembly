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
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import gensim
import string
from gensim import corpora
from gensim.corpora.dictionary import Dictionary

# Create your views here.
def home(request):
    s_bills = SenateBills.objects.count()
    s_res = SenateResolutions.objects.count()

    context = {
        's_bills':s_bills,
        's_res':s_res,
    }
    return render(request, 'main/index.html', context)

class SenateBillsList(ListView):
    model = SenateBills
    paginate_by = 10
    ordering = ['-bill_number']

class SenateResolutionsList(ListView):
    model = SenateResolutions
    paginate_by = 10
    ordering = ['-resolution_number']

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

@login_required
def get_sr_data(request):
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
        new_senate_res.resolution_number = int(res_number)

        history_url = res_soup.find('div', class_='BillInfo-NavLinks2').find('a', href=True)['href'].strip()
        history_url = 'https://www.legis.state.pa.us/cfdocs/billinfo/' + history_url
        history_page = requests.get(history_url)
        history_soup = BeautifulSoup(history_page.content, 'html.parser')

        res_date_introduced = history_soup.find('div', class_='BillInfo-Actions').find('div', class_='BillInfo-Section-Data').find_all('td')[2].text.strip()
        res_date_introduced = res_date_introduced.split()
        res_date_introduced = ' '.join(res_date_introduced[-3:])
        new_senate_res.date_introduced = res_date_introduced

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

        res_last_action = res_soup.find('div', class_='BillInfo-LastAction').find('div', class_='BillInfo-Section-Data').text.strip()
        new_senate_res.last_action = res_last_action

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

        res_text = res_soup.find('div', class_='BillInfo-PN').find('table', class_='BillInfo-PNTable').find_all('td')[1].find('a', href=True)['href'].strip()
        new_senate_res.resolution_text = 'https://www.legis.state.pa.us' + res_text

        new_senate_res.save()

    return redirect("/")

class RenderSBData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        s_bills = SenateBills.objects.all().values()
        sb_df = pd.DataFrame(list(s_bills))

        prime_sponsor = sb_df['prime_sponsor'].value_counts()
        prime_labels = list(prime_sponsor.index)
        prime_labels_new = []
        for l in prime_labels:
            prime_labels_new.append(l.strip('Senator '))
        prime_data = list(prime_sponsor)

        all_sponsors = sb_df['all_sponsors'].str.split(',', expand=True).stack()
        all_sponsors = all_sponsors.str.strip()
        all_sponsors = all_sponsors.value_counts()
        all_sponsors_labels = list(all_sponsors.index)
        all_sponsors_data = list(all_sponsors)

        data = {
            "prime_labels":prime_labels_new,
            "prime_data":prime_data,
            "all_sponsors_labels":all_sponsors_labels,
            "all_sponsors_data":all_sponsors_data,
        }

        return Response(data)

class RenderSRData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        s_res = SenateResolutions.objects.all().values()
        sr_df = pd.DataFrame(list(s_res))

        prime_sponsor = sr_df['prime_sponsor'].value_counts()
        prime_labels = list(prime_sponsor.index)
        prime_labels_new = []
        for l in prime_labels:
            prime_labels_new.append(l.strip('Senator '))
        prime_data = list(prime_sponsor)

        all_sponsors = sr_df['all_sponsors'].str.split(',', expand=True).stack()
        all_sponsors = all_sponsors.str.strip()
        all_sponsors = all_sponsors.value_counts()
        all_sponsors_labels = list(all_sponsors.index)
        all_sponsors_data = list(all_sponsors)

        data = {
            "prime_labels":prime_labels_new,
            "prime_data":prime_data,
            "all_sponsors_labels":all_sponsors_labels,
            "all_sponsors_data":all_sponsors_data,
        }

        return Response(data)

def sb_dashboard(request):
    return render(request, 'main/sb-dashboard.html')

def sr_dashboard(request):
    return render(request, 'main/sr-dashboard.html')

def sr_text_analysis(request):
    s_res = SenateResolutions.objects.all().values()
    sr_df = pd.DataFrame(list(s_res))

    short_titles = list(sr_df['short_title'])

    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(document):
        stopwordremoval = " ".join([i for i in document.lower().split() if i not in stop_words])
        punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
        return normalized

    final_doc = [clean(document).split() for document in short_titles]
    final_doc_exclusion = ['resolution', 'senate', 'session', 'pennsylvania', 'general', 'commonwealth', 'adopting', 'declaring', 'rule', '2020', '2021', 'january',
                           'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'president', 'vice', 'day',
                           'week', 'month', 'year', 'state', 'bill', 'recognizing', 'designating', '205th', '206th']

    number_range = list(range(0,500))
    number_range = map(str, number_range)
    number_list = list(number_range)
    final_doc_exclusion.extend(number_list)

    final_doc = [[i for i in doc if i not in final_doc_exclusion] for doc in final_doc]

    dictionary = corpora.Dictionary(final_doc)

    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]

    Lda_object = gensim.models.ldamodel.LdaModel

    lda_model_1 = Lda_object(DT_matrix, num_topics=8, id2word = dictionary)
    model_results = lda_model_1.print_topics(num_topics=8, num_words=3)

    context = {
        'short_titles':model_results,
    }

    return render(request, 'main/sr-text-analysis.html', context)