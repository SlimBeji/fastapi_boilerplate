def parse_db_url(database_url):
    client_str = database_url.split("://")[0]
    database_url = database_url.lstrip(f"{client_str}://")

    user = database_url.split("@")[0].split(":")[0]
    password = database_url.split("@")[0].split(":")[1]
    database_url = database_url.lstrip(f"{user}:{password}")[1:]
    host = database_url.split(":")[0]
    port = database_url.split("/")[0].split(":")[1]
    database_name = database_url.split("/")[1]

    return {
        "client": client_str,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "db": database_name,
    }
