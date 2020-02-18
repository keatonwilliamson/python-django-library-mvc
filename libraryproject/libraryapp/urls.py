from django.urls import include, path
from .views import *


app_name = "libraryapp"

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),

    path('books/', book_list, name='books'),
    path('book/form', book_form, name='book_form'),
    path('books/<int:book_id>/', book_details, name='book'),
    path('books/<int:book_id>/form/', book_edit_form, name='book_edit_form'),

    path('libraries/', library_list, name='libraries'),
    path('library/form', library_form, name='library_form'),
    path('libraries/<int:library_id>/', library_details, name='library'),

    path('librarians/', librarian_list, name='librarians'),
    path('librarians/<int:librarian_id>/', librarian_details, name='librarian'),
]