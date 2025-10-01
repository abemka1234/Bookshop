from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
with open("meta_data.json", "r",encoding="UTF8") as my_file:
    books = json.load(my_file)
rendered_page = template.render(
    books = books,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = Server()
server.watch('*.html', shell('make html', cwd='docs'))
server.serve(root='')