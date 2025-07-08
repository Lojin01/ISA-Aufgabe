import sqlite3, os, pickle, yaml, random, http.server, socketserver

# Harte Kryptoschluessel (schlecht)
SECRET_KEY = "hardcoded-super-secret"

# Unsicherer RNG mit fixiertem Seed
random.seed(1337)

# In-Memory-DB ohne Schutz
DB = sqlite3.connect(":memory:")
cur = DB.cursor()
cur.execute("CREATE TABLE users (u TEXT, p TEXT)")
cur.execute("INSERT INTO users VALUES ('admin', 'secret')")
DB.commit()

def unsafe_pickle_load(data):
    # Beliebige Codeausfuehrung beim Laden
    return pickle.loads(data)

def unsafe_yaml_load(text):
    # YAML Unsafe Load
    return yaml.load(text, Loader=yaml.Loader)

class InsecureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Pfad-Traversal
        path = self.path.lstrip("/")
        try:
            with open(path, "rb") as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
        except Exception as e:
            self.send_error(404, str(e))

def main():
    while True:
        inp = input("Wahl (SQL:<qry>|SH:<cmd>|PY:<expr>|PK:<hex>|YAML:<txt>|EX:<code>|SRV): ")

        if inp.startswith("SQL:"):
            # SQL-Injection
            qry = inp[4:]
            print(cur.execute(qry).fetchall())

        elif inp.startswith("SH:"):
            # Command-Injection
            os.system(inp[3:])

        elif inp.startswith("PY:"):
            # Eval-Injection
            print(eval(inp[3:]))

        elif inp.startswith("PK:"):
            # Unsichere Pickle-Deserialisierung
            data = bytes.fromhex(inp[3:])
            print(unsafe_pickle_load(data))

        elif inp.startswith("YAML:"):
            # Unsichere YAML-Deserialisierung
            print(unsafe_yaml_load(inp[5:]))

        elif inp.startswith("EX:"):
            # exec mit Benutzereingabe
            exec(inp[3:])

        elif inp == "SRV":
            # Unsicherer HTTP-Server
            port = 8080
            print(f"Starte Server auf Port {port}")
            with socketserver.TCPServer(("", port), InsecureHandler) as httpd:
                httpd.serve_forever()

        else:
            print("Unbekanntes Format")

if __name__ == "__main__":
    main()
