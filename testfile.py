"""
Intentionally unsicheres Demo-Programm.
Enthaelt mehrere Security-Risiken: SQL-Injection, Command-Injection, unsicheres eval, Klartext-Credentials.
NICHT in Produktion verwenden.
"""

import sqlite3
import os

# Hardcodierte Zugangsdaten (schlecht)
DB = sqlite3.connect(":memory:")
cur = DB.cursor()
cur.execute("CREATE TABLE users (username TEXT, password TEXT)")
cur.execute("INSERT INTO users VALUES ('admin', 'secret')")
DB.commit()

while True:
    inp = input("Eingabe (SQL:<qry> | SH:<cmd> | PY:<expr>): ")

    if inp.startswith("SQL:"):
        # Unsichere direkte String-Konkatenation -> SQL-Injection
        qry = inp[4:]
        try:
            rows = cur.execute(qry).fetchall()
            print(rows)
        except Exception as e:
            print("DB-Fehler:", e)

    elif inp.startswith("SH:"):
        # Unsichere Weitergabe an Shell -> Command-Injection
        cmd = inp[3:]
        os.system(cmd)

    elif inp.startswith("PY:"):
        # Gefaehrliches eval -> Ausfuehrung beliebigen Python-Codes
        expr = inp[3:]
        try:
            print(eval(expr))
        except Exception as e:
            print("Eval-Fehler:", e)

    else:
        print("Unbekanntes Format")
