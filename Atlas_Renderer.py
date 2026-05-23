# -*- coding: utf-8 -*-
import os
import json
import shutil
import traceback

class AtlasRenderer:
    """
    AtlasRenderer v15.6 - Hardened Open-Source Edition
    Genera l'ecosistema AtlasCodex_Viewer riducendo al minimo i file lock di Windows.
    """
    
    @staticmethod
    def write_ecosystem(payload, output_base_path, project_root):
        print(f"DEBUG [Renderer]: Avvio write_ecosystem...")
        print(f"DEBUG [Renderer]: Output richiesto: {output_base_path}")
        
        try:
            # 1. Calcolo percorsi assoluti puliti
            base_dir = os.path.dirname(os.path.abspath(output_base_path))
            data_dir = os.path.join(base_dir, "AtlasCodex_Viewer")
            print(f"DEBUG [Renderer]: Cartella target finale: {data_dir}")
            
            # 2. Creazione forzata senza distruggere la cartella radice per evitare WinError 32
            os.makedirs(data_dir, exist_ok=True)
            
            # Svuota i vecchi file interni in modo tollerante senza rmtree sulla directory principale
            for filename in os.listdir(data_dir):
                file_path = os.path.join(data_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"DEBUG [Renderer] Note: Impossibile eliminare {filename} (in uso), verrà sovrascritto: {e}")
            
            # 3. Individuazione dei sorgenti interni a AtlasCodex
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            localisation_dir = os.path.join(script_dir, "Localisation")
            if not os.path.exists(localisation_dir):
                localisation_dir = os.path.join(script_dir, "Localization")
                
            template_src = os.path.join(script_dir, "AtlasTemplate.html")
            template_dest = os.path.join(data_dir, "index.html")

            # 4. Copia del file d'interfaccia HTML principale
            if not os.path.exists(template_src):
                error_msg = f"File sorgente AtlasTemplate.html non trovato in {script_dir}"
                print(f"DEBUG [Renderer] CRITICAL: {error_msg}")
                return False, error_msg
            
            shutil.copy(template_src, template_dest)
            print("DEBUG [Renderer]: Template index.html copiato.")

            # 5. Copia dei file della matrice lingua
            if os.path.exists(localisation_dir):
                files = [f for f in os.listdir(localisation_dir) if f.endswith(".js")]
                for lang_file in files:
                    src = os.path.join(localisation_dir, lang_file)
                    dest = os.path.join(data_dir, lang_file)
                    shutil.copy(src, dest)
                print(f"DEBUG [Renderer]: Copiati {len(files)} file lingua.")

            # 6. Generazione del Payload Dati strutturato
            json_path = os.path.join(data_dir, "atlas_data.js")
            json_data = json.dumps(payload, indent=4, ensure_ascii=False)
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(f"const AtlasData = {json_data};")
            print("DEBUG [Renderer]: atlas_data.js scritto con successo.")

            return True, data_dir
            
        except Exception as e:
            error_msg = f"Crash Renderer durante la compilazione visiva: {str(e)}\n{traceback.format_exc()}"
            print(f"DEBUG [Renderer] CRITICAL: {error_msg}")
            return False, error_msg