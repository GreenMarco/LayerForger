import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

def procesar_imagenes(base_path, folder_path, nombre_output):
    base_dir = os.path.dirname(base_path)
    output_folder = os.path.join(base_dir, nombre_output)
    os.makedirs(output_folder, exist_ok=True)

    try:
        base_image = Image.open(base_path).convert("RGBA")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen base:\n{e}")
        return

    archivos = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]
    total = len(archivos)
    if total == 0:
        messagebox.showwarning("Sin imágenes", "No se encontraron imágenes .png en la carpeta de imágenes.")
        return

    progress_bar["maximum"] = total
    progress_bar["value"] = 0

    for i, filename in enumerate(archivos, start=1):
        activo_path = os.path.join(folder_path, filename)

        try:
            activo_image = Image.open(activo_path).convert("RGBA")
        except:
            continue

        composed_image = base_image.copy()
        paste_x = base_image.width - activo_image.width
        paste_y = 0
        composed_image.paste(activo_image, (paste_x, paste_y), activo_image)

        output_path = os.path.join(output_folder, filename)
        composed_image.save(output_path)

        progress_bar["value"] = i
        root.update_idletasks()

    messagebox.showinfo("Proceso completado", f"Se procesaron {total} imágenes.\nGuardadas en:\n{output_folder}")

def mostrar_thumbnail(image_path, label_widget):
    try:
        img = Image.open(image_path)
        img.thumbnail((128, 128))
        photo = ImageTk.PhotoImage(img)
        label_widget.configure(image=photo, text="")
        label_widget.image = photo
    except:
        label_widget.configure(image='', text="Vista no disponible")

def mostrar_preview_compuesta():
    base_path = base_entry.get()
    folder_path = folder_entry.get()
    if not (os.path.isfile(base_path) and os.path.isdir(folder_path)):
        return
    try:
        base_img = Image.open(base_path).convert("RGBA")
        for f in os.listdir(folder_path):
            if f.lower().endswith(".png"):
                activo_img = Image.open(os.path.join(folder_path, f)).convert("RGBA")
                compuesta = base_img.copy()
                compuesta.paste(activo_img, (base_img.width - activo_img.width, 0), activo_img)
                compuesta.thumbnail((256, 384))
                photo = ImageTk.PhotoImage(compuesta)
                preview_compuesta.configure(image=photo, text="")
                preview_compuesta.image = photo
                break
    except:
        preview_compuesta.configure(image='', text="Vista previa fallida")

def seleccionar_base():
    file_path = filedialog.askopenfilename(
        title="Selecciona la imagen base",
        filetypes=[("Imagen PNG", "*.png")]
    )
    if file_path:
        base_entry.delete(0, tk.END)
        base_entry.insert(0, file_path)
        mostrar_thumbnail(file_path, base_preview)
        mostrar_preview_compuesta()

def seleccionar_carpeta():
    folder_path = filedialog.askdirectory(title="Selecciona la carpeta de imágenes")
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

        # Mostrar preview de primer PNG encontrado
        for f in os.listdir(folder_path):
            if f.lower().endswith(".png"):
                primer_png = os.path.join(folder_path, f)
                mostrar_thumbnail(primer_png, activo_preview)
                mostrar_preview_compuesta()
                break

def ejecutar():
    base_path = base_entry.get()
    folder_path = folder_entry.get()
    nombre_output = carpeta_salida_entry.get().strip()

    if base_path.strip() in ["", "imagen.png"] or not os.path.isfile(base_path):
        messagebox.showerror("Error", "La ruta de la imagen base no es válida.")
        return

    if folder_path.strip() in ["", "Ubicación de carpeta"] or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "La ruta de la carpeta de imágenes no es válida.")
        return
    nombre_output = carpeta_salida_entry.get().strip()
    if nombre_output == "" or nombre_output == "Escribe el nombre de la carpeta":
        messagebox.showerror("Error", "Debes indicar un nombre válido para la carpeta de salida.")
        return


    procesar_imagenes(base_path, folder_path, nombre_output)

def poner_placeholder(event):
    if carpeta_salida_entry.get().strip() == "":
        carpeta_salida_entry.insert(0, "Escribe el nombre de la carpeta")
        carpeta_salida_entry.config(fg="grey")

def quitar_placeholder(event):
    if carpeta_salida_entry.get() == "Escribe el nombre de la carpeta":
        carpeta_salida_entry.delete(0, tk.END)
        carpeta_salida_entry.config(fg="black")

def poner_placeholder_generico(entry, texto):
    if entry.get().strip() == "":
        entry.insert(0, texto)
        entry.config(fg="grey")

def quitar_placeholder_generico(entry, texto):
    if entry.get() == texto:
        entry.delete(0, tk.END)
        entry.config(fg="black")


# Interfaz
root = tk.Tk()
root.title("LayerForger")
root.iconbitmap("icono.ico")
root.update_idletasks()  # Forza a que se midan todos los widgets visibles
root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())


# Entradas y botones
tk.Label(root, text="Imagen base (.png):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
base_entry = tk.Entry(root, width=50, fg="grey")
base_entry.insert(0, "imagen.png")
base_entry.grid(row=0, column=1)
base_entry.bind("<FocusIn>", lambda e: quitar_placeholder_generico(base_entry, "imagen.png"))
base_entry.bind("<FocusOut>", lambda e: poner_placeholder_generico(base_entry, "imagen.png"))
tk.Button(root, text="Seleccionar...", command=seleccionar_base).grid(row=0, column=2, padx=5)

tk.Label(root, text="Carpeta de imágenes:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
folder_entry = tk.Entry(root, width=50, fg="grey")
folder_entry.insert(0, "Ubicación de carpeta")
folder_entry.grid(row=1, column=1)
folder_entry.bind("<FocusIn>", lambda e: quitar_placeholder_generico(folder_entry, "Ubicación de carpeta"))
folder_entry.bind("<FocusOut>", lambda e: poner_placeholder_generico(folder_entry, "Ubicación de carpeta"))
tk.Button(root, text="Seleccionar...", command=seleccionar_carpeta).grid(row=1, column=2, padx=5)

tk.Label(root, text="Nombre carpeta salida:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
carpeta_salida_entry = tk.Entry(root, width=50, fg="grey")
carpeta_salida_entry.insert(0, "Escribe el nombre de la carpeta")
carpeta_salida_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=5)

# Asociar eventos
carpeta_salida_entry.bind("<FocusIn>", quitar_placeholder)
carpeta_salida_entry.bind("<FocusOut>", poner_placeholder)


# Previews
tk.Label(root, text="Vista Base:").grid(row=3, column=0, sticky="e", padx=5)
base_preview = tk.Label(root, text="Sin vista")
base_preview.grid(row=3, column=1, sticky="w")

tk.Label(root, text="Vista Activo:").grid(row=4, column=0, sticky="e", padx=5)
activo_preview = tk.Label(root, text="Sin vista")
activo_preview.grid(row=4, column=1, sticky="w")

tk.Label(root, text="Vista Previa Compuesta:").grid(row=5, column=0, sticky="e", padx=5)
preview_compuesta = tk.Label(root, text="Sin vista")
preview_compuesta.grid(row=5, column=1, sticky="w")

# Barra de progreso
progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.grid(row=6, column=0, columnspan=3, pady=10)

# Botón principal
tk.Button(root, text="Ejecutar", command=ejecutar, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=3, pady=10)

root.mainloop()
