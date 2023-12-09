import xlsxwriter
from get_info_for_recording import get_info

# импортируем функцию get_info которая возвращает данные по каждой карточке с цитатами
# создаем Excel файл
# задаем размеры полей в таблице (ширина колонок)
# загружаем данные в таблицу по очереди, карточку за карточкой
def writer(parametrs):
    book = xlsxwriter.Workbook(r"C:\Studies\BS4\BS4_website_with_Login\quotes.xlsx")
    page = book.add_worksheet('Цитаты')

    row = 0
    column = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 100)
    page.set_column("C:C", 20)

    for item in parametrs:
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        row += 1
    book.close()

writer(get_info())