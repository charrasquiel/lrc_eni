import subprocess
import os

def wait_for_line(process, line_to_wait):
    while True:
        line = process.stdout.readline().strip()
        print(line)
        if line == line_to_wait:
            break


def remove_shards(num):
    for i in range(num):
        file = "shard_"+str(i*3)+".shard"
        os.remove(os.path.join("shards", file))


### MAIN
if __name__ == "__main__":
    for filename in os.listdir("test"):
        for i in range(4):
            process = subprocess.Popen(['python', 'lrc.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

            # Esperar por la línea de confirmación específica
            confirmacion_esperada = "> Fichero a codificar: "
            #wait_for_line(process, confirmacion_esperada)
            process.stdin.write('test/'+filename + '\n')
            process.stdin.flush()

            # Esperar por la línea de confirmación específica
            confirmacion_esperada = "Ahora puedes borrar shards."
            wait_for_line(process, confirmacion_esperada)

            remove_shards(i)

            process.stdin.write('a\n')
            process.stdin.flush()

            # Esperar por la línea de confirmación específica
            confirmacion_esperada = "Fichero decodificado."
            wait_for_line(process, confirmacion_esperada)

            # Escribir el nombre del archivo de salida
            nombre_archivo_salida = "recovered_"+filename
            process.stdin.write(nombre_archivo_salida + '\n')
            process.stdin.flush()

            process.wait()
