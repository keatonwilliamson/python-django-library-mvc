import sqlite3
from django.shortcuts import render
from libraryapp.models import Librarian
from ..connection import Connection


def librarian_list(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            l.id,
            l.location_id,
            l.user_id,
            u.first_name,
            u.last_name,
            u.email
        from libraryapp_librarian l
        join auth_user u on l.user_id = u.id
        """)

        all_librarians = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            lib = Librarian()
            lib.id = row["id"]
            lib.location_id = row["location_id"]
            lib.user_id = row["user_id"]
            lib.first_name = row["first_name"]
            lib.last_name = row["last_name"]
            lib.email = row["email"]

            all_librarians.append(lib)

    template_name = 'librarians/list.html'

    context = {
        'all_librarians': all_librarians
    }

    return render(request, template_name, context)