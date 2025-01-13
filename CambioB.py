import tkinter as tk
from tkinter import messagebox
import numpy as np
from fractions import Fraction

# Función para generar la tabla según m (variables) y n (restricciones)
def generar_tabla():
    try:
        m = int(entry_variables.get())
        n = int(entry_restricciones.get())
        
        if m <= 0 or n <= 0:
            messagebox.showerror("Error", "La cantidad de variables y restricciones debe ser mayor que 0.")
            return
        
        # Limpiar la tabla anterior si existe
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        # Crear los encabezados de las columnas
        for i in range(m):
            encabezado = tk.Label(frame_tabla, text=f"X{i+1}", relief="solid", width=10)
            encabezado.grid(row=0, column=i)

        for i in range(n):
            encabezado = tk.Label(frame_tabla, text=f"H{i+1}", relief="solid", width=10)
            encabezado.grid(row=0, column=m + i)

        # Crear las celdas de la tabla
        for i in range(n):
            for j in range(m + n):
                entry = tk.Entry(frame_tabla, width=10)
                entry.grid(row=i+1, column=j)
                entries.append(entry)

        # Ajustar el botón Confirmar para que no se sobreponga
        boton_confirmar.grid(row=2 + n, columnspan=2, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos.")

# Función para guardar los datos ingresados en un numpy array
def guardar_tabla():
    try:
        # Obtener m y n directamente desde los widgets de entrada
        m = int(entry_variables.get())
        n = int(entry_restricciones.get())

        # Obtener el vector de n elementos
        vector = entry_vector.get()
        
        # Convertir el vector en un arreglo numpy
        vector = np.array([float(Fraction(x)) for x in vector.split(',')])

        # Mostrar los valores ingresados
        print(f"Vector: {vector}")
        
        # Crear una lista para almacenar los valores de las columnas H
        tabla_h = []
        for i in range(n):
            fila_h = []
            # Obtener los valores de la columna H de cada fila (columnas m, m+1, m+2,...)
            for j in range(m, m + n):  # Itera a través de las columnas de H
                valor = entries[i * (m + n) + j].get()  # Calcular el índice correcto
                # Convertir el valor a fracción y almacenarlo
                if valor:
                    fila_h.append(float(Fraction(valor)))
                else:
                    fila_h.append(0.0)
            tabla_h.append(fila_h)

        # Convertir la lista de valores en un numpy array
        tabla_h_array = np.array(tabla_h)
        
        # Mostrar la tabla_h_array para verificar
        print("Tabla H:")
        print(tabla_h_array)
        
        # Multiplicar tabla_h por el vector
        resultado = np.dot(tabla_h_array, vector)
        
        # Mostrar el resultado
        print(f"Resultado de la multiplicación: {resultado}")
        messagebox.showinfo("Resultado", f"El nuevo vector de solucion es: {resultado}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al guardar los datos: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Cambio en B")

# Variables para la cantidad de variables y restricciones
label_variables = tk.Label(root, text="Cantidad de Variables (m):")
label_variables.grid(row=0, column=0)
entry_variables = tk.Entry(root)
entry_variables.grid(row=0, column=1)

label_restricciones = tk.Label(root, text="Cantidad de Restricciones (n):")
label_restricciones.grid(row=1, column=0)
entry_restricciones = tk.Entry(root)
entry_restricciones.grid(row=1, column=1)

# Campo para ingresar el vector de n elementos
label_vector = tk.Label(root, text="Vector de n elementos (separados por comas):")
label_vector.grid(row=2, column=0)
entry_vector = tk.Entry(root)
entry_vector.grid(row=2, column=1)

# Botón para generar la tabla
boton_generar = tk.Button(root, text="Generar Tabla", command=generar_tabla)
boton_generar.grid(row=3, columnspan=2, pady=10)

# Frame para la tabla de entrada
frame_tabla = tk.Frame(root)
frame_tabla.grid(row=4, columnspan=2)

# Lista para almacenar las celdas de la tabla
entries = []

# Botón de Confirmar (inicialmente fuera del frame)
boton_confirmar = tk.Button(root, text="Confirmar", command=guardar_tabla)

root.mainloop()

