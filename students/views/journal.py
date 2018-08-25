# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def journal_list(request):

    return render(request, 'students/journal.html', {})
