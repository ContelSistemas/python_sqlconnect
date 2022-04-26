import mysql.connector
import csv

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'ptoorp',
    database = 'vpn'
)
cursor=mydb.cursor()
# CREAR LA TABLA vpn
'''
cursor.execute("CREATE DATABASE vpn")
'''
# CREAR LA TABLA vpn CON TODAS ESTAS COLUMNAS.
'''
cursor.execute("CREATE TABLE vpn\
(id INT AUTO_INCREMENT PRIMARY KEY,\
cliente VARCHAR (50),\
uso VARCHAR (50),\
modelo VARCHAR (50),\
tipo VARCHAR (50),\
nombre_vpn1 VARCHAR (50),\
pass VARCHAR (50),\
ip_gestion VARCHAR (15),\
red VARCHAR (15),\
ip_vpn_local VARCHAR (15),\
ip_vpn_remoto VARCHAR (15),\
ip_wan1 VARCHAR (15),\
proveedor VARCHAR (50),\
nombre_vpn2 VARCHAR (50),\
pass2 VARCHAR (50),\
red_vpn_bk VARCHAR (15),\
ip_vpn_bk_local VARCHAR (15),\
ip_vpn_bk_remoto VARCHAR (15),\
ip_wan2 VARCHAR (50),\
proveedor_bk VARCHAR (50),\
columna6 VARCHAR (50),\
pass_ipsec VARCHAR (50),\
area_ospf VARCHAR (3),\
loopbak_local VARCHAR (15),\
loopbak_remoto VARCHAR (15))")

#MODIFICAR UNA COLUMNA

cursor.execute("MALTER TABLE vpn ODIFY COLUMN area_ospf VARCHAR (3)")
'''
# RECOGE EL CSV Y LO INSERTA EN LA TABLA datos.
'''
with open('vpn.csv', newline='') as csvfile:

    csv_data = csv.reader(csvfile, delimiter=',', quotechar='|')
 
    for row in csv_data:
        cursor.execute('INSERT INTO vpn(cliente, uso, modelo, tipo, nombre_vpn1, pass, ip_gestion, red, ip_vpn_local, ip_vpn_remoto, ip_wan1, proveedor, nombre_vpn2, pass2, red_vpn_bk, ip_vpn_bk_local, ip_vpn_bk_remoto, ip_wan2, proveedor_bk, columna6, pass_ipsec, area_ospf, loopbak_local, loopbak_remoto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', row )
'''
sql = ("INSERT INTO vpn (cliente, uso) VALUES (%s, %s)") 
dato1 = input("nombre de cliente? ")
dato2 = input("uso? ")
val = (dato1, dato2)
cursor.execute(sql, val)
mydb.commit()

cursor.close()

# YA TENGO LOS DATOS EN LA TABLA. AHORA NECESITO SABER COMO CREAR DE MANERA AUTOMATICA MAS vpn's
