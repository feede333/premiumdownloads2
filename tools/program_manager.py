import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
from datetime import datetime

class ProgramManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Programas - PremiumDownloads")
        self.root.geometry("600x800")

        # Crear el formulario
        self.create_form()

    def create_form(self):
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Campos del formulario
        fields = [
            ("ID del programa:", "id"),
            ("Título:", "title"),
            ("Categoría:", "category"),
            ("Tamaño del archivo:", "fileSize"),
            ("Descripción:", "description", "text"),
            ("Sistema operativo:", "os"),
            ("Procesador:", "processor"),
            ("RAM:", "ram"),
            ("Espacio en disco:", "disk"),
            ("Pantalla:", "display")
        ]

        self.entries = {}
        
        for field in fields:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            label = ttk.Label(frame, text=field[0])
            label.pack(side=tk.LEFT)
            
            if len(field) > 2 and field[2] == "text":
                entry = tk.Text(frame, height=4, width=40)
            else:
                entry = ttk.Entry(frame, width=40)
            entry.pack(side=tk.LEFT, padx=5)
            
            self.entries[field[1]] = entry

        # Botón para seleccionar imagen
        ttk.Button(self.scrollable_frame, text="Seleccionar imagen", 
                  command=self.select_image).pack(pady=5)

        # Botón para guardar
        ttk.Button(self.scrollable_frame, text="Guardar programa", 
                  command=self.save_program).pack(pady=20)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )

    def save_program(self):
        try:
            data = {}
            for key, entry in self.entries.items():
                if isinstance(entry, tk.Text):
                    data[key] = entry.get("1.0", tk.END).strip()
                else:
                    data[key] = entry.get().strip()

            # Validar campos requeridos
            if not all([data["id"], data["title"], data["category"]]):
                messagebox.showerror("Error", "Los campos ID, título y categoría son obligatorios")
                return

            # Modificar las rutas para asegurar la ubicación correcta
            base_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Base dir: {base_dir}")  # Debug

            # Subir un nivel para llegar a la raíz del proyecto
            repo_dir = os.path.dirname(os.path.dirname(base_dir))
            print(f"Repo dir: {repo_dir}")  # Debug

            # Definir rutas correctas
            frontend_dir = os.path.join(repo_dir, "frontend", "public")
            images_dir = os.path.join(frontend_dir, "images")
            data_dir = os.path.join(frontend_dir, "data")
            
            print(f"Images dir: {images_dir}")  # Debug
            print(f"Data dir: {data_dir}")  # Debug

            # Crear directorios si no existen
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(data_dir, exist_ok=True)

            # Verificar que los directorios se crearon
            print(f"Images dir exists: {os.path.exists(images_dir)}")
            print(f"Data dir exists: {os.path.exists(data_dir)}")

            # Copiar imagen
            if hasattr(self, 'image_path') and self.image_path:
                image_filename = f"{data['id']}{os.path.splitext(self.image_path)[1]}"
                image_dest = os.path.join(images_dir, image_filename)
                print(f"Copying image to: {image_dest}")  # Debug
                shutil.copy2(self.image_path, image_dest)
                data["image"] = f"images/{image_filename}"

            # Guardar JSON
            json_path = os.path.join(data_dir, "programs.json")
            print(f"JSON path: {json_path}")  # Debug

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    programs_data = json.load(f)
                    print(f"Loaded existing JSON with {len(programs_data.get('programs', []))} programs")
            except FileNotFoundError:
                print("Creating new programs.json")
                programs_data = {"programs": []}

            # Añadir nuevo programa
            programs_data["programs"].append({
                "id": data["id"],
                "title": data["title"],
                "category": data["category"],
                "fileSize": data["fileSize"],
                "date": datetime.now().strftime("%d.%m.%Y"),
                "image": data.get("image", "images/default.png"),
                "description": data["description"],
                "requirements": {
                    "os": data["os"],
                    "processor": data["processor"],
                    "ram": data["ram"],
                    "disk": data["disk"],
                    "display": data["display"]
                }
            })

            # Guardar JSON con formato legible
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(programs_data, f, indent=2, ensure_ascii=False)
                print(f"Saved JSON successfully")

            # Verificar que el archivo se guardó
            print(f"JSON file exists: {os.path.exists(json_path)}")
            print(f"JSON file size: {os.path.getsize(json_path)} bytes")

            messagebox.showinfo("Éxito", "Programa guardado correctamente")
            
            # Ejecutar git status para ver cambios
            import subprocess
            result = subprocess.run(['git', 'status'], 
                                  cwd=repo_dir, 
                                  capture_output=True, 
                                  text=True)
            print("\nGit status:")
            print(result.stdout)

            self.root.quit()

        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar el programa: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramManagerApp(root)
    root.mainloop()

# Archivo batch para actualizar el repositorio
batch_file_content = """@echo off
echo Actualizando repositorio...

REM Forzar actualización del índice de git
git update-index --refresh

echo Verificando cambios...
git status

echo.
echo Subiendo cambios...
git add -A
git commit -m "Update: %date% %time%"
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo Cambios subidos exitosamente!
    timeout /t 2 >nul
) else (
    echo.
    echo Hubo un error al subir los cambios.
    echo Presiona cualquier tecla para cerrar...
    pause >nul
)
"""

batch_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "update.bat")
with open(batch_file_path, "w") as batch_file:
    batch_file.write(batch_file_content)