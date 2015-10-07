# coding: utf-8

from django.shortcuts import render_to_response, render


# TODO Вынести это из корня проекта
def time(request):
    return render(request, 'repo_list.html')
