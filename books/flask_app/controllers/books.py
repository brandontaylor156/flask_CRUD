from flask_app import app, render_template, request, redirect, session
from flask_app.models import book, author as author_module

@app.route("/")
def index():
    return redirect("/books")

@app.route("/books", methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        book.Book.save(request.form)
        return redirect("/books")
    
    books = book.Book.get_all()
    return render_template("book_add.html", books=books)

@app.route("/books/<int:id>")
def book_show(id):
    data = {
        'id' : id
    }
    newAuthorList = []
    authors = author_module.Author.get_all()

    template_book = book.Book.get_all_relationships(data)
    
    for this_author in authors:
        for favorite in template_book.authors:
            if favorite.id == this_author.id and this_author not in newAuthorList:
                newAuthorList.append(this_author)

    for temp_author in newAuthorList:
        print(temp_author.first_name)
        authors.remove(temp_author)

    return render_template("book_show.html", book=template_book, authors=authors)

@app.route("/book/add/favorite", methods=['POST'])
def book_add_favorite():
    data = {
        'author_id' : request.form['author_id'],
        'book_id': request.form['book_id']
    }
    book.Book.save_favorite(data)
    return redirect(f"/books/{request.form['book_id']}")
