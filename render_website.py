from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
import more_itertools
import os

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
with open("meta_data.json", "r",encoding="UTF8") as my_file:
    books = json.load(my_file)

books_pages = list(more_itertools.chunked(books, 15))
os.makedirs("pages")

for i, books_part in enumerate(books_pages, 1):
    rendered_page = template.render(
        books = books_part,
    )
    with open('pages/index{}.html'.format(i), 'w', encoding="utf8") as file:
        file.write(rendered_page)

server = Server()
server.watch('*.html', shell('make html', cwd='docs'))
server.serve(root='')