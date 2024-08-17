import os
import shutil
import win32com.client

def move_folder(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    shutil.move(src_folder, dest_folder)

def create_shortcut(target_path, shortcut_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.save()

def main():
    # Definir las rutas
    src_folder = 'ConnectionApp'
    dest_folder = r'C:\Archivos de Sistema\ConnectionApp'
    executable_path = os.path.join(dest_folder, 'ConnectionApp.exe')
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop, 'ConnectionApp.lnk')

    # Mover la carpeta
    try:
        move_folder(src_folder, dest_folder)
        print(f'Carpeta movida a {dest_folder}')
    except Exception as e:
        print(f'Error al mover la carpeta: {e}')
        return

    # Crear el acceso directo
    try:
        create_shortcut(executable_path, shortcut_path)
        print(f'Acceso directo creado en {shortcut_path}')
    except Exception as e:
        print(f'Error al crear el acceso directo: {e}')

if __name__ == '__main__':
    main()
