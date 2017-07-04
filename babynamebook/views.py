from django.shortcuts import render
from .forms import BookForm

def home(request):
    return render(request, 'babynamebook/home.html', {})

def upload_tree(request):
    form = BookForm()
    return render(request, 'babynamebook/upload_tree.html', {'form': form})
