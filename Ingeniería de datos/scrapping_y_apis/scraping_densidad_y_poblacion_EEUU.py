import requests
from bs4 import BeautifulSoup
import csv

# URL de la página
url = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population_density"

# Hacer una solicitud GET a la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar la tabla específica (puede que necesitemos ajustar el selector)
    table = soup.find('table', {'class': 'wikitable'})

    if table:
        # Crear una lista para almacenar los datos
        data = []

        # Iterar sobre las filas de la tabla
        for row in table.find('tbody').find_all('tr')[1:]:  # Saltar la primera fila porque es la cabecera de la tabla
            cols = row.find_all('td')
            if len(cols) > 3:  # Asegurarse de que hay suficientes columnas en la fila
                estado = cols[0].get_text(strip=True)
                densidad = cols[2].get_text(strip=True)
                poblacion = cols[3].get_text(strip=True)
                data.append((estado, densidad, poblacion))

        # Guardar los datos en un archivo CSV
        with open('estados_densidad_poblacion1.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Estado', 'Densidad', 'Poblacion'])
            writer.writerows(data)

        print("Datos guardados en 'estados_densidad_poblacion.csv'")
    else:
        print("No se encontró la tabla en la página")

else:
    print("No se pudo acceder a la página")
