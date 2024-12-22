import requests
from bs4 import BeautifulSoup as bs, Tag
import json

URL = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2"
response = requests.get(URL)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = bs(response.text, "html.parser")
    h3Elements = soup.find_all("h3")
    liElements = soup.select(".tss")
    inform = []

    if len(h3Elements) == len(liElements):
        for i, teacher in enumerate(h3Elements):
            teacher_info = {
                "Teacher": teacher.text,
                "Post": liElements[i].text
            }
            inform.append(teacher_info)

        with open("data.json", "w", encoding='utf-8') as json_file:
            json.dump(inform, json_file, ensure_ascii=False, indent=4)

        with open('template.html', 'r', encoding='utf-8') as file:
            filedata = file.read()

        soup = bs(filedata, "html.parser")
        element_to_paste = soup.find("div", class_="place-here")

        # Создаем таблицу и заполняем ее данными из JSON
        table = Tag(name="table")
        header_row = Tag(name="tr")
        for header in ["№", "Teacher", "Post"]:
            th = Tag(name="th")
            th.string = header
            header_row.append(th)
        table.append(header_row)

        for i, item in enumerate(inform):
            row = Tag(name="tr")
            td_num = Tag(name="td")
            td_num.string = str(i + 1)
            row.append(td_num)
            td_teacher = Tag(name="td")
            td_teacher.string = item['Teacher']
            row.append(td_teacher)
            td_post = Tag(name="td")
            td_post.string = item['Post']
            row.append(td_post)
            table.append(row)

        element_to_paste.append(table)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        print("HTML файл создан.")
else:
    print(f"Ошибка: {response.status_code}")
