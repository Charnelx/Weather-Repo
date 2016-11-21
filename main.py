from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4, A2
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle
import requests
import json
from datetime import datetime


API_KEY = ''

def get_weather(city_id):
    URL = 'http://api.openweathermap.org/data/2.5/group'

    payload = {
        'id': ','.join(city_id),
        'units': 'metric',
        'APPID': API_KEY,
    }
    r = requests.get(URL, params=payload)

    if r.status_code == 200:
        dict = json.loads(r.content.decode('utf-8'))
        return dict

def create_report(cities):
    doc = SimpleDocTemplate(
            'report.pdf',
            rightMargin=5,
            leftMargin=5,
            topMargin=30,
            bottomMargin=72,
            pagesize=A4)

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER))
    styles.add(ParagraphStyle(
            name="Justify", fontSize=10, alignment=TA_JUSTIFY))


    data = []
    data.append(Paragraph('Current weather on {: %I:%M:%S, %d.%m.%Y}'.format(datetime.now()), styles['Title']))
    data.append(Spacer(1, 12))

    table_data = []
    table_data.append([
            Paragraph('Town', styles['TableHeader']),
            Paragraph('Current temp', styles['TableHeader']),
            Paragraph('Pressure', styles['TableHeader']),
            Paragraph('Humidity', styles['TableHeader']),
            Paragraph('Wind speed', styles['TableHeader']),
            Paragraph('Description', styles['TableHeader']),
    ])

    for city in cities['list']:
        table_data.append(
                [
                 Paragraph(city['name'].strip(), styles['Justify']),
                 Paragraph(str(city['main']['temp']).strip(), styles['Justify']),
                 Paragraph(str(city['main']['pressure']).strip(), styles['Justify']),
                 Paragraph(str(city['main']['humidity']).strip(), styles['Justify']),
                 Paragraph(str(city['wind']['speed']).strip(), styles['Justify']),
                 Paragraph(str(city['weather'][0]['description']).lower().strip(), styles['Justify']),
                ]
        )

    wh_table = Table(table_data, colWidths=[doc.width/6.0]*6)
    wh_table.hAlign = 'CENTER'
    wh_table.hAlign = 'CENTER'
    wh_table.setStyle(TableStyle(
        [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
         ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
         ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
         ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
    data.append(wh_table)
    data.append(Spacer(1, 48))


    doc.build(data)

if __name__ == '__main__':
    city_id = ['703448', '524901', '625144', '756135', '618426', '683506', '2643743', '2950159', '2988507']
    result = get_weather(city_id)
    create_report(result)