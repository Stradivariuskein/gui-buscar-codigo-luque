import re
import tkinter as tk
import tkinter.font as tkFont
import os

from colorama import Fore, Style

def buscar_palabras_clave(event=None):
    op = entrada_busqueda.get().upper()
    resultados.delete("1.0", tk.END)
    ruta_actual = os.getcwd()

    try:
        articdb = open(f"{ruta_actual}/articDB.txt", "r")
    except:
        resultados.insert("1.0", "ERROR: No se pudo abrir el archivo")
        return

    encontrados = 0
    indice_inicial = "1.0"
    for linea in articdb:
        linea = normalizar(linea).upper()
        palabras = op.split()
        
        linea = linea[:78] + '\n'
        
        insertar_linea = True
        mach_plabra = 0

        for palabra in palabras:
            result = re.search(palabra, linea.upper())

            if result:
                mach_plabra += 1
                if insertar_linea:
                    resultados.insert(indice_inicial, linea)
                    insertar_linea = False
                inIndex = result.regs[0][0]
                fIndex = result.regs[0][1]

                #se colorean los maches
                tag = f"match{encontrados}"
                resultados.tag_configure(tag, foreground='red')
                current_index = resultados.index(tk.CURRENT)
                current_index = resultados.index(indice_inicial + f"+{inIndex}c")
                fin_index = resultados.index(indice_inicial + f"+{inIndex + len(palabra)}c")
                resultados.delete(current_index, fin_index)     
                resultados.insert(current_index, linea[inIndex:fIndex], (tag,))
                



                
                
        logn_labaras = len(palabras)
        #si se encontron todas las palabras se aumenta el index del tk.text si no se borra la linea previamente ingresada
        if mach_plabra == logn_labaras:
            encontrados += 1
            indice_inicial = resultados.index(indice_inicial + f"+{len(linea)}c")
        else:
            indice_final =resultados.index(tk.CURRENT)
            resultados.delete(indice_inicial, indice_final)



    resultados_label.config(text=f"Resultados: {encontrados}")



def normalizar(linea):
    linea = linea.replace('¤', 'ñ')
    linea = linea.replace('§', '°')
    linea = linea.replace('ø', '°')
    linea = linea.replace('£', 'Ú')
    linea = linea.replace('¥', 'ñ')
    return linea


def copiar_seleccion(event=None):
    try:
        seleccion = resultados.get(resultados.curselection())
        ventana.clipboard_clear()
        ventana.clipboard_append(seleccion)
    except:
        pass

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Búsqueda de palabras clave")
ventana.geometry("800x500")


# Crear un contenedor para agrupar la barra de búsqueda y el botón
contenedor = tk.Frame(ventana)
contenedor.pack(pady=10, padx=10, fill=tk.X)

# Cuadro de entrada para la búsqueda
entrada_busqueda = tk.Entry(contenedor, width=50, font=('Arial', 14))
entrada_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True)
entrada_busqueda.bind('<Return>', buscar_palabras_clave)
entrada_busqueda.focus_set()
entrada_busqueda.config(bg='white', fg='black', highlightbackground='gray', highlightthickness=1, relief=tk.FLAT, insertbackground='black', selectbackground='#bde4ff')

# Botón para iniciar la búsqueda
boton_buscar = tk.Button(contenedor, text="Buscar", command=buscar_palabras_clave, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
boton_buscar.pack(side=tk.RIGHT, padx=(10, 0))

#Área de texto para mostrar los resultados
fuente_personalizada = tkFont.Font(family="Helvetica", size=12, weight="bold")
resultados = tk.Text(ventana, font=fuente_personalizada)
resultados.pack(expand=True, fill="both")
resultados.bind('<Control-c>', copiar_seleccion)

#Configuración de la barra de desplazamiento
scrollbar = tk.Scrollbar(resultados)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultados.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=resultados.yview)

# Etiqueta para el número de resultados
resultados_label = tk.Label(ventana, text="")
resultados_label.pack()

ventana.mainloop()