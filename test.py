with open("mariadb_ip", "r") as f:
    database_ip = f.readline()

database_ip = database_ip.replace(" ", "")

print(database_ip)