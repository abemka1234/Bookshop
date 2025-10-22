import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
import more_itertools
from dotenv import load_dotenv 

def on_reload():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    load_dotenv()
    template = env.get_template("template.html")
    with open(os.getenv("FILENAME_BOOKLIST", "meta_data.json"), "r",encoding="UTF8") as my_file:
        books = json.load(my_file)

    books_pages = list(more_itertools.chunked(books, 15))
    os.makedirs("pages",exist_ok=True)

    for books_number, books_part in enumerate(books_pages, 1):
        rendered_page = template.render(
            books = books_part,
            pages_count = len(books_pages),
            current_page = books_number,
        )
        with open("pages/index{}.html".format(books_number), "w", encoding="utf8") as file:
            file.write(rendered_page)

def main():
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root="",default_filename="pages/index1.html")


if __name__ == "__main__":
    main()