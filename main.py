import requests
from bs4 import BeautifulSoup as bs
import json

URL = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2"
response = requests.get(URL)
response.encoding = 'utf-8'  # Устанавливаем кодировку

if response.status_code == 200: 
    soup = bs(response.text, "html.parser")
    h3Elements = soup.find_all("h3")
    liElements = soup.select(".tss")
    inform = []

    if len(h3Elements) == len(liElements):  # Проверка на соответствие количества элементов
        for i, teacher in enumerate(h3Elements):
            teacher_info = {
                "Teacher": teacher.text,
                "Post": liElements[i].text
            }
            inform.append(teacher_info)

        with open("data.json", "w", encoding='utf-8') as json_file:
            json.dump(inform, json_file, ensure_ascii=False, indent=4)

        with open("index.html", "w", encoding='utf-8') as file_html:
            file_html.write("""<!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <title>Преподаватели МГКЦТ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
            background-color: #f0f8ff;
        }

        h1 {
            font-family: Georgia, serif;
            text-align: center;
            color: #4b0082;
        }

        table {
            width: 100%;
            background-color: #f5f5f5;
            border: 2px solid #8b0000;
        }

        th {
            padding: 10px;
            text-align: center;
            border: 1px solid #8b0000;
            background-color: #ff6347;
            color: white;
        }
        
        td {
            padding: 10px;
            text-align: center;
            border: 1px solid #8b0000;
            background-color: #ffebcd;
        }

        p {
            padding: 15px;
            color: #696969;
        }
    </style>
</head>

<body>
    <h1>Преподавательский состав</h1>
    <table>
        <tr>
            <th>№</th>
            <th>Teacher</th>
            <th>Post</th>
        </tr>
        """)

            with open("data.json", "r", encoding='utf-8') as input_file:
                text = json.load(input_file)
                for i, item in enumerate(text):
                    file_html.write(f"<tr><td>{i+1}</td><td>{item['Teacher']}</td><td>{item['Post']}</td></tr>\n")

                file_html.write("""
    </table>
    <p><a href="https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2">Источник данных</a></p>
</body>
</html>""")
        
        print("HTML файл создан.")
else:
    print(f"Ошибка: {response.status_code}")
    exit()
