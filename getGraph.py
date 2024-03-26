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

# Crear una gráfica para cada valor de 'Longitud del fichero' según los datos de 'Tiempo de Codificación'
for longitud, group in grouped_len:
    plt.plot(group['Cantidad de shards borrados'], group['Tiempo de Codificación'], label=f'Longitud {longitud}')

# Añadir etiquetas y leyenda
plt.xlabel('Cantidad de shards borrados')
plt.ylabel('Tiempo de Codificación')
plt.title('Tiempo de Codificación para diferentes longitudes de fichero')
plt.legend()
plt.grid(True)
plt.xticks(grouped_data['Cantidad de shards borrados'].unique())

# Mostrar la gráfica
plt.show()


# Crear una gráfica para cada valor de 'Longitud del fichero' según los datos de 'Tiempo de Recuperación'
for longitud, group in grouped_len:
    plt.plot(group['Cantidad de shards borrados'], group['Tiempo de Recuperación'], label=f'Longitud {longitud}')

# Añadir etiquetas y leyenda
plt.xlabel('Cantidad de shards borrados')
plt.ylabel('Tiempo de Recuperación')
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
plt.ylabel('Tiempo de Decodificación')
plt.title('Tiempo de Decodificación para diferentes longitudes de fichero')
plt.legend()
plt.grid(True)
plt.xticks(grouped_data['Cantidad de shards borrados'].unique())

# Mostrar la gráfica
plt.show()