from django.urls import include, path
from .views import *


app_name = "libraryapp"

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('books/', book_list, name='books'),
    path('librarians/', librarian_list, name='librarians'),
    path('libraries/', library_list, name='librarians'),
]