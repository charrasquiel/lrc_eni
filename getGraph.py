import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
data = pd.read_csv('data.csv', header=None)

# Renombrar las columnas
data.columns = ['Longitud del fichero', 'Tiempo de Codificación', 'Tiempo de Recuperación', 'Tiempo de Decodificación', 'Cantidad de shards borrados']

# Agrupar por la primera y última columna y calcular las medias
grouped_data = data.groupby(['Longitud del fichero', 'Cantidad de shards borrados']).mean().reset_index()

# Agrupar por 'Longitud del fichero'
grouped_len = grouped_data.groupby('Longitud del fichero')
# Calcular el promedio del tiempo de codificación por tamaño del archivo
average_coding_time = grouped_len['Tiempo de Codificación'].mean()

# Obtener los tamaños de los archivos
file_sizes = average_coding_time.index

# Obtener el tiempo promedio de codificación
coding_times = average_coding_time.values

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(file_sizes, coding_times, marker='o', color='r', linestyle='-')
plt.title('Tiempo de Codificación vs Tamaño del Fichero')
plt.xlabel('Tamaño del Fichero')
plt.ylabel('Tiempo de Codificación (s)')
plt.grid(True)
plt.show()


# Crear una gráfica para cada valor de 'Longitud del fichero' según los datos de 'Tiempo de Recuperación'
for longitud, group in grouped_len:
    plt.plot(group['Cantidad de shards borrados'], group['Tiempo de Recuperación'], label=f'Longitud {longitud}')

# Añadir etiquetas y leyenda
plt.xlabel('Cantidad de shards borrados')
plt.ylabel('Tiempo de Recuperación (s)')
plt.title('Tiempo de Recuperación para diferentes longitudes de fichero')
plt.legend()
plt.grid(True)
plt.xticks(grouped_data['Cantidad de shards borrados'].unique())

# Mostrar la gráfica
plt.show()

# Crear una gráfica para cada valor de 'Longitud del fichero' según los datos de 'Tiempo de Decodificación'
for longitud, group in grouped_len:
    plt.plot(group['Cantidad de shards borrados'], group['Tiempo de Decodificación'], label=f'Longitud {longitud}')

# Añadir etiquetas y leyenda
plt.xlabel('Cantidad de shards borrados')
plt.ylabel('Tiempo de Decodificación (s)')
plt.title('Tiempo de Decodificación para diferentes longitudes de fichero')
plt.legend()
plt.grid(True)
plt.xticks(grouped_data['Cantidad de shards borrados'].unique())

# Mostrar la gráfica
plt.show()