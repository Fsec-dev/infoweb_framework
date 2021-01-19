#!/usr/bin/env python3
import socket
import sys, os
import random, re
import requests, json
from bs4 import BeautifulSoup
# Modulo encargado de añadir los colores
from modulos import colors

__author__ = "F-sec (Andrew)"
__version__ = "1.0"
__update__ = "01/19/2021"

# Funcion para limpiar la terminal
clear = lambda:os.system("clear")

# Instancia para el manejo de los colores
c = colors.colors()

conexion = True

# Lista con los posibles directorios
lista_dir = "recursos/dir_admin"
# Creando arreglo con los directorios
with open(lista_dir, "r") as f:
	dirlist = []
	for line in f:
		line = line.rstrip("\n")
		dirlist.append(line)

# Verificando la conexion a internet 
def verifyconex():
	try:
		reqs = requests.get("https://www.google.com")
		if reqs.ok:
			return True
	except requests.ConnectionError:
		return False

def urlparser(url):
	# Quitando el "/" de la ultima parte de la URL para no tener problemas con
	# la libreria requests.
	if '/' is url[-1]:
		url = url[0:-1]
	# Si la url no especifica el tipo de protocolo asignar uno (http)
	if not url.startswith("http") == True:
		return "http://" + url
	else:
		return url
		
# Funcion encargada de lanzarnos un USERAGENT de forma aleatoria
def randomUA():
	UA = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
		  'Mozilla/5.0 (X11; FreeBSD amd64; rv:40.0) Gecko/20100101 Firefox/40.0',
		  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36 OPR/48.0.2685.7',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
		  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
		  'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
		  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.97.1211.3',
	 	  'Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36',
		  'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1']
	return random.choice(UA)

def ayuda():
	print ("""
-----------------		----------------------------
	Comando					Descripcion
-----------------		----------------------------
	info 			Informacion de este proyecto
	help/ayuda		Obtener este cuadro de ayuda
	getheader		Obtener el header del servidor Web
	getrobot		Leendo fichero robots.txt si existe
	getlocation		Obteniendo la ubicacion del servidor Web
	geturls			Obteniendo URLS del sitio
	getdir			Obtener panel admin
	getemail		Obteniendo direcciones EMAIL
	getsub			Obteniendo lista de subdominios del servidor
	cls 			Limpiar la terminal
	reset 			Ingresar nuevamente el Target
	salir/exit			Salir (obvio)		
		""")

def banner():
	print (c.bold_w + """
            _  _  _ ____ ____ _ _ _ ____ ___  
            | |\\ | |___ |  | | | | |___ |__] 
            | | \\| |    |__| |_|_| |___ |__] 
	   - Information Gathering | Active & Pasive - 
	""" + c.non)	
	print (c.r + "\t[Version: %s ]"%__version__)
	print ("\t[Programado por: %s ]"%__author__)
	print ("\t[Ultima actualizacion: %s ]\n\n"%__update__ + c.non)

# Funcion encargada de leer el fichero robots.txt del servidor
def readRobot(host):
	re = requests.get(host + "/robots.txt", headers={'User-agent':randomUA()})
	
	if re.ok:
		print (re.text)
	elif re.status_code == 404:
		print (c.r + "\n[-] El fichero robots.txt no se encuentra en el servidor\n" + c.non)
	else:
		print (c.r + "\nError " + str(re.status_code) + c.non)

# Obteniendo header del servidor Web
def getheader(host):
	r = requests.get(host, headers={'User-agent':randomUA()})
	if r.ok:
		print (c.bold_w + "\n[ HEADERS del Servidor ]\n" + c.non)

		for infoheaders in r.headers:
			print (infoheaders + " : " + r.headers[infoheaders])
		print ("\n")
	else:
		print ("\nError al conectarse con el servidor\nError: {}".format(r.status_code))

# Obteniendo las URLS de la pagina Web
def geturls(host):
	r = requests.get(host, headers={'User-agent':randomUA()})
	if r.ok:
		soup = BeautifulSoup(r.text, 'lxml')

		print (c.bold_w + "\n[+] URLS encontrados en el servidor \n" + c.non)
		
		for url in soup.find_all('a'):
			url = re.findall('href=\"(.*?)\"', str(url))
			for urls in url:
				if urls.startswith("http"):
					print (urls)

		print (c.bold_w + "\n[+] Comentarios encontrados en la pagina\n" + c.non)

		# Obteniendo comentarios de la pagina
		for lineas in re.findall('<!-- (.*?) -->', r.text):
			print (lineas)

# Recorriendo el fichero "dir_admin" en busca de directorios interesantes
def getadmin(host):
	print (c.bold_g + "Escaneado directorios del servidor..." + c.non)
	
	for path in dirlist:
		try:
			r = requests.get (host + path, headers= {'User-Agent':randomUA()}, timeout=5)
			
			if (r.status_code != 404): 
				print (c.bold_w + "\n[📂] URL : {}{}".format(host, path) + c.g + " Status Code: %s" % r.status_code + c.non)
			else:
				continue
		except KeyboardInterrupt:
			print (c.bold + "\n[i] Operacion interrumpida!!!\n" + c.non)
			break
		except Exception as ex:
			print (ex)
			break

