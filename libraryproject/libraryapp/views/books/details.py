import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, Librarian
from libraryapp.models import model_factory
from ..connection import Connection


def create_book(cursor, row):
    _row = sqlite3.Row(cursor, row)

    book = Book()
    book.id = _row["book_id"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.title = _row["title"]
    book.year_published = _row["year_published"]

    librarian = Librarian()
    librarian.id = _row["librarian_id"]
    librarian.first_name = _row["first_name"]
    librarian.last_name = _row["last_name"]

    library = Library()
    library.id = _row["library_id"]
    library.title = _row["library_name"]

    book.librarian = librarian
    book.location = library

    return book

def get_book(book_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_book
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            b.id book_id,
            b.title,
            b.isbn,
            b.author,
            b.year_published,
            b.librarian_id,
            b.location_id,
            li.id librarian_id,
            u.first_name,
            u.last_name,
            loc.id library_id,
            loc.title library_name
        FROM libraryapp_book b
        JOIN libraryapp_librarian li ON b.librarian_id = li.id
        JOIN libraryapp_library loc ON b.location_id = loc.id
        JOIN auth_user u ON u.id = li.user_id
        WHERE b.id = ?
        """, (book_id,))

        return db_cursor.fetchone()

@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)
        template_name = 'books/detail.html'
        return render(request, template_name, {'book': book})

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE libraryapp_book
                SET title = ?,
                    author = ?,
                    isbn = ?,
                    year_published = ?,
                    location_id = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['author'],
                    form_data['isbn'], form_data['year_published'],
                    form_data["location"], book_id,
                ))

            return redirect(reverse('libraryapp:books'))

        # Check if this POST is for deleting a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM libraryapp_book
                    WHERE id = ?
                """, (book_id,))

            return redirect(reverse('libraryapp:books'))