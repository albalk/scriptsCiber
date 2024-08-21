import whois
import requests
import socket
import dns.resolver
import ipaddress
import sys

#ejecutar script: python scriptAuto.py nombreDominio


#hace el whois del dominio pasado por parametro
def obtener_whois(dominio):
    try:
        informacion_whois = whois.whois(dominio) #ejecuta el comando whois del dominio recibido
        return informacion_whois 
    except whois.parser.PywhoisError as e:
        return f"Error al obtener WHOIS: {e}"

#una forma para comprobar si hay filtraciones de un correo electrónico es con la API de have i been pawned
#para usar la api hay que pagar una subscripcion así que en mi caso no va a funcionar porque no la tengo
#pero dejo el codigo de como se haría en caso de tenerla. Todo lo comentado en el main es para las filtraciones
def verificar_filtracion(correo):
    api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}" #usa la API de have I been pawned
    headers = {"User-Agent": "YourApp/1.0 (your@email.com)"} #rellenar con la info personal si compras la API

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return f"La dirección de correo {correo} ha sido encontrada en filtraciones."
    elif response.status_code == 404:
        return f"La dirección de correo {correo} no ha sido encontrada en filtraciones."
    else:
        return f"Error al verificar filtración para {correo}: {response.text}"

#comprueba si el dominio esta activo
def comprobar_dominio_activo(dominio):
    try:
        direccion_ip = socket.gethostbyname(dominio) #obtiene el host (IP) del dominio
        return f"El dominio {dominio} está activo con la dirección IP: {direccion_ip}"
    except socket.gaierror:
        return f"El dominio {dominio} no está activo o no se pudo resolver su dirección IP."

#escanea el top 10 puertos
def escanear_puertos(direccion_ip):
    #declaración del TOP 10 puertos usados
    puertos_comunes = [21, 22, 23, 80, 443, 143, 3306, 8080, 8443, 53]

    resultados_escaneo = []
    for puerto in puertos_comunes: #recorre todos los puertos
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        #comprueba si el puerto actual de la IP que recibimos está activo o no
        resultado = sock.connect_ex((direccion_ip, puerto))
        sock.close()

        if resultado == 0:
            resultados_escaneo.append(f"El puerto {puerto} está abierto.")
        else:
            resultados_escaneo.append(f"El puerto {puerto} está cerrado.")

    return resultados_escaneo

#mostrar informacion servidores ns
def obtener_servidores_ns(dominio):
    try:
        respuestas = dns.resolver.resolve(dominio, 'NS')
        #añade la información del servidor ns al array
        servidores_ns = [str(respuesta) for respuesta in respuestas]
        return servidores_ns
    except dns.resolver.NXDOMAIN: #en caso de no encontrar servidor NS
        return f"No se encontraron registros NS para {dominio}."
    except dns.resolver.NoAnswer: #en caso de que el servidor del dominio no responda
        return f"No hay respuesta del servidor DNS para {dominio}."
    except dns.resolver.Timeout: #en caso de timeout
        return f"Se agotó el tiempo de espera al consultar NS para {dominio}."

#mostrar informacion servidores mx
def obtener_servidores_mx(dominio):
    try:
        respuesta = dns.resolver.resolve(dominio, 'MX')
        #añade la información del servidor ns al array
        servidores_mx = [(str(respuesta.exchange), respuesta.preference) for respuesta in respuesta]
        return servidores_mx
    except dns.resolver.NXDOMAIN: #en caso de no encontrar servidor MX
        return f"No se encontraron registros MX para {dominio}."
    except dns.resolver.NoAnswer: #en caso de que el servidor del dominio no responda
        return f"No hay respuesta del servidor DNS para {dominio}."
    except dns.resolver.Timeout: #en caso de timeout
        return f"Se agotó el tiempo de espera al consultar MX para {dominio}."

#main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python whois_script.py <dominio>")
        sys.exit(1)

    dominio = sys.argv[1] #guarda el dominio pasado por parametros

    print(f"\n///////////////////////////////WHOIS///////////////////////////////\n")
    resultado_whois = obtener_whois(dominio) #llamada a la función
    
    print(f"Información WHOIS para el dominio {dominio}:\n")
    print(resultado_whois) #imprimir los resultados

#    print(f"\n///////////////////////FILTRACIONES DE CORREO//////////////////////\n")
#    correos_en_whois = resultado_whois.get("emails", []) #obtiene el correo del comando whois
#    for correo in correos_en_whois:
#        print(verificar_filtracion(correo)) #llamada a la función

    print(f"\n////////////////////COMPROBACION DOMINIO ACTIVO////////////////////\n")
    print(comprobar_dominio_activo(dominio))

    print(f"\n//////////////////////ESCANEO TOP 10 PUERTOS///////////////////////\n")
    try:
        direccion_ip = socket.gethostbyname(dominio)
        resultados_escaneo = escanear_puertos(direccion_ip) #llamada a la función

        print("\nResultados del escaneo de puertos:")
        for resultado in resultados_escaneo: #imprime los resultados del escaneo de puertos
            print(resultado)

    except socket.gaierror: #en caso de error
        print(f"No se pudo realizar el escaneo de puertos para {dominio}.")

    print(f"\n/////////////////////INFORMACION SERVIDORES NS/////////////////////\n")
    servidores_ns = obtener_servidores_ns(dominio) #llamada a la función
    print(f"\nServidores NS para {dominio}:\n{servidores_ns}") #imprime los resultados

    print(f"\n/////////////////////INFORMACION SERVIDORES MX/////////////////////\n")
    servidores_mx = obtener_servidores_mx(dominio) #llamada a la función
    print(f"\nServidores MX para {dominio}:\n{servidores_mx}") #imprime los resultados

    print(f"\n///////////////////////////////////////////////////////////////////\n")
