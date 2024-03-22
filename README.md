# Código LRC

## Descripción del programa

Este código implementa un sistema de codificación y decodificación utilizando códigos LRC sobre campos finitos (256). La codificación se realiza dividiendo un mensaje en fragmentos y aplicando operaciones polinomiales para generar *shards* codificados. El proceso de decodificación reconstruye el mensaje original a partir de los *shards*, incluso en presencia de borrado de datos de alguno de los ficheros.

Se describirá con más detalle en el pdf *"Memoria_ENI.pdf"*.

## Ejecución

Para poder probar este proyecto necesitarás la ubicación de un archivo cualquiera que quieras codificar y tener python instalado.

Para ejecutarlo:

```bash
  python lrc.py
```

Tras esto cargará los subconjuntos correspondientes para el código **[9,4]** de localidad **2** y te preguntará por el fichero a codificar. 
Debes escribir el fichero con la extensión correspondiente. Por ejemplo: 

```bash
  > Fichero a codificar: ejemplo.pdf
```

Tras esto realizará una parada donde se espera cualquier caracter para poder continuar. Esta parada servirá para poder simular el borrado de los *shards*. 
Una vez se desee continuar se realizará la decodificación de los archivos y volverá a preguntar por el nombre que se le quiere dar al fichero decodificado. **El nombre introducido eberá llevar la extensión del fichero para poder verlo correctamente.** Por ejemplo:

```bash
  > Nombre que le quieres dar al fichero recuperado: recovered_ejemplo.pdf
```

## Autor

- [Alba Ferreira Charrasquiel](https://www.github.com/charrasquiel)