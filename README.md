# owmfdw
PostgreSQL FDW example for Open Weather Map

- This FDW just supports one city query.
- The default appid in the code is the sample appid which can not query dynamically. (static data results)
- You need to apply your own appid on [Open Weather Map](https://openweathermap.org/).

## Installation
This FDW is based on [Multicorn](https://multicorn.org/) project.

- On Debian bullseye 

```
# apt install postgresql-11-python3-multicorn
# git clone https://github.com/ycku/owmfdw.git
# cd owmfdw
# cp owmfdw.py /usr/lib/python3/dist-packages/multicorn/
```

## on PostgreSQL

- Replace appid with your appid

```
CREATE EXTENSION multicorn;
CREATE SERVER owmfdw_srv FOREIGN DATA WRAPPER multicorn OPTIONS ( wrapper 'multicorn.owmfdw.owmfdw'
                                                                 ,appid='b6907d289e10d714a6e88b30761fae22' );
CREATE FOREIGN TABLE owmfdw ( city text, description text, temp float, lang text ) SERVER owmfdw_srv;

SELECT * FROM owmfdw WHERE city='Sapporo';
SELECT * FROM owmfdw WHERE city='Taipei' and lang='zh_tw';
SELECT * FROM owmfdw WHERE city='Tokyo' and lang='ja';
```

## Sample

```
postgres=# SELECT * FROM owmfdw WHERE city='Sapporo' and lang='ja';
  city   | description  | temp | lang 
---------+--------------+------+------
 Sapporo | 曇りがち      |   10 | ja
(1 row)
```
