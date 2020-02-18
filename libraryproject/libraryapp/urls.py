from django.urls import path
from .views import *

app_name = "libraryapp"

urlpatterns = [
    path('', book_list, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', librarian_list, name='librarians'),
]