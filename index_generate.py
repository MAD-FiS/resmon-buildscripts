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
    def __init__(self, template_file_name="index_template.html"):
        self.template_path = os.path.join(PDF_GEN_APP_DIR,
                                          template_file_name)
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

    def generate(self, output_file_name="index.html"):
        exs_latex_code = "".join(
            [exercise.generate_html_code() for exercise in self.exercises])
        PDF_GEN_APP_DIR = os.path.dirname(os.path.abspath(__file__))
        file_to_edit = os.path.join(self.temp_dir, output_file_name)
        copyfile(self.template_path,
                 file_to_edit)
        with open(file_to_edit, "r+") as file:
            content = file.read()
            content = content.replace(r"%%%ARTICLES%%%", exs_latex_code)
            file.seek(0)
            file.truncate()
            file.write(content)


class RowTableSinglePart(object):
    def __init__(self, href=None, name=None):
        self.href = href
        self.name = name

    def generate_html_code(self):
        latex_code =\
            '<tr>\n'\
            '<td><a href="{0}">{1}</a></td>\n'\
            '</tr>'.format(self.href, self.name)
        return latex_code


class TabNameSinglePart(object):
    def __init__(self, href, tabname, rows_param=[]):
        self.href = href
        self.tabname = tabname
        self.rows = rows_param

    def generate_tabname_card_code(self):
        latex_code =\
            '<li role="presentation"><a href="#{0}" aria-controls="{0}" role="tab" data-toggle="tab">{1}</a></li>\n'\
            .format(self.href, self.tabname)
        return latex_code

    def add_row(self, rowhref, rowname):
        self.rows.append(RowTableSinglePart(rowhref, rowname))

    def add_row_obj(self, row):
        if not isinstance(row, RowTableSinglePart):
            raise
        self.rows.append(row)

    def generate_tabname_content_code(self, output_file_name="index_beauty.html"):
        rows_latex_code = "".join(
            [row.generate_html_code() for row in self.rows])
        tabs_content_latex_code =\
            '<div role="tabpanel" class="tab-pane fade in active" id="{0}">'\
            '    <div class="panel panel-default">'\
            '      <!-- Default panel contents -->'\
            '      <div class="panel-heading">Zawartość</div>'\
            '      <!-- Table -->'\
            '      <table class="table">'\
            '          {1}'\
            '      </table>'\
            '    </div>'\
            '</div>'.format(self.href, rows_latex_code)
        return tabs_content_latex_code


class HtmlBeautyFile(object):
    def __init__(self, title, template_file_name="index_template_beauty.html"):
        self.template_path = os.path.join(PDF_GEN_APP_DIR,
                                          template_file_name)
        self.temp_dir = os.path.join(PDF_GEN_APP_DIR, "static")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.tabs = []
        self.title = title

    def add_tab(self, href, tabname, rows):
        self.tabs.append(TabNameSinglePart(href, tabname, rows))

    def add_tab_obj(self, tab):
        if not isinstance(tab, TabNameSinglePart):
            raise
        self.tabs.append(tab)

    def generate(self, output_file_name="index_beauty.html"):
        tabs_card_code = "".join(
            [tab.generate_tabname_card_code() for tab in self.tabs])
        tabs_content_code = "".join(
            [tab.generate_tabname_content_code() for tab in self.tabs])

        PDF_GEN_APP_DIR = os.path.dirname(os.path.abspath(__file__))
        file_to_edit = os.path.join(self.temp_dir, output_file_name)
        copyfile(self.template_path,
                 file_to_edit)
        with open(file_to_edit, "r+") as file:
            content = file.read()
            content = content.replace(r"%%%TABNAME%%%", tabs_card_code)
            content = content.replace(r"%%%TABCONTENT%%%", tabs_content_code)
            content = content.replace(r"%%%TITLE%%%", self.title)
            file.seek(0)
            file.truncate()
            file.write(content)


# if __name__ == '__main__':
#     dirs = os.listdir(path=sys.argv[1])
#     html_file = HtmlFile()
#     for dire in dirs:
#         html_file.add_exercise(dire, dire)
#     html_file.generate()

import code
if __name__ == '__main__':
    row_one = []
    row_two = []
    row_three = []
    dirs = os.listdir(path=sys.argv[1])
    html_file = HtmlBeautyFile(title=sys.argv[2])
    for dire in dirs:
        if dire != "swagger_index.html":
            row_one.append(RowTableSinglePart(dire, dire))

    html_file.add_tab('tab11', "Dokumentacja Pydoc", row_one)
    if sys.argv[2] == "resmon-monitor":
        row_two.append(RowTableSinglePart("swagger_index.html", "Otwórz Swagger"))
        html_file.add_tab('tab22', "Dokumentacja Swagger", row_two)
    row_three.append(RowTableSinglePart("../guide_pl.pdf", "Otwórz Podręcznik"))
    html_file.add_tab('tab33', "Podręcznik użytkownika", row_three)

    html_file.generate()
