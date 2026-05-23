# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
import logging

# =====================================================================
# 🪐 ATOMIZZAZIONE DEL PERCORSO DI RUNTIME & ENVIRONMENT INIT
# =====================================================================
# Individua la cartella fisica in cui risiede main.py
base_directory = os.path.dirname(os.path.abspath(__file__))

# Forza il sistema operativo a considerare questa cartella come directory operativa
os.chdir(base_directory)

# Inietta la cartella root nel percorso di ricerca di Python
if base_directory not in sys.path:
    sys.path.insert(0, base_directory)

# =====================================================================
# CHECK INTEGRITÀ STRUTTURA (Pre-flight check)
# =====================================================================
def check_environment():
    """Verifica che la struttura dei plugin sia integra prima dell'avvio."""
    processors_path = os.path.join(base_directory, "processors")
    init_file = os.path.join(processors_path, "__init__.py")
    
    if not os.path.exists(processors_path):
        print(f"❌ CRITICAL ERROR: Directory 'processors' non trovata in {base_directory}")
        return False
    if not os.path.exists(init_file):
        print(f"⚠️ ATTENZIONE: File 'processors/__init__.py' mancante. Creazione automatica...")
        try:
            with open(init_file, 'w') as f: pass
        except Exception as e:
            print(f"❌ Errore critico creazione __init__.py: {e}")
            return False
    return True

# =====================================================================
# AVVIO INTERFACCIA GRAFICA CENTRALIZZATA
# =====================================================================
if __name__ == "__main__":
    if check_environment():
        try:
            # Import differito per evitare crash precoci durante il setup
            from Atlas_UI import AtlasAppUI
            
            main_window = tk.Tk()
            # Istanzia l'interfaccia utente
            app = AtlasAppUI(main_window)
            # Avvia il loop grafico
            main_window.mainloop()
            
        except Exception as e:
            print(f"💥 ERRORE DURANTE L'AVVIO DELL'APPLICAZIONE:\n{e}")
            input("Premi INVIO per chiudere...")
            sys.exit(1)
    else:
        input("Setup fallito. Premi INVIO per chiudere...")
        sys.exit(1)