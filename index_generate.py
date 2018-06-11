from shutil import copyfile
import os
import code
import uuid
import subprocess
import sys

PDF_GEN_APP_DIR = os.path.dirname(os.path.abspath(__file__))


class ArticlePart(object):
    def __init__(self, href=None, link=None):
        self.href = href
        self.link = link

    def generate_html_code(self):
        latex_code =\
            '<article><a href="{0}" target="_blank">>{1}</a></article>\n'\
            .format(self.href, self.link)
        return latex_code


class HtmlFile(object):
    def __init__(self):
        self.template_path = os.path.join(PDF_GEN_APP_DIR,
                                          "index_template.html")
        self.temp_dir = os.path.join(PDF_GEN_APP_DIR, "static")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.exercises = []

    def add_exercise(self, href, link):
        self.exercises.append(ArticlePart(href, link))

    def add_exercise_obj(self, exercise):
        if not isinstance(exercise, ArticlePart):
            raise
        self.exercises.append(exercise)

    def generate(self):
        exs_latex_code = "".join(
            [exercise.generate_html_code() for exercise in self.exercises])
        PDF_GEN_APP_DIR = os.path.dirname(os.path.abspath(__file__))
        file_to_edit = os.path.join(self.temp_dir, "index.html")
        copyfile(self.template_path,
                 file_to_edit)
        print(file_to_edit)
        with open(file_to_edit, "r+") as file:
            content = file.read()
            content = content.replace(r"%%%ARTICLES%%%", exs_latex_code)
            file.seek(0)
            file.truncate()
            file.write(content)


if __name__ == '__main__':
    dirs = os.listdir(path=sys.argv[1])
    html_file = HtmlFile()
    for dire in dirs:
        html_file.add_exercise(dire, dire)
    html_file.generate()
