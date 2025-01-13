import tkinter as tk
from tkinter import messagebox, ttk
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
        tk.Label(frame_tabla, text="Tipo", relief="solid", width=10).grid(row=0, column=0)
        for i in range(m):
            tk.Label(frame_tabla, text=f"X{i+1}", relief="solid", width=10).grid(row=0, column=i + 1)
        for i in range(n):
            tk.Label(frame_tabla, text=f"H{i+1}", relief="solid", width=10).grid(row=0, column=m + i + 1)

        # Crear las filas con menús desplegables y entradas
        for i in range(n):
            # Menú desplegable para seleccionar el tipo de fila
            opciones = [f"X{j+1}" for j in range(m)] + [f"H{j+1}" for j in range(n)]
            tipo_var = tk.StringVar(value=opciones[0])
            dropdown = ttk.Combobox(frame_tabla, textvariable=tipo_var, values=opciones, state="readonly", width=8)
            dropdown.grid(row=i + 1, column=0)
            dropdowns.append(tipo_var)

            # Entradas para los valores
            fila = []
            for j in range(m + n):
                entry = tk.Entry(frame_tabla, width=10)
                entry.grid(row=i + 1, column=j + 1)
                fila.append(entry)
            entries.append(fila)

        # Ajustar el botón Confirmar para que no se sobreponga
        boton_confirmar.grid(row=6 + n, columnspan=2, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos.")

# Función para mostrar el resultado con campos adicionales
def mostrar_resultado(vector_resultado):
    # Limpiar el frame anterior si existe
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    # Crear encabezados
    tk.Label(frame_resultados, text="Ingreso", relief="solid", width=10).grid(row=0, column=0)
    tk.Label(frame_resultados, text="Resultado", relief="solid", width=10).grid(row=0, column=1)

    # Mostrar los resultados con campos adicionales
    for i, valor in enumerate(vector_resultado):
        entry_ingreso = tk.Entry(frame_resultados, width=10)
        entry_ingreso.grid(row=i + 1, column=0)
        entry_ingreso.insert(0, "0")  # Valor por defecto

        label_resultado = tk.Label(frame_resultados, text=f"{valor:.4f}", relief="solid", width=10)
        label_resultado.grid(row=i + 1, column=1)


# Función para guardar los datos ingresados en un numpy array
def guardar_tabla():
    try:
        m = int(entry_variables.get())
        n = int(entry_restricciones.get())
        vector = entry_vector.get()

        # Convertir los vectores en arreglos numpy
        vector = np.array([float(Fraction(x)) for x in vector.split(',')])

        if len(vector) != n:
            messagebox.showerror("Error", "El tamaño del vector debe ser igual a la cantidad de restricciones (n).")
            return

        # Crear la tabla solo con los datos de las columnas H
        tabla_h = []
        for i in range(n):
            fila_h = []
            for j in range(m, m + n):
                valor = entries[i][j].get()
                fila_h.append(float(Fraction(valor)) if valor else 0.0)
            tabla_h.append(fila_h)

        tabla_h_array = np.array(tabla_h)

        # Multiplicar tabla_h por el vector
        resultado = np.dot(tabla_h_array, vector)

        # Mostrar el resultado en la nueva tabla
        mostrar_resultado(resultado)

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al guardar los datos: {e}")

# Función para calcular Z óptima
def calcular_z_optima():
    try:
        z_optima = 0

        # Iterar por las filas de resultados
        for i in range(1, len(frame_resultados.winfo_children()) // 2):  # Cada fila tiene dos columnas
            ingreso_widget = frame_resultados.grid_slaves(row=i, column=0)[0]  # Widget de ingreso (Entry)
            resultado_widget = frame_resultados.grid_slaves(row=i, column=1)[0]  # Widget de resultado (Label)

            # Obtener valores del Entry y del Label
            ingreso = float(Fraction(ingreso_widget.get()))
            resultado = float(resultado_widget["text"])

            # Sumar producto al valor de Z óptima
            z_optima += ingreso * resultado

        # Mostrar el resultado de Z óptima
        messagebox.showinfo("Z Óptima", f"El valor de Z óptima es: {z_optima:.4f}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al calcular Z óptima: {e}")


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
label_vector = tk.Label(root, text="Nuevo vector B:")
label_vector.grid(row=2, column=0)
entry_vector = tk.Entry(root)
entry_vector.grid(row=2, column=1)

# Botón para generar la tabla
boton_generar = tk.Button(root, text="Generar Tabla", command=generar_tabla)
boton_generar.grid(row=4, columnspan=2, pady=10)

# Frame para la tabla de entrada
frame_tabla = tk.Frame(root)
frame_tabla.grid(row=5, columnspan=2)

# Lista para almacenar las celdas de la tabla y los menús desplegables
entries = []
dropdowns = []

# Botón de Confirmar (inicialmente fuera del frame)
boton_confirmar = tk.Button(root, text="Confirmar", command=guardar_tabla)

# Crear un frame para los resultados
frame_resultados = tk.Frame(root)
frame_resultados.grid(row=6, columnspan=2, pady=10)

# Ajustar el botón Confirmar para que no se sobreponga
boton_confirmar.grid(row=7, columnspan=2, pady=10)

# Botón para calcular Z óptima
boton_calcular_z = tk.Button(root, text="Calcular Z Óptima", command=calcular_z_optima)
boton_calcular_z.grid(row=8, columnspan=2, pady=10)

root.mainloop()
