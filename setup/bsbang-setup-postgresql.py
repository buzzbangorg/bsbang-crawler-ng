#!/usr/bin/env python3

import psycopg2

with psycopg2.connect('dbname=buzzbang_crawl user=justincc password=passw0rd') as conn:
    with conn.cursor() as curs:
        curs.execute(
            "CREATE TABLE crawl "
            "(url TEXT NOT NULL, last_crawled timestamp NOT NULL DEFAULT now(), "
            "crawler_id TEXT NOT NULL, schema JSON NOT NULL)")
