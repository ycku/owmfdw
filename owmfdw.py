"""
This FDW just supports one city query.
The appid in the code is the sample appid which can not query dynamically. (static data results)
You need to apply your own appid on Open Weather Map.

API doc: https://openweathermap.org/current

CREATE SERVER owmfdw_srv FOREIGN DATA WRAPPER multicorn OPTIONS ( wrapper 'multicorn.owmfdw.owmfdw'
                                                                 ,appid='b6907d289e10d714a6e88b30761fae22' );
CREATE FOREIGN TABLE owmfdw ( city text, description text, temp float, lang text ) SERVER owmfdw_srv;

SELECT * FROM owmfdw WHERE city='Sapporo';
SELECT * FROM owmfdw WHERE city='Taipei' and lang='zh_tw';
SELECT * FROM owmfdw WHERE city='Tokyo' and lang='ja';
"""

from multicorn import ForeignDataWrapper
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
import json, urllib3

class owmfdw(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(owmfdw, self).__init__(options, columns)
        self.appid = options.get('appid', 'b6907d289e10d714a6e88b30761fae22')

    def execute(self, quals, columns):
        http = urllib3.PoolManager()
        log_to_postgres(quals)
        city = ''
        lang = 'en'
        for qual in quals:
            if qual.field_name=='city' and qual.operator=='=':
               city = qual.value
            if qual.field_name=='lang' and qual.operator=='=':
               lang = qual.value
        if city=='':
           log_to_postgres('The field \'city\' needs to be in the where clause.')
        url ='https://api.openweathermap.org/data/2.5/weather?units=metric&q='+city+'&lang='+lang+'&appid='+self.appid
        r = http.request('GET', url)
        log_to_postgres(url)
        j = json.loads(r.data)
        rows = []
        row = {}
        row['city'] = j['name']
        row['description'] = j['weather'][0]['description']
        row['temp'] = j['main']["temp"]
        row['lang'] = lang
        rows.append(row)
        return rows
        
