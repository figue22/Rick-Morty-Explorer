

import json
import requests

API_URL = "https://rickandmortyapi.com/api/character"

def menu():
    print("\nBienvenido al explorador Ricky & Morty\n")
    print("Elige una opcion para iniciar\n")
    print("1.Buscar personaje por nombre")
    print("2.Ver personajes por estado")
    print("3.Mostrar estadisticas")
    print("4.Guardar favoritos")
    print("5.Ver favoritos")
    print("6.Salir\n")


lista_favoritos = []

def obtener_personaje_por_nombre(nombre, API_URL):
        
        api_url = f"{API_URL}/?name={nombre}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "results" not in data:
            print("\nNo se encontraron resultados 🫤\n")
            return None
        
        return data['results'][0]
        

    

def transformar_personaje(info):
    return {
            "name": info['name'],
            "status": info["status"],
            "species": info["species"],
            "type": info["type"] or "N/A",
            "gender": info["gender"],
            "origin": info["origin"]["name"],
            "location": info["location"]["name"]
        }



def buscar_personaje():
    nombre = input("Ingrese el nombre del personaje 👉: ").strip()

    if not nombre:
        print("\nEl nombre no puede estar vacio ❌\n")
        return 
    
    try:
         info = obtener_personaje_por_nombre(nombre, API_URL)

         if not info:
              print("\nNo se encontró el personaje🙅‍♂️\n")
              return
        
         
         personaje = transformar_personaje(info)

         print("\n👉👉Información del personaje👀:")
         for clave, valor in personaje.items():
              print(f"{clave}: {valor}")

    except requests.exceptions.RequestException as e:
         print(f"Error en la solicitud: {e}")


def obetener_personajes_por_estado(estado, API_URL):
        api_url = f"{API_URL}/?status={estado}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'results' not in data:
             print("\nNo se encontraron resultados❌\n")
             return
        
        return data['results']


def obtener_todos_personajes(API_URL):
        api_url = API_URL
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'results' not in data:
             print("\nNo se encontraron resultados❌\n")
             return
        
        return data['results']

def calcular_estadistica_por_especie(API_URL):
     cuenta_especies = {}
     try:
          data = obtener_todos_personajes(API_URL)

          for personaje in data:
               if personaje['species'] not in cuenta_especies:
                    cuenta_especies[personaje['species']] = 1
               
               else:
                    cuenta_especies[personaje['species']] += 1

          return cuenta_especies

     except requests.exceptions.RequestException as e:
          print(f"Error en la solicitud {e}")


def calcular_total_personajes(API_URL):
     try:
          data = obtener_todos_personajes(API_URL)

          cantidad_personajes = len(data)

          return cantidad_personajes
     
     except requests.exceptions.RequestException as e:
          print(f"Error en la solicitud: {e}")


def calcular_especie_mas_comun(API_URL):
     total_por_especie = calcular_estadistica_por_especie(API_URL)

     if not total_por_especie:
          print("Ocurrio un error")
          return
     
     especie_mas_comun = max(total_por_especie, key= total_por_especie.get)

     return especie_mas_comun


def calcular_total_por_estado(API_URL):

     total_por_estado = {}
     try:
          data = obtener_todos_personajes(API_URL)

          for personaje in data:
               if personaje['status'] not in total_por_estado:
                    total_por_estado[personaje['status']] = 1
               
               else:
                    total_por_estado[personaje['status']] += 1

          return total_por_estado
     
     except requests.exceptions.RequestException as e:
          print(f"Error en la solicitud: {e}")


def mostrar_estadisticas(API_URL):
     print("\nEstadisticas de los personajes📶:\n")

     total_personajes = calcular_total_personajes(API_URL)
     especie_mas_comun = calcular_especie_mas_comun(API_URL)
     total_por_estado = calcular_total_por_estado(API_URL)
     print(f"Total de personajes: {total_personajes} 📶✅")
     print(f"Especie mas comun: {especie_mas_comun} 🔥🔝")
     print("Total por estado:")
     for estado, valor in total_por_estado.items():
          print(f"{estado}: {valor} 🔥✅")


def buscar_personajes_por_estado():
     estado = input("\nIngrese el estado de los personajes👉:\n")

     if not estado:
          print("\nEl estado no puede ser vacio❌\n")
          return
     
     try:
          info = obetener_personajes_por_estado(estado, API_URL)

          if not info:
               print(f"\nNo se econtraron personajes con el estado {estado}❌\n")
               return
          
          print(f"\nPersonajes con el estado: {estado}✅\n")

          for pesonaje in info:
                personaje_transformado = transformar_personaje(pesonaje)
                for clave, valor in personaje_transformado.items():
                     print(f"{clave}: {valor}")
                print("〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️")   

     except requests.exceptions.RequestException as e:
          print(f"Error en la sulicitud: {e}")


def obtener_favorito_por_nombre(nombre, API_URL):
    print(f"\nBuscando el personaje {nombre} en la API...")
    info = obtener_personaje_por_nombre(nombre, API_URL)
    return info



def guardar_favorito(lista_favoritos):
     favorito = input("\nIngrese el nombre de su personaje favorito: ")

     if not favorito:
          print("El personaje no puede ser vacio")
          return
     
     try:
          info_favorito = obtener_favorito_por_nombre(favorito, API_URL)

          if not info_favorito:
               print("Personaje no encontrado")
               return
          
          transformar_favorito = transformar_personaje(info_favorito)

          agregar_favorito_lista(transformar_favorito, lista_favoritos)

          print(f"Personaje agregado a favoritos con exito:")
          for i, favorito in enumerate(lista_favoritos, start=1):
               print (f"{i}.{favorito['name']}")

     except requests.exceptions.RequestException as e:
          print(f"Error en la solicitud: {e}")
          


     

def agregar_favorito_lista(favorito, lista_favoritos):
     
    if not favorito:
          print("No hay personaje para agregar")
          return
    
    if favorito in lista_favoritos:
         print("El personaje ya se encuentra agregado a favoritos")
         return
     
    lista_favoritos.append(favorito)

    return lista_favoritos


def ver_favoritos(lista_favoritos):

     if len(lista_favoritos) == 0:
          print("No tienes personajes favoritos agregados actualmente")
          return
     
     print("\nTus personajes favoritos son:\n")
     for i, favorito in enumerate(lista_favoritos, start=1):
          print(f"{i}.{favorito['name']}")





def iniciar_programa(lista_favoritos):
     ejecucion = True
     while ejecucion:
          menu()

          try:
     
               opcion_menu = int(input("\nIngrese la opcion que desea:\n"))

               if opcion_menu == 1:
                    buscar_personaje()

               elif opcion_menu == 2:
                    buscar_personajes_por_estado()
               
               elif opcion_menu == 3:
                    mostrar_estadisticas(API_URL)

               elif opcion_menu == 4:
                    guardar_favorito(lista_favoritos)
               
               elif opcion_menu == 5:
                    ver_favoritos(lista_favoritos)

               elif opcion_menu == 6:
                    print("El programa ha finalizado.")
                    ejecucion = False
           
          except ValueError:
               print("Por favor, ingrese un número válido para la opción del menú.") 

     

     
if __name__ == "__main__":
     iniciar_programa(lista_favoritos)







