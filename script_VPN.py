import os
from datetime import date
import urllib.request
import ipaddress
import mysql.connector

today = date.today()

def borrarPantalla():
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")
borrarPantalla()
name_file = input ("¿Que nombre le daermos a esta VPN? ")
#name_vpn = input ("¿Que nombre tiene la VPN principal? ")
name_vpn = (name_file + '-Contel')
#name_vpn_bk = input ("¿Que nombre tiene la VPN de Backup? ")
name_vpn_bk = (name_vpn + '_BK')
ip_vpn_local = input ("¿cual es la ip local de la vpn principal? ")
ip_vpn = ipaddress.IPv4Address(ip_vpn_local)
ip_vpn_remote = (ip_vpn + 1)
ip_vpn_local_bk = (ip_vpn + 256)
ip_vpn_remote_bk = (ip_vpn + 257)
#ip_vpn_remote = input ("¿Cual es la ip remota de la vpn principal? ")
#ip_vpn_local_bk = input ("¿cual es la ip vpn de backup servidor? ")
#ip_vpn_remote_bk = input ("¿Cual es la ip vpn del backup cliente? ")
password_l2tp = input ("¿Cual es la contraseña L2tp? ")
area_id = input ("¿Cual será el número de área asignada? " )
#area_name = input ("¿Que nombre le daremos a este área? ")
area_name = ('area-' + area_id)
#instance_name = input ("¿Que nombre tiene esta instancia OSPF? ")
instance_name = ('OSPF-' + name_vpn)
#wan_lcr = input ("¿Que direccion ip uasermos de LCR? ")

borrarPantalla()

f = open ("servidor.src", "w")
## MK Servidor ##
f.write('/interface l2tp-server \n')
f.write('add name=% s'% name_vpn )
f.write(' user=% s \n'% name_vpn)
f.write('add name=% s'% name_vpn_bk)
f.write(' user=% s \n'% name_vpn_bk)
f.write('\n/ppp profile \n')
f.write('add name=% s'% name_vpn)
f.write(' local-address=% s' % ip_vpn_local)
f.write(' remote-address=% s' % ip_vpn_remote)
f.write('\nadd name=% s'% name_vpn_bk)
f.write(' local-address=% s' % ip_vpn_local_bk)
f.write(' remote-address=% s' % ip_vpn_remote_bk)
f.write('\n/ppp secret \n')
f.write('add name=% s'% name_vpn)
f.write(' password=% s' % password_l2tp)
f.write(' service=l2tp')
f.write(' profile=% s' % name_vpn)
f.write('\nadd name=% s'% name_vpn_bk)
f.write(' password=% s' % password_l2tp)
f.write(' service=l2tp')
f.write(' profile=% s' % name_vpn_bk)
f.write('\n/interface bridge add name=loopback-% s' % area_id)
f.write('\n/ip address add address=10.255.254.% s' % area_id)
f.write(' interface=loopback-% s' % area_id)
## OSPF ##
f.write('\n/routing ospf instance add name=% s' % instance_name)
f.write(' router-id=10.255.254.% s' % area_id)
f.write('\n/routing ospf interface')
f.write('\nadd interface=% s' % name_vpn)
f.write(' authentication=md5 authentication-key=!contelospf#2020 network-type=point-to-point')
f.write('\nadd interface=% s' % name_vpn_bk)
f.write(' authentication=md5 authentication-key=!contelospf#2020 network-type=point-to-point')
f.write('\n/routing ospf area add name=% s' % area_name)
f.write(' instance=% s' % instance_name)
f.write(' area-id=0.0.0.% s' % area_id)
f.write('\n/routing ospf network') 
f.write('\nadd network=% s' % ip_vpn_remote)
f.write(' area=% s' % area_name)
f.write('\nadd network=% s' % ip_vpn_remote_bk)
f.write(' area=% s' % area_name)
f.close()
## Configuracion lado del Cliente ##
f = open ("cliente.src", "w")
f.write('/interface l2tp-client \n')
f.write('add name=% s' % name_vpn)
f.write(' connect-to=80.39.126.201 user=% s' % name_vpn)
f.write(' password=% s' % password_l2tp)
f.write(' use-ipsec=no ipsec-secret=!contelmkvpn2017 allow-fast-path=yes allow=mschap2,mschap1 disabled=no\n')
f.write('add name=% s' % name_vpn_bk)
f.write(' connect-to=88.26.225.249 user=% s' % name_vpn_bk)
f.write(' password=% s' % password_l2tp)
f.write(' use-ipsec=no ipsec-secret=!contelmkvpn2017 allow-fast-path=yes allow=mschap2,mschap1 disabled=no\n')
f.write('/interface bridge add name=loopback\n')
f.write('/ip address add address=10.255.255.% s' % area_id)
f.write(' interface=loopback\n')
f.write('/routing ospf instance add name=% s' % instance_name)
f.write(' router-id=10.255.255.% s' % area_id)
f.write('\n/routing ospf interface\n')
f.write('add interface=% s' % name_vpn)
f.write(' authentication=md5 authentication-key=!contelospf#2020 network-type=point-to-point\n')
f.write('add interface=% s' % name_vpn_bk)
f.write(' authentication=md5 authentication-key=!contelospf#2020 network-type=point-to-point\n')
f.write('/routing ospf area add name=Area-% s' % area_id)
f.write(' instance=% s' % instance_name)
f.write(' area-id=0.0.0.% s' % area_id)
f.write('\n/routing ospf network\n')
f.write('add network=% s' % ip_vpn_local)
f.write(' area=Area-% s' % area_id)
f.write('\nadd network=% s' % ip_vpn_local_bk)
f.write(' area=Area-% s' % area_id)
f.write('\nadd network=10.255.255.% s' % area_id)
f.write(' area=Area-% s' % area_id)
f.close()
print ('Usa los ficheros generados servidor.scr y cliente.scr, contienen un script para poder configurar de forma rapida. ')
print ('La VPN l2tp y la conexión OSPF ')

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'ptoorp',
    database = 'vpn'
)
cursor=mydb.cursor()

sql = ("INSERT INTO vpn (cliente, nombre_vpn1, pass, ip_vpn_local) VALUES (%s, %s, %s, %s)") 
val = (name_file, name_vpn, password_l2tp, ip_vpn_local)
cursor.execute(sql, val)
mydb.commit()




