import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library
from libraryapp.models import model_factory
from ..connection import Connection


def get_book(book_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Book)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            b.id,
            b.title,
            b.isbn,
            b.author,
            b.year_published,
            b.librarian_id,
            b.location_id
        FROM libraryapp_book b
        WHERE b.id = ?
        """, (book_id,))

        return db_cursor.fetchone()

@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)

        template = 'books/detail.html'
        context = {
            'book': book
        }

        return render(request, template, context)