import requests
from django.http import HttpResponse
from django.shortcuts import render
from fanatics_item.models import FanaticsItem
from fanatics_item.serializers import FanaticsItemSerializer
from rest_framework import generics


class FanaticsItemList(generics.ListCreateAPIView):
    queryset = FanaticsItem.objects.all()
    serializer_class = FanaticsItemSerializer


class FanaticsItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FanaticsItem.objects.all()
    serializer_class = FanaticsItemSerializer


def is_job_running(response, job):
    running_jobs = [job['id'] for job in response['running']]
    return job in running_jobs


def is_job_pending(response, job):
    pending_jobs = [job['id'] for job in response['pending']]
    return job in pending_jobs


def index(request):
    request_url = 'http://localhost:6800/listjobs.json?project=FanaticsSpider'
    response = requests.get(url=request_url)
    response = response.json()
    job = request.session.get('job_id')
    if is_job_running(response, job) or is_job_pending(response, job):
        return render(request, 'index.html', context={'spider_status': 'Stop Spider'})
    return render(request, 'index.html', context={'spider_status': 'Start Spider'})


def start_fanatics_spider(request):
    request_url = 'http://localhost:6800/listjobs.json?project=FanaticsSpider'
    response = requests.get(url=request_url)
    response = response.json()
    job = request.session.get('job_id')
    if is_job_running(response, job) or is_job_pending(response, job):
        return HttpResponse('Spider already running')

    request_url = 'http://127.0.0.1:6800/schedule.json'
    request_payload = {
        'project': 'FanaticsSpider',
        'spider': 'fanatics_spider',
        'setting': 'JOBDIR=crawls/fanatics_spider_crawls'
    }
    response = requests.post(url=request_url, data=request_payload)
    response = response.json()
    request.session['job_id'] = response['jobid']
    if response['status'] == 'ok':
        return HttpResponse('Spider started')
    return HttpResponse('Couldn\'t start spider')


def stop_fanatics_spider(request):
    request_url = 'http://127.0.0.1:6800/cancel.json'
    request_payload = {
        'project': 'FanaticsSpider',
        'job': request.session.get('job_id')
    }
    response = requests.post(url=request_url, data=request_payload)
    response = response.json()
    if response['status'] == 'ok':
        return HttpResponse('Spider stopped')
    return HttpResponse('Couldn\'t stop spider')
