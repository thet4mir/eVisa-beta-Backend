from django.shortcuts import render
from main.decorators import admin_required


@admin_required
def doc_all(request):
    return render(request, 'doc/all.html')
