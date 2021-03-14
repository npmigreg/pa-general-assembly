# Django imports
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import *

# Django Rest Framework imports for the API endpoints used in analysis pages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# NLTK and other imports for text analysis
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import gensim
import string
from gensim import corpora
from gensim.corpora.dictionary import Dictionary

def home(request):
    h_bills = HouseBills.objects.count()
    h_res = HouseResolutions.objects.count()
    s_bills = SenateBills.objects.count()
    s_res = SenateResolutions.objects.count()

    context = {
        'h_bills':h_bills,
        'h_res':h_res,
        's_bills':s_bills,
        's_res':s_res,
    }
    return render(request, 'main/index.html', context)

class HouseBillsList(ListView):
    model = HouseBills
    paginate_by = 10
    ordering = ['-bill_number']

class HouseResolutionsList(ListView):
    model = HouseResolutions
    paginate_by = 10
    ordering = ['-resolution_number']

class SenateBillsList(ListView):
    model = SenateBills
    paginate_by = 10
    ordering = ['-bill_number']

class SenateResolutionsList(ListView):
    model = SenateResolutions
    paginate_by = 10
    ordering = ['-resolution_number']

class RenderHBData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        h_bills = HouseBills.objects.all().values()
        hb_df = pd.DataFrame(list(h_bills))

        prime_sponsor = hb_df['prime_sponsor'].value_counts()
        prime_labels = list(prime_sponsor.index)
        prime_labels_new = []
        for l in prime_labels:
            prime_labels_new.append(l.strip('Representative '))
        prime_data = list(prime_sponsor)

        all_sponsors = hb_df['all_sponsors'].str.split(',', expand=True).stack()
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

class RenderHRData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        h_res = HouseResolutions.objects.all().values()
        hr_df = pd.DataFrame(list(h_res))

        prime_sponsor = hr_df['prime_sponsor'].value_counts()
        prime_labels = list(prime_sponsor.index)
        prime_labels_new = []
        for l in prime_labels:
            prime_labels_new.append(l.strip('Representative '))
        prime_data = list(prime_sponsor)

        all_sponsors = hr_df['all_sponsors'].str.split(',', expand=True).stack()
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

def hb_dashboard(request):
    return render(request, 'main/hb-dashboard.html')

def hr_dashboard(request):
    return render(request, 'main/hr-dashboard.html')

def sb_dashboard(request):
    return render(request, 'main/sb-dashboard.html')

def sr_dashboard(request):
    return render(request, 'main/sr-dashboard.html')

def hb_text_analysis(request):
    h_bill = HouseBills.objects.all().values()
    hb_df = pd.DataFrame(list(h_bill))

    short_titles = list(hb_df['short_title'])

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
                           'week', 'month', 'year', 'state', 'bill', 'recognizing', 'designating', '205th', '206th', 'act', 'providing', 'amending', 'title', 'statute',
                           'house', 'known', 'consolidated']

    number_range = list(range(0,500))
    number_range = map(str, number_range)
    number_list = list(number_range)
    final_doc_exclusion.extend(number_list)

    century_range = list(range(1899,2022))
    century_range = map(str, century_range)
    century_list = list(century_range)
    final_doc_exclusion.extend(century_list)

    final_doc = [[i for i in doc if i not in final_doc_exclusion] for doc in final_doc]

    dictionary = corpora.Dictionary(final_doc)

    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]

    Lda_object = gensim.models.ldamodel.LdaModel

    lda_model_1 = Lda_object(DT_matrix, num_topics=10, id2word = dictionary)
    model_results = lda_model_1.print_topics(num_topics=10, num_words=3)

    context = {
        'model_results':model_results,
    }

    return render(request, 'main/hb-text-analysis.html', context)   

def hr_text_analysis(request):
    h_res = HouseResolutions.objects.all().values()
    hr_df = pd.DataFrame(list(h_res))

    short_titles = list(hr_df['short_title'])

    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(document):
        stopwordremoval = " ".join([i for i in document.lower().split() if i not in stop_words])
        punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
        return normalized

    final_doc = [clean(document).split() for document in short_titles]
    final_doc_exclusion = ['resolution', 'house', 'senate', 'session', 'pennsylvania', 'general', 'commonwealth', 'adopting', 'declaring', 'rule', '2020', '2021', 'january',
                           'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'president', 'vice', 'day',
                           'week', 'month', 'year', 'state', 'bill', 'recognizing', 'designating', '205th', '206th', 'urging', 'providing', 'amending']

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
        'model_results':model_results,
    }

    return render(request, 'main/hr-text-analysis.html', context)

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
        'model_results':model_results,
    }

    return render(request, 'main/sr-text-analysis.html', context)

def sb_text_analysis(request):
    s_bill = SenateBills.objects.all().values()
    sb_df = pd.DataFrame(list(s_bill))

    short_titles = list(sb_df['short_title'])

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
                           'week', 'month', 'year', 'state', 'bill', 'recognizing', 'designating', '205th', '206th', 'act', 'providing', 'amending', 'title', 'statute']

    number_range = list(range(0,500))
    number_range = map(str, number_range)
    number_list = list(number_range)
    final_doc_exclusion.extend(number_list)

    final_doc = [[i for i in doc if i not in final_doc_exclusion] for doc in final_doc]

    dictionary = corpora.Dictionary(final_doc)

    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]

    Lda_object = gensim.models.ldamodel.LdaModel

    lda_model_1 = Lda_object(DT_matrix, num_topics=10, id2word = dictionary)
    model_results = lda_model_1.print_topics(num_topics=10, num_words=3)

    context = {
        'model_results':model_results,
    }

    return render(request, 'main/sb-text-analysis.html', context)