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

            # Modificar las rutas para GitHub Pages
            base_dir = os.path.dirname(os.path.abspath(__file__))
            repo_dir = os.path.dirname(os.path.dirname(base_dir))
            
            # Las rutas deben ser relativas a la raíz del repositorio
            data_dir = os.path.join(repo_dir, "data")
            images_dir = os.path.join(repo_dir, "images")
            
            # Crear directorios si no existen
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Copiar imagen
            if hasattr(self, 'image_path') and self.image_path:
                image_filename = f"{data['id']}{os.path.splitext(self.image_path)[1]}"
                image_dest = os.path.join(images_dir, image_filename)
                shutil.copy2(self.image_path, image_dest)
                data["image"] = f"/premiumdownloads2/images/{image_filename}"  # Ruta para GitHub Pages

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
            
            # Actualizar repositorio
            print("\nActualizando repositorio...")
            import subprocess

            # Guardar cambios JSON actuales
            backup_json = None
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    backup_json = f.read()

            try:
                # Forzar sincronización con remoto
                print("Sincronizando con remoto...")
                subprocess.run(['git', 'fetch', 'origin'], cwd=repo_dir, check=True)
                subprocess.run(['git', 'reset', '--hard', 'origin/main'], cwd=repo_dir, check=True)
                subprocess.run(['git', 'pull', 'origin', 'main'], cwd=repo_dir, check=True)

                # Restaurar JSON con los nuevos cambios
                if backup_json:
                    current_json = json.loads(backup_json)
                    try:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            remote_json = json.load(f)
                    except FileNotFoundError:
                        remote_json = {"programs": []}

                    # Combinar programas
                    existing_ids = {prog["id"] for prog in remote_json["programs"]}
                    for prog in current_json["programs"]:
                        if prog["id"] not in existing_ids:
                            remote_json["programs"].append(prog)

                    # Guardar JSON combinado
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(remote_json, f, indent=2, ensure_ascii=False)

                # Agregar y subir cambios
                print("Subiendo cambios...")
                subprocess.run(['git', 'add', 'data/programs.json'], 
                             cwd=repo_dir, check=True)
                
                if hasattr(self, 'image_path'):
                    subprocess.run(['git', 'add', 'images/*'], 
                                 cwd=repo_dir, check=True)
                
                subprocess.run(['git', 'commit', '-m', f'Update: Nuevo programa {data["title"]}'],
                             cwd=repo_dir, check=True)
                
                subprocess.run(['git', 'push', 'origin', 'main'],
                             cwd=repo_dir, check=True)
                
                print("Repositorio actualizado exitosamente")
                messagebox.showinfo("Éxito", "Programa guardado y sincronizado correctamente")
                self.root.quit()

            except subprocess.CalledProcessError as git_error:
                print(f"Error en Git: {str(git_error)}")
                
                # Restaurar backup si algo falló
                if backup_json:
                    with open(json_path, 'w', encoding='utf-8') as f:
                        f.write(backup_json)
                
                raise git_error

        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", 
                "No se pudo actualizar el repositorio.\n" +
                "Tus cambios están guardados localmente pero deberás sincronizar manualmente.")
            
            # Mostrar estado actual
            try:
                status = subprocess.run(['git', 'status'], 
                                     cwd=repo_dir, 
                                     capture_output=True, 
                                     text=True)
                print("\nEstado del repositorio:")
                print(status.stdout)
            except Exception as git_status_error:
                print(f"Error al obtener estado de git: {str(git_status_error)}")
                pass

        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar el programa: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramManagerApp(root)
    root.mainloop()