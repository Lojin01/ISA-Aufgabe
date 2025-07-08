"""
Intentionally vulnerable demo program – use ONLY for Dependabot tests.

"""

import sqlite3, os, pickle, yaml, requests, random, http.server, socketserver

# Hard-coded secret
SECRET_KEY = "hardcoded-super-secret"

# Predictable random numbers
random.seed(1337)

# In-memory DB, no auth
DB = sqlite3.connect(":memory:")
cur = DB.cursor()
cur.execute("CREATE TABLE users (u TEXT, p TEXT)")
cur.execute("INSERT INTO users VALUES ('admin', 'secret')")
DB.commit()

def unsafe_pickle_load(data: bytes):
    """Deserialise untrusted pickle – LEADS TO CODE EXEC."""
    return pickle.loads(data)

def unsafe_yaml_load(text: str):
    """yaml.load with default Loader – CVE-2020-1747."""
    return yaml.load(text, Loader=yaml.Loader)

def insecure_http_fetch(url: str):
    """requests 2.19.0 with TLS disabled."""
    return requests.get(url, verify=False).text

class InsecureHandler(http.server.SimpleHTTPRequestHandler):
    """Exposes arbitrary files via path traversal."""
    def do_GET(self):
        path = self.path.lstrip("/")
        try:
            with open(path, "rb") as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
        except Exception as err:
            self.send_error(404, str(err))

def main():
    menu = ("SQL:<qry>|SH:<cmd>|PY:<expr>|EX:<code>|"
            "PK:<hex>|YAML:<txt>|GET:<url>|SRV")
    while True:
        inp = input(f"Wahl ({menu}): ")

        try:
            if inp.startswith("SQL:"):
                print(cur.execute(inp[4:]).fetchall())               # Injection
            elif inp.startswith("SH:"):
                os.system(inp[3:])                                   # Cmd inj
            elif inp.startswith("PY:"):
                print(eval(inp[3:]))                                 # Eval inj
            elif inp.startswith("EX:"):
                exec(inp[3:])                                        # Exec inj
            elif inp.startswith("PK:"):
                print(unsafe_pickle_load(bytes.fromhex(inp[3:])))    # Pickle inj
            elif inp.startswith("YAML:"):
                print(unsafe_yaml_load(inp[5:]))                     # YAML inj
            elif inp.startswith("GET:"):
                print(insecure_http_fetch(inp[4:]))                  # No TLS ver
            elif inp == "SRV":
                port = 8080
                print(f"Starte HTTP-Server auf Port {port}")
                with socketserver.TCPServer(("", port), InsecureHandler) as s:
                    s.serve_forever()
            else:
                print("Unbekanntes Format")
        except Exception as err:
            print("Fehler:", err)

if __name__ == "__main__":
    main()
