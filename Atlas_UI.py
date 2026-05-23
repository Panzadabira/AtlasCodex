# -*- coding: utf-8 -*-
import os
import json
import sys
import logging
import traceback
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import subprocess
import shutil
import http.server
import socketserver

# =====================================================================
# 🛡️ PROTEZIONE LIVELLO 0: CRASH JOURNAL ATTIVATO ALL'INIZIO ASSOLUTO
# =====================================================================
LOG_FILE = "atlas_engine_errors.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def global_exception_handler(exctype, value, tb):
    """Cattura qualsiasi anomalia, inclusi gli errori di importazione iniziali."""
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    logging.error(f"⚠️ CRASH CRITICO INIZIALE:\n{error_msg}\n" + "="*60)
    print(f"\n💥 DETTAGLIO CRASH INTERCETTATO:\n{error_msg}")
    try:
        root_hidden = tk.Tk()
        root_hidden.withdraw()
        messagebox.showerror(
            "Errore Avvio Applicazione / Application Startup Error",
            f"Impossibile avviare il motore.\n\nControlla il file log per i dettagli:\n{os.path.abspath(LOG_FILE)}"
        )
    except Exception:
        pass
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler

try:
    from Atlas_Generator import AtlasGenerator
    from Atlas_Localization import LOCALIZATION_MATRIX
except ImportError as e:
    logging.error(f"❌ MODULO MANCANTE DI BACKEND: {e}. Controlla la presenza dei file nella radice.")
    raise

_GLOBAL_SERVER = None
_GLOBAL_PORT = 8000

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def _run_local_server(directory_to_serve, port):
    global _GLOBAL_SERVER
    handler = http.server.SimpleHTTPRequestHandler
    
    class SubFolderHandler(handler):
        def translate_path(self, path):
            rel_path = path.lstrip('/')
            return os.path.join(directory_to_serve, rel_path)
            
        def log_message(self, format, *args):
            pass

    try:
        _GLOBAL_SERVER = ThreadedHTTPServer(("127.0.0.1", port), SubFolderHandler)
        print(f"DEBUG [Server]: Local Server attivato su http://127.0.0.1:{port}")
        _GLOBAL_SERVER.serve_forever()
    except Exception as e:
        print(f"DEBUG [Server]: Nota di runtime porta {port}: {e}")

class AtlasAppUI:
    """
    AtlasAppUI v5.6 - Fully Automated Launch Suite
    Assicura la persistenza cromatica delle tendine e forza l'apertura automatica del browser.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("PanzaScope - Project Configuration Hub")
        
        try:
            self.root.state('zoomed')
        except Exception:
            self.root.geometry("1024x768")
        
        self.root.report_callback_exception = self._tk_exception_handler
        self.config_file = "atlas_gui_config.json"
        self.app_root = os.path.dirname(os.path.abspath(__file__))
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_cleanup)
        
        self.memory_dir = os.path.join(self.app_root, "Memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.snapshots_file = os.path.join(self.memory_dir, "atlas_projects_snapshots.json")

        self.bg_main = "#0d1117"
        self.bg_panel = "#161b22"
        self.fg_light = "#c9d1d9"
        self.fg_green = "#58a6ff"
        self.btn_green = "#238636"
        self.btn_text = "#ffffff"
        
        self.root.configure(bg=self.bg_main)
        
        # FIX CROMATICO: Mantiene il testo leggibile, fisso e nitido anche in stato Readonly
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.bg_main, foreground=self.fg_light)
        self.style.configure("TLabel", background=self.bg_main, foreground=self.fg_light, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=self.bg_main, foreground=self.btn_green, font=("Segoe UI", 16, "bold"))
        self.style.configure("TEntry", fieldbackground=self.bg_panel, foreground=self.fg_light, bordercolor="#30363d")
        
        self.style.configure("TCombobox", 
                             fieldbackground=self.bg_panel, 
                             foreground=self.fg_light, 
                             background=self.bg_panel, 
                             bordercolor="#30363d", 
                             arrowcolor=self.fg_green)
                             
        self.style.map("TCombobox", 
                       fieldbackground=[("readonly", self.bg_panel), ("disabled", self.bg_main)],
                       foreground=[("readonly", self.fg_light), ("disabled", "#8b949e")],
                       selectbackground=[("readonly", self.bg_panel)],
                       selectforeground=[("readonly", self.fg_light)])
                       
        self.style.configure("Horizontal.TProgressbar", background=self.btn_green, troughcolor=self.bg_panel, bordercolor="#30363d")
        
        self.source_type_var = tk.StringVar(value="Locale")
        self.source_path_var = tk.StringVar()
        self.project_type_var = tk.StringVar(value="Rilevamento Automatico")
        self.lang_var = tk.StringVar(value="EN")
        self.provider_var = tk.StringVar(value="none (pure logic)")
        self.model_var = tk.StringVar(value="offline_parser")
        self.url_var = tk.StringVar(value="local")
        self.api_key_var = tk.StringVar()
        
        self.status_msg_var = tk.StringVar()
        self.progress_val_var = tk.DoubleVar(value=0.0)

        self._build_ui()
        self._load_saved_config()
        self._retranslate_ui_dynamic()
        
        self.source_path_var.trace_add("write", self._on_source_path_auto_detect)
        
        self.source_type_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.project_type_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.lang_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.provider_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.model_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.url_var.trace_add("write", lambda *args: self._auto_save_current_state())
        self.api_key_var.trace_add("write", lambda *args: self._auto_save_current_state())

    def _tk_exception_handler(self, exctype, value, tb):
        error_msg = "".join(traceback.format_exception(exctype, value, tb))
        logging.error(f"💥 ERRORE INTERFACCIA UTENTE (UI):\n{error_msg}\n" + "="*60)

    def _load_saved_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.source_type_var.set(data.get("source_type", "Locale"))
                    self.source_path_var.set(data.get("source_path", ""))
                    self.project_type_var.set(data.get("project_type", "Rilevamento Automatico"))
                    self.lang_var.set(data.get("lang", "EN"))
                    self.provider_var.set(data.get("provider", "none (pure logic)"))
                    self.model_var.set(data.get("model", "offline_parser"))
                    self.url_var.set(data.get("url", "local"))
                    self.api_key_var.set(data.get("api_key", ""))
            except Exception:
                pass

    def _save_current_config(self):
        data = {
            "source_type": self.source_type_var.get(),
            "source_path": self.source_path_var.get(),
            "project_type": self.project_type_var.get(),
            "lang": self.lang_var.get(),
            "provider": self.provider_var.get(),
            "model": self.model_var.get(),
            "url": self.url_var.get(),
            "api_key": self.api_key_var.get()
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def _on_source_path_auto_detect(self, *args):
        folder_path = self.source_path_var.get().strip()
        if not folder_path or not os.path.exists(folder_path):
            return
        abs_key = os.path.abspath(folder_path)
        
        if os.path.exists(self.snapshots_file):
            try:
                with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                    snapshots = json.load(f)
                if abs_key in snapshots:
                    snap = snapshots[abs_key]
                    self.project_type_var.set(snap.get("project_type", "Rilevamento Automatico"))
                    self.lang_var.set(snap.get("target_lang", "EN"))
                    self.provider_var.set(snap.get("provider", "none (pure logic)"))
                    self.model_var.set(snap.get("model", "offline_parser"))
                    self.url_var.set(snap.get("url", "local"))
                    self.api_key_var.set(snap.get("api_key", ""))
                    self._on_provider_change()
                    self._retranslate_ui_dynamic()
                    
                    lex = LOCALIZATION_MATRIX.get(self.lang_var.get().upper(), LOCALIZATION_MATRIX["EN"])
                    self.status_msg_var.set(lex.get("UI_STATUS_RECOGNIZED", "").format(folder_path))
            except Exception as e:
                logging.error(f"Errore auto-matching cache: {e}")

    def _auto_save_current_state(self):
        if not hasattr(self, 'snapshots_file') or not hasattr(self, 'ent_model'):
            return
            
        self._save_current_config()
        
        folder_path = self.source_path_var.get().strip()
        if folder_path and os.path.exists(folder_path):
            abs_key = os.path.abspath(folder_path)
            try:
                snapshots = {}
                if os.path.exists(self.snapshots_file):
                    with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                        snapshots = json.load(f)
                
                if abs_key not in snapshots:
                    snapshots[abs_key] = {}
                    
                snapshots[abs_key]["source_path"] = folder_path
                snapshots[abs_key]["project_type"] = self.project_type_var.get()
                snapshots[abs_key]["target_lang"] = self.lang_var.get()
                snapshots[abs_key]["provider"] = self.provider_var.get()
                snapshots[abs_key]["model"] = self.model_var.get()
                snapshots[abs_key]["url"] = self.url_var.get()
                snapshots[abs_key]["api_key"] = self.api_key_var.get()
                if "files" not in snapshots[abs_key]:
                    snapshots[abs_key]["files"] = {}
                    
                with open(self.snapshots_file, 'w', encoding='utf-8') as f:
                    json.dump(snapshots, f, indent=4)
            except Exception as e:
                logging.error(f"Errore durante l'auto-salvataggio reattivo: {e}")

    def _retranslate_ui_dynamic(self, event=None):
        lang = self.lang_var.get().upper()
        lex = LOCALIZATION_MATRIX.get(lang, LOCALIZATION_MATRIX["EN"])
        
        self.header.pack_forget()
        self.header.config(text=lex.get("UI_HEADER", ""))
        self.header.pack(pady=10)
        
        self.src_frame.config(text=lex.get("UI_SRC_FRAME", ""))
        self.lbl_src_type.config(text=lex.get("UI_SRC_TYPE", ""))
        self.lbl_proj_type.config(text=lex.get("UI_PROJ_TYPE", ""))
        self.browse_btn.config(text=lex.get("UI_BROWSE", ""))
        self.meta_frame.config(text=lex.get("UI_ENGINE_FRAME", ""))
        self.lbl_motor.config(text=lex.get("UI_MOTOR", ""))
        self.lbl_model.config(text=lex.get("UI_MODEL", ""))
        self.lbl_url.config(text=lex.get("UI_URL", ""))
        self.lbl_key.config(text=lex.get("UI_KEY", ""))
        self.lang_frame.config(text=lex.get("UI_LANG_FRAME", ""))
        self.lbl_lang_select.config(text=lex.get("UI_LANG_LABEL", ""))
        self.progress_frame.config(text=lex.get("UI_STATUS_FRAME", ""))
        self.footer.config(text=lex.get("UI_FOOTER", ""))
        
        self._on_source_type_change()
        
        if self.run_btn.cget("state") == "normal":
            self.run_btn.config(text=lex.get("UI_RUN_BTN", ""))
            if not self.source_path_var.get().strip():
                self.status_msg_var.set(lex.get("UI_STATUS_READY", ""))

    def _build_ui(self):
        main_container = tk.Frame(self.root, bg=self.bg_main)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=740, height=660)

        self.header = ttk.Label(main_container, text="", style="Header.TLabel")
        self.header.pack(pady=10)

        # 📂 AREA SORGENTE E CONTESTO ARCHITETTURALE
        self.src_frame = tk.LabelFrame(main_container, text="", bg=self.bg_main, fg=self.fg_green, font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
        self.src_frame.pack(fill="x", pady=10, ipady=12)

        self.lbl_src_type = ttk.Label(self.src_frame, text="")
        self.lbl_src_type.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        type_combo = ttk.Combobox(self.src_frame, textvariable=self.source_type_var, values=["Locale", "Git Repository"], width=15, state="readonly")
        type_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        type_combo.bind("<<ComboboxSelected>>", self._on_source_type_change)

        self.lbl_proj_type = ttk.Label(self.src_frame, text="")
        self.lbl_proj_type.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        
        proj_values = ["Rilevamento Automatico", "Unity Game", "Multi-Agent AI", "Unreal / Godot Engine", "Enterprise Backend (Java/C++)", "Web Application (JS/HTML/CSS)"]
        proj_combo = ttk.Combobox(self.src_frame, textvariable=self.project_type_var, values=proj_values, width=22, state="readonly")
        proj_combo.grid(row=0, column=3, sticky="w", padx=10, pady=5)

        self.path_label = ttk.Label(self.src_frame, text="")
        self.path_label.grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.path_entry = ttk.Entry(self.src_frame, textvariable=self.source_path_var, width=46)
        self.path_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=8, sticky="ew")
        self.browse_btn = tk.Button(self.src_frame, text="", bg=self.bg_panel, fg=self.fg_light, activebackground="#21262d", activeforeground="white", bd=1, relief="solid", cursor="hand2", command=self._browse_source)
        self.browse_btn.grid(row=1, column=3, padx=10, pady=8)

        # 🧠 AREA CONFIGURAZIONE ENGINE
        self.meta_frame = tk.LabelFrame(main_container, text="", bg=self.bg_main, fg=self.fg_green, font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
        self.meta_frame.pack(fill="x", pady=10, ipady=8)

        self.lbl_motor = ttk.Label(self.meta_frame, text="")
        self.lbl_motor.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        prov_combo = ttk.Combobox(self.meta_frame, textvariable=self.provider_var, values=["none (pure logic)", "ollama", "openai", "gemini", "claude", "groq"], width=18, state="readonly")
        prov_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        prov_combo.bind("<<ComboboxSelected>>", self._on_provider_change)

        self.lbl_model = ttk.Label(self.meta_frame, text="")
        self.lbl_model.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.ent_model = ttk.Entry(self.meta_frame, textvariable=self.model_var, width=22)
        self.ent_model.grid(row=0, column=3, sticky="w", padx=10, pady=5)

        self.lbl_url = ttk.Label(self.meta_frame, text="")
        self.lbl_url.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.ent_url = ttk.Entry(self.meta_frame, textvariable=self.url_var, width=24)
        self.ent_url.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.lbl_key = ttk.Label(self.meta_frame, text="")
        self.lbl_key.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.ent_key = ttk.Entry(self.meta_frame, textvariable=self.api_key_var, width=62, show="*")
        self.ent_key.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=5)

        # 🌍 AREA LOCALIZZAZIONE GLOBALE DI SISTEMA
        self.lang_frame = tk.LabelFrame(main_container, text="", bg=self.bg_main, fg=self.fg_green, font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
        self.lang_frame.pack(fill="x", pady=10, ipady=8)
        
        self.lbl_lang_select = ttk.Label(self.lang_frame, text="")
        self.lbl_lang_select.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        lang_combo_box = ttk.Combobox(self.lang_frame, textvariable=self.lang_var, values=["EN", "IT", "DE", "FR", "ES", "RU", "ZH"], width=12, state="readonly")
        lang_combo_box.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        lang_combo_box.bind("<<ComboboxSelected>>", self._retranslate_ui_dynamic)

        # 📊 AREA STATO PROGRESSO
        self.progress_frame = tk.LabelFrame(main_container, text="", bg=self.bg_main, fg=self.fg_green, font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
        self.progress_frame.pack(fill="x", pady=5, ipady=8)

        self.lbl_status = ttk.Label(self.progress_frame, textvariable=self.status_msg_var, font=("Segoe UI", 9, "italic"), foreground="#8b949e")
        self.lbl_status.pack(anchor="w", padx=10, pady=2)

        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_val_var, maximum=100, style="Horizontal.TProgressbar", mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=5)

        # PULSANTE DI CONFIGURAZIONE
        self.run_btn = tk.Button(main_container, text="", bg=self.btn_green, fg=self.btn_text, font=("Segoe UI", 11, "bold"), activebackground="#2ea043", activeforeground="white", bd=0, cursor="hand2", command=self._start_async_generation)
        self.run_btn.pack(fill="x", pady=15, ipady=12)

        self.footer = ttk.Label(main_container, text="", font=("Segoe UI", 8, "italic"))
        self.footer.pack(side="bottom", pady=5)

    def _on_source_type_change(self, event=None):
        lang = self.lang_var.get().upper()
        lex = LOCALIZATION_MATRIX.get(lang, LOCALIZATION_MATRIX["EN"])
        if self.source_type_var.get() == "Locale":
            self.path_label.config(text=lex.get("UI_PATH_FOLDER", "Project Folder Path:"))
            self.browse_btn.grid()
        else:
            self.path_label.config(text=lex.get("UI_PATH_GIT", "Git Repository URL:"))
            self.browse_btn.grid_remove()

    def _on_provider_change(self, event=None):
        if not hasattr(self, 'ent_model'): return
        state = "disabled" if "none" in self.provider_var.get().lower() else "normal"
        self.ent_model.config(state=state); self.ent_url.config(state=state); self.ent_key.config(state=state)

    def _browse_source(self):
        directory = filedialog.askdirectory(title="Select code repository folder")
        if directory:
            self.source_path_var.set(os.path.normpath(directory))

    def _start_async_generation(self):
        raw_source = self.source_path_var.get().strip()
        if not raw_source: return
        self.run_btn.config(state="disabled", text="⚡ HOT-RELOAD RUNNING...")
        self._save_current_config()
        threading.Thread(target=self._async_worker_pipeline, args=(raw_source,), daemon=True).start()

    def _safe_update_ui(self, msg, value):
        self.root.after(0, lambda: self.status_msg_var.set(msg))
        self.root.after(0, lambda: self.progress_val_var.set(value))

    def _async_worker_pipeline(self, raw_source):
        global _GLOBAL_SERVER, _GLOBAL_PORT
        source_type, project_context = self.source_type_var.get(), self.project_type_var.get()
        scan_target_dir = raw_source if source_type == "Locale" else os.path.join(self.app_root, "Atlas_Workspace")
        final_html_output = os.path.join(scan_target_dir, "Atlas_Architecture_Codex.html") if source_type == "Locale" else os.path.join(self.app_root, "Atlas_Git_Codex.html")

        if source_type != "Locale":
            scan_target_dir = self._handle_git_cloning(raw_source)
            if not scan_target_dir: return self._reset_run_button()

        ai_config = {"provider": self.provider_var.get().lower(), "model": self.model_var.get().strip(), "url": self.url_var.get().strip(), "api_key": self.api_key_var.get().strip()}
        generator = AtlasGenerator(project_root=self.app_root, ai_provider_config=ai_config)
        
        force_proceed = False
        while True:
            success, result_path, was_updated = generator.generate_atlas(
                source_code_folder=scan_target_dir, output_html_path=final_html_output,
                target_lang=self.lang_var.get(), project_type=project_context,
                status_callback=lambda txt, val: self._safe_update_ui(txt, val), force_proceed=force_proceed
            )
            
            # POPUP DETTAGLIATO PROGETTI GRANDI / FILE INUTILI
            if not success and str(result_path).startswith("LARGE_PROJECT_WARNING:"):
                num_files = result_path.split(":")[1]
                user_approval = []
                
                def ask_confirmation():
                    is_it = self.lang_var.get().upper() == "IT"
                    t = "Avviso Dimensioni Progetto" if is_it else "Project Scale Warning"
                    
                    m = (
                        f"⚠️ ATTENZIONE: Sono stati rilevati {num_files} file scansionabili.\n\n"
                        "La cartella selezionata potrebbe contenere file non necessari o elementi estranei "
                        "che rallenteranno drasticamente le prestazioni del software.\n\n"
                        "Consiglio: Seleziona una sottocartella più mirata (es. solo 'Assets' o la directory dei moduli core).\n\n"
                        "Vuoi procedere comunque con l'analisi completa di tutti i file? Richiederà più tempo."
                    ) if is_it else (
                        f"⚠️ WARNING: {num_files} scannable files detected.\n\n"
                        "The selected folder may contain excessive non-essential or untracked files "
                        "that will severely reduce visualization and rendering performance.\n\n"
                        "Recommendation: Select a more focused subfolder (e.g., core modules only).\n\n"
                        "Do you want to proceed with the entire codebase anyway? This will take significantly longer."
                    )
                    user_approval.append(messagebox.askyesno(t, m))
                
                self.root.after(0, ask_confirmation)
                while not user_approval: time.sleep(0.1)
                
                if user_approval[0]:
                    force_proceed = True
                    continue
                else:
                    self._safe_update_ui("Mappatura interrotta per salvaguardia prestazioni.", 0)
                    return self._reset_run_button()
            break

        # AUTOMAZIONE COMPLETA: Avvia il server e lancia in automatico il browser all'indirizzo sicuro HTTP
        if success:
            viewer_directory = os.path.abspath(result_path)
            
            if _GLOBAL_SERVER is None:
                server_thread = threading.Thread(target=_run_local_server, args=(viewer_directory, _GLOBAL_PORT), daemon=True)
                server_thread.start()
                time.sleep(0.5)  # Tempo di aggancio del socket

            # Forza l'apertura automatica del browser sulla porta locale anti-CORS
            webbrowser.open(f"http://127.0.0.1:{_GLOBAL_PORT}/index.html")
            self._safe_update_ui("Ecosistema visivo generato e aperto in automatico via HTTP.", 100)

        self._reset_run_button()

    def _reset_run_button(self):
        self.root.after(0, self._retranslate_ui_dynamic)
        self.root.after(0, lambda: self.run_btn.config(state="normal"))

    def _handle_git_cloning(self, git_url):
        workspace_dir = os.path.join(self.app_root, "Atlas_Workspace")
        if os.path.exists(workspace_dir):
            try: shutil.rmtree(workspace_dir)
            except Exception: pass
        os.makedirs(workspace_dir, exist_ok=True)
        try:
            subprocess.run(["git", "clone", git_url, workspace_dir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return workspace_dir
        except Exception: return None

    def _on_close_cleanup(self):
        global _GLOBAL_SERVER
        if _GLOBAL_SERVER is not None:
            print("DEBUG [Server]: Spegnimento del server HTTP locale...")
            _GLOBAL_SERVER.shutdown()
            _GLOBAL_SERVER.server_close()
        self.root.destroy()

if __name__ == "__main__":
    main_window = tk.Tk()
    app = AtlasAppUI(main_window)
    main_window.mainloop()