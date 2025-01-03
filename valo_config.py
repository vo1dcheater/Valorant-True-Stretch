import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import time

def kill_game_processes():
    try:
        #Kill Valorant
        subprocess.run(['taskkill', '/F', '/IM', 'VALORANT.exe'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'VALORANT-Win64-Shipping.exe'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'RiotClientServices.exe'], capture_output=True)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to close Valorant processes: {str(e)}")
        return False

def edit_valo_config(resolution_x=None, resolution_y=None):
    #Kill game processes first
    if not kill_game_processes():
        return
    time.sleep(5)
        
    #Find Valorant config folder
    local_appdata = os.environ.get('LOCALAPPDATA')
    valo_config_dir = os.path.join(local_appdata, 'VALORANT', 'Saved', 'Config')
    
    #Find UUID folder
    uuid_folders = [f for f in os.listdir(valo_config_dir) if os.path.isdir(os.path.join(valo_config_dir, f))]
    
    if not uuid_folders:
        messagebox.showerror("Error", "Config folder not found")
        return
    
    #Use first UUID folder
    config_path = os.path.join(valo_config_dir, uuid_folders[0], 'Windows', 'GameUserSettings.ini')
    
    try:
        #Read file
        with open(config_path, 'r') as file:
            lines = file.readlines()

        #Edit settings
        for i, line in enumerate(lines):
            if line.startswith('bShouldLetterbox='):
                lines[i] = 'bShouldLetterbox=False\n'
            elif line.startswith('bLastConfirmedShouldLetterbox='):
                lines[i] = 'bLastConfirmedShouldLetterbox=False\n'
            elif line.startswith('bUseVSync='):
                lines[i] = 'bUseVSync=False\n'
            elif line.startswith('bUseDynamicResolution='):
                lines[i] = 'bUseDynamicResolution=False\n'
            elif line.startswith('LastConfirmedFullscreenMode='):
                lines[i] = 'LastConfirmedFullscreenMode=2\n'
            elif line.startswith('PreferredFullscreenMode='):
                lines[i] = 'PreferredFullscreenMode=0\n'
            elif line.startswith('HDRDisplayOutputNits'):
                if not any("FullscreenMode=2" in line for line in lines[lines.index(line):]):
                lines.insert(i + 1, 'FullscreenMode=2\n')
            
            elif resolution_x and resolution_y:
                if line.startswith('ResolutionSizeX='):
                    lines[i] = f'ResolutionSizeX={resolution_x}\n'
                elif line.startswith('ResolutionSizeY='):
                    lines[i] = f'ResolutionSizeY={resolution_y}\n'
                elif line.startswith('LastUserConfirmedResolutionSizeX='):
                    lines[i] = f'LastUserConfirmedResolutionSizeX={resolution_x}\n'
                elif line.startswith('LastUserConfirmedResolutionSizeY='):
                    lines[i] = f'LastUserConfirmedResolutionSizeY={resolution_y}\n'

        #Save changes
        with open(config_path, 'w') as file:
            file.writelines(lines)
            
        messagebox.showinfo("Success", "open valo now and enjoy!")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def apply_settings():
    try:
        res_x = int(resolution_x_entry.get())
        res_y = int(resolution_y_entry.get())
        edit_valo_config(res_x, res_y)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for resolution")

#main window
root = tk.Tk()
root.title("Valorant True Stretch")
root.geometry("300x200")

#Resolution input frame
resolution_frame = ttk.LabelFrame(root, text="Resolution", padding=10)
resolution_frame.pack(padx=10, pady=5, fill="x")

#Resolution input fields
ttk.Label(resolution_frame, text="Width:").grid(row=0, column=0, padx=5, pady=5)
resolution_x_entry = ttk.Entry(resolution_frame)
resolution_x_entry.grid(row=0, column=1, padx=5, pady=5)
resolution_x_entry.insert(0, "1280")

ttk.Label(resolution_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
resolution_y_entry = ttk.Entry(resolution_frame)
resolution_y_entry.grid(row=1, column=1, padx=5, pady=5)
resolution_y_entry.insert(0, "960")

#button
apply_button = ttk.Button(root, text="Apply Settings", command=apply_settings)
apply_button.pack(pady=20)

#Run application
root.mainloop()
