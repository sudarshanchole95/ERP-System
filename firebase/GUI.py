import customtkinter as ctk
import threading
import sys
import os
import re
from tkinter import filedialog

# --- IMPORT BACKEND ---
try:
    import uploader as backend
except ImportError:
    print("⚠️ 'uploader.py' not found. Make sure it is in the same directory.")
    backend = None

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", str)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("🔥 Universal Firestore Importer")
        self.geometry("900x700")

        # Layout Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ThinkBridge\nERP Importer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Reset / Clear Logs", command=self.clear_logs)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- MAIN AREA ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Step 0: Firebase Key Selection
        self.label_key = ctk.CTkLabel(self.main_frame, text="Step 1: Firebase Configuration", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_key.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.key_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.key_frame.grid(row=1, column=0, padx=20, sticky="ew")

        self.btn_key = ctk.CTkButton(self.key_frame, text="Select Service Key", command=self.select_key, width=150)
        self.btn_key.pack(side="left", padx=(0, 10))
        
        self.lbl_key_path = ctk.CTkLabel(self.key_frame, text="Default: ERP-System/firebase/config/firebase-key.json", text_color="gray")
        self.lbl_key_path.pack(side="left")

        # Step 1: File Selection
        self.label_title = ctk.CTkLabel(self.main_frame, text="Step 2: Select Data Source", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")

        self.tabview = ctk.CTkTabview(self.main_frame, height=80)
        self.tabview.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.tabview.add("Single File")
        self.tabview.add("Batch Folder")

        self.btn_file = ctk.CTkButton(self.tabview.tab("Single File"), text="Browse File...", command=self.select_file)
        self.btn_file.pack(side="left", padx=20, pady=10)
        self.lbl_file_path = ctk.CTkLabel(self.tabview.tab("Single File"), text="No file selected", text_color="gray")
        self.lbl_file_path.pack(side="left", padx=10)

        self.btn_folder = ctk.CTkButton(self.tabview.tab("Batch Folder"), text="Browse Folder...", command=self.select_folder)
        self.btn_folder.pack(side="left", padx=20, pady=10)
        self.lbl_folder_path = ctk.CTkLabel(self.tabview.tab("Batch Folder"), text="No folder selected", text_color="gray")
        self.lbl_folder_path.pack(side="left", padx=10)

        # Step 2: Configuration
        self.label_settings = ctk.CTkLabel(self.main_frame, text="Step 3: Upload Settings", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_settings.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="w")

        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame.grid(row=5, column=0, padx=20, sticky="ew")

        self.entry_collection = ctk.CTkEntry(self.settings_frame, placeholder_text="Collection Name (Leave empty to use Filename)", width=300)
        self.entry_collection.pack(side="left", padx=(0, 20))

        self.check_dupe = ctk.CTkCheckBox(self.settings_frame, text="Store Duplicates (Append All)")
        self.check_dupe.pack(side="left")

        # Step 3: Import Button
        self.btn_start = ctk.CTkButton(self.main_frame, text="🚀 START IMPORT", height=40, font=ctk.CTkFont(size=15, weight="bold"), 
                                       fg_color="#2CC985", hover_color="#229A66", command=self.start_import_thread)
        self.btn_start.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.progressbar = ctk.CTkProgressBar(self.main_frame)
        self.progressbar.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progressbar.set(0)

        # Logs
        self.textbox = ctk.CTkTextbox(self.main_frame, width=500, height=200)
        self.textbox.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(8, weight=1)

        sys.stdout = TextRedirector(self.textbox)
        
        # State Variables
        self.selected_path = None
        self.service_key_path = None  # Default is None (uses backend hardcoded path if not set)
        self.mode = "single" 

    def select_key(self):
        path = filedialog.askopenfilename(title="Select Service Account JSON", filetypes=[("JSON Files", "*.json")])
        if path:
            self.service_key_path = path
            self.lbl_key_path.configure(text=os.path.basename(path), text_color="#2CC985")
            print(f"🔑 Key selected: {path}")

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Data Files", "*.csv *.xlsx *.xls *.pdf")])
        if path:
            self.selected_path = path
            self.mode = "single"
            self.lbl_file_path.configure(text=os.path.basename(path), text_color="white")
            self.lbl_folder_path.configure(text="No folder selected", text_color="gray")
            self.tabview.set("Single File")

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path = path
            self.mode = "batch"
            self.lbl_folder_path.configure(text=path, text_color="white")
            self.lbl_file_path.configure(text="No file selected", text_color="gray")
            self.tabview.set("Batch Folder")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_logs(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")

    def start_import_thread(self):
        if not self.selected_path:
            print("❌ Error: Please select a file or folder first.")
            return
        
        self.btn_start.configure(state="disabled", text="Processing...")
        self.progressbar.start()
        threading.Thread(target=self.run_import_logic, daemon=True).start()

    def run_import_logic(self):
        if not backend:
            print("❌ Backend logic not loaded.")
            self.stop_progress()
            return

        collection_name = self.entry_collection.get().strip()
        store_duplicates = self.check_dupe.get() == 1
        
        try:
            print("\n🔐 Initializing Firestore...")
            
            # KEY LOGIC: Use user-selected key OR default
            final_key_path = self.service_key_path if self.service_key_path else "ERP-System/firebase/config/firebase-key.json"
            
            if not os.path.exists(final_key_path):
                 print(f"❌ Critical Error: Key file not found at: {final_key_path}")
                 self.stop_progress()
                 return

            # Explicitly initialize with the chosen key path
            db = backend.firestore.Client.from_service_account_json(final_key_path)
            print(f"✅ Authenticated using: {os.path.basename(final_key_path)}")
            
            files = []
            if self.mode == "single":
                files.append(self.selected_path)
            else:
                for f in os.listdir(self.selected_path):
                    if f.lower().endswith((".csv", ".xlsx", ".xls", ".pdf")):
                        files.append(os.path.join(self.selected_path, f))

            print(f"📂 Found {len(files)} file(s) to process.")
            
            total_w, total_s, total_f = 0, 0, 0

            for f_path in files:
                if collection_name:
                    coll = collection_name
                else:
                    coll = os.path.splitext(os.path.basename(f_path))[0]
                    coll = re.sub(r'[^a-zA-Z0-9_]', '_', coll)

                ext = os.path.splitext(f_path)[1].lower()
                w, s, f = 0, 0, 0
                
                if ext == ".csv": 
                    w, s, f = backend.import_csv(f_path, db, coll, store_duplicates)
                elif ext in (".xlsx", ".xls"): 
                    w, s, f = backend.import_excel(f_path, db, coll, store_duplicates)
                elif ext == ".pdf": 
                    w, s, f = backend.import_pdf(f_path, db, coll, store_duplicates)
                
                total_w += w
                total_s += s
                total_f += f

            print("\n🎉 DONE!")
            print(f"✔ Total Inserted: {total_w}")
            print(f"⏭ Total Skipped : {total_s}")
            print(f"⚠️ Total Failed  : {total_f}")

        except Exception as e:
            print(f"\n❌ Critical Error: {str(e)}")
        
        finally:
            self.stop_progress()

    def stop_progress(self):
        self.progressbar.stop()
        self.progressbar.set(1)
        self.btn_start.configure(state="normal", text="🚀 START IMPORT")

if __name__ == "__main__":
    app = App()
    app.mainloop()