# Código LRC

## Descripción del programa

Este código implementa un sistema de codificación y decodificación utilizando códigos LRC sobre campos finitos (256). La codificación se realiza dividiendo un mensaje en fragmentos y aplicando operaciones polinomiales para generar *shards* codificados. El proceso de decodificación reconstruye el mensaje original a partir de los *shards*, incluso en presencia de borrado de datos de alguno de los ficheros.

Se describirá con más detalle en el pdf *"Memoria_ENI.pdf"*.

## Estructura

````
proyecto/
│
├── shards/
│   ├── shard_0.shard
│   ├── shard_1.shard
|   | ...
│   └── shard_8.shard
│
├── decoded/
│   ├── recovered_{filename1}
|   | ...
│   └── recovered_{filenameM}
|
├── test/
│   ├── {filename1}
|   | ...
│   └── {filenameM}
│
├── data.csv
├── getData.py
├── getGraph.py
├── lrc.py
└── README.md
````

Presenta la siguiente distribución:

- `proyecto/` es la carpeta raíz. Puede tener cualquier nombre.
- `shards/` contiene los archivos codificados.
- `decoded/` los archivos recuperados tras la decodificación.
- `test/` los archivos que se utilizaron de ejemplo para testear el programa principal.
- `lrc.py` el código principal.
- `getData.py` el programa utilizado para testear el código principal.
- `data.csv` datos recogidos tras la ejecución.
- `getGraph.py` agrupa filas de los datos recogidos por longitud de fichero y número de *shards* borrados y representa el tiempo tardado para cada acción.


## Ejecución individual

Para poder probar este proyecto necesitarás la ubicación de un archivo cualquiera que quieras codificar y tener python instalado.

Para ejecutarlo:

```bash
  python lrc.py
```

Tras esto cargará los subconjuntos correspondientes para el código **[9,4]** de localidad **2** y te preguntará por el fichero a codificar. 
Debes escribir el fichero con la extensión correspondiente. Por ejemplo: 

```bash
  > Fichero a codificar: path_to_ejemplo.pdf
```

Tras esto realizará una parada donde se espera cualquier caracter para poder continuar. Esta parada servirá para poder simular el borrado de los *shards*. 

Una vez se desee continuar se realizará la decodificación de los archivos y volverá a preguntar por el nombre que se le quiere dar al fichero decodificado. **El nombre introducido eberá llevar la extensión del fichero para poder verlo correctamente.** Por ejemplo:

```bash
  > Nombre que le quieres dar al fichero recuperado: recovered_ejemplo.pdf
```

## Ejecución para testing

Para conseguir datos de forma más cómoda (sin tener que ir indicando uno por uno el nombre del fichero o los *shards* a borrar) se creó `getData.py`. Este archivo lo que hace es hacer un barrido sobre estos ficheros y, para cada uno, ejecutar el código `lrc.py` y borrar *shards*. Va borrando desde 0 (ninguno) hasta 3 archivos (el 0, el 3 y el 6) para cada fichero de la carpeta `test`.

Para ejecutar este fichero es necesario que **exista** una carpeta con el nombre `test` a la altura de este archivo. Dentro de esta carpeta deben estar los ficheros que queremos procesar. 

Para ejecutarlo:

```bash
  python getData.py
```

## Ejecución para obtener gráficas

Finalmente, para la evaluación de las métricas recogidas se creó el fichero `getGraph.py` que graficará los datos recogidos. Para poder hacer uso de este programa debe existir el fichero *`data.csv`*, que se genera y almacena datos al efectuar cualquier ejecución de las dos mencionadas previamente. Se generarán tres gráficas separadas: una para el tiempo de codificación, otra para el tiempo de recuperación y otra para el tiempo de decodificación. Cada gráfica muestra cómo varía el tiempo según la cantidad de shards borrados para diferentes longitudes de fichero. Las gráficas se irán mostrando una por una. 

Para ejecutarlo:

```bash
  python getGraph.py
```

## Autor

- [Alba Ferreira Charrasquiel](https://www.github.com/charrasquiel)