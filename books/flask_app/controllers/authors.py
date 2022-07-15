from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import book as book_module, author
from pprint import pprint

@app.route("/authors")
def authors():
    authors = author.Author.get_all()
    return render_template("author_add.html", authors=authors)

@app.route("/create_author", methods=['POST'])
def create_author():
    author.Author.insert_one(request.form)
    return redirect("/authors")

@app.route("/authors/<int:id>")
def show_author(id):
    data = {
        'id' : id
    }
    newBookList = []
    books = book_module.Book.get_all()

    template_author = author.Author.get_all_relationships(data)
    
    for this_book in books:
        for favorite in template_author.books:
            if favorite.id == this_book.id and this_book not in newBookList:
                newBookList.append(this_book)

    for tempbook in newBookList:
        print(tempbook.title)
        books.remove(tempbook)

    return render_template("author_show.html", author=template_author, books=books)

@app.route("/author/add/favorite", methods=['POST'])
def author_add_favorite():
    data = {
        'author_id' : request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.save_favorite(data)
    return redirect(f"/authors/{request.form['author_id']}")
