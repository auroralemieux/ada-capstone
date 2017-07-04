from django.shortcuts import render

def home(request):
    return render(request, 'babynamebook/home.html', {})

def upload_tree(request):
    return render(request, 'babynamebook/upload_tree.html', {})