# Obteniendo direcciones de EMAIL
def getemail(host):
	req = requests.get(host)
	if req.ok:
		print (c.bold_g + "\n[+] Direcciones obtenidas:" + c.non)
		i = 0
		for lista in re.findall('[a-zA-Z0-9._\\-]*\\@[a-zA-Z0-9._\\-]*', req.text):
			i = i + 1
			print (lista)

		if i == 0: print (c.w + "[-] Ninguna direccion encontrada :(\n" + c.non)
		
# Obteniendo la geolocalizacion del servidor
def getlocation(host):
	# Obteniendo la IP del Server
	host = socket.gethostbyname(host.split("//")[1])
	api = "https://ipinfo.io/"+host+"/json"
	r = requests.get(api, headers={'User-Agent':'curl/7.47.0'})
	
	if r.status_code != 200:
			print ("\nError {}\n".format(r.status_code))
	else:
		j = json.loads(r.text)

		ip = j['ip']
		city = j['city']
		region = j['region']
		geo = j['loc']
		isp = j['org']
		
		print (c.bold_w + "\n[+] Geolocalizacion del servidor\n" + c.non)
		
		print ("""
IP: {}
Ciudad: {}
Region: {}
Geolocalizacion: {}
ISP: {}
		""".format(ip, city, region, geo, isp))

# Verificando si un subdominio esta online
def verifysub(target):
	try:
		r = requests.get("http://" + target, headers={'User-Agent':randomUA()})

		if r.ok:
			return target + c.bold_g + " [ONLINE]" + c.non
		elif r.status_code == 401:
			return target + c.bold_r + " [Acceso denegado: Error 401]" + c.non
		else:
			return target + c.bold_r + " [Codigo de error: %s]"%str(r.status_code) + c.non
	except:
		pass

# Obteniendo subdominios
def getsubdomin(host):
	list_urls = []

	req = requests.get("https://rapiddns.io/subdomain/%s?full=1"%host,
	headers={'User-Agent':'curl/7.47.0'},
	timeout=5)
		
	if req.ok:
		geturl = re.findall('_blank">(.*?)</a>', req.text)
		
		print (c.bold_w + "\n[+] Lista de Subdominios\n" + c.non)
		print (c.bold_w + "[i] Verificando si los servidores estan Online..." + c.non)

		for urls in geturl:
			list_urls.append(urls)

		# Eliminando elementos repetidos
		for u in list(set(list_urls)):
			if verifysub(u) != None:
				print (verifysub(u))
	
	else:
		print ("Error: " + str(req.status_code))

def main():
	clear()  # Limpiar la terminal	
	banner() # Mostrar un bonito banner :)
	
	print (c.bold_g + "\n[info]" + c.non + c.bold_w + " Antes de comenzar, ingresa la url del servidor objetivo\n" + c.non)
	target = input("Target: ")

	if target == "":
		print (c.r + "\n[!]" + c.non + c.bold_r + " Ingresa la URL del servidor para continuar\n" + c.non)
		exit(0)
	else:
		target = urlparser(target)
			
	while True:
		prompt = input(c.line_g + "[infoweb]> " + c.non)

		if prompt in ['salir', 'exit']:
			clear()
			c.rainbow("\nBye and Happy Hacking!!!")
			break
		
		if prompt in "info":
			banner()
			print (c.bold_g + "[ Info ]" + c.non)
			print (c.w + """
Infoweb es un proyecto individual creado para la fase
de reconocimiento teniendo como objetivo un servidor Web
este proyecto es Software Libre por lo tanto sientete libre
de modificar este Script.

Happy Hacking!!.
				""" + c.non)
		elif prompt in "banner":
			banner()
		
		elif prompt in "cls":
			clear()

		elif prompt in "getrobot":
			readRobot(target)

		elif prompt in "getheader":
			getheader(target)

		elif prompt in "geturls":
			geturls(target)

		elif prompt in "getdir":
			getadmin(target)

		elif prompt in "getemail":
			getemail(target)
			
		elif prompt in "getlocation":
			if verifyconex() != True: 
				print (c.bold_r + "[!]" + c.bold_w + " Esta funcion requiere conexion a internet" + c.non)
				input()	
			else:
				getlocation(target)

		elif prompt in "getsub":
			if verifyconex() != True: 
				print (c.bold_r + "[!]" + c.bold_w + " Esta funcion requiere conexion a internet" + c.non)
				input()
			else:	
				getsubdomin(target.split("//")[1])
		
		elif prompt in "reset":
			clear()
			main()

		elif prompt in ['ayuda', 'help']:
			ayuda()

		else:
			print (c.bold + "\n[info]"+ c.bold_w + " Usa el comando ayuda para una lista de comandos a usar \n" + c.non)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		clear()
		c.rainbow("Bye and Happy Hacking!!")
