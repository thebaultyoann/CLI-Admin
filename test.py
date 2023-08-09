with open("mariadb_ip", "r") as f:
    database_ip = f.readline()

print(database_ip)

print(str(database_ip))