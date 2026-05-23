# -*- coding: utf-8 -*-
import json
import os
import time
from Atlas_Analyzer import AtlasAnalyzer
from Atlas_Renderer import AtlasRenderer
from Atlas_Scanner import AtlasScanner
from Atlas_AI_Analyzer import AtlasAIAnalyzer

class AtlasGenerator:
    """
    AtlasGenerator v17.2 - Dynamic Naming Edition
    Orchestra la pipeline nominando i file di deploy in base al progetto scansionato.
    """
    def __init__(self, project_root, ai_provider_config=None):
        self.project_root = project_root
        self.analyzer = AtlasAnalyzer(self.project_root, ai_provider_config)
        self.snapshots_file = os.path.join(self.project_root, "Memory", "atlas_projects_snapshots.json")

    def generate_atlas(self, source_code_folder, output_html_path, target_lang="IT", project_type="Unity Game", status_callback=None, force_proceed=False):
        
        if project_type == "Unity Game" and os.path.exists(os.path.join(source_code_folder, "Assets")):
            source_code_folder = os.path.join(source_code_folder, "Assets")

        # Estrae il nome pulito della cartella del progetto (es. "Wildroots Project")
        project_name = os.path.basename(os.path.normpath(source_code_folder))
        if not project_name or project_name.lower() in ["assets", "src", "source"]:
            # Se la cartella è generica, prova a prendere il nome del padre
            project_name = os.path.basename(os.path.dirname(os.path.normpath(source_code_folder)))
        
        # Rigenera i nomi dei file di output per renderli unici ed evitare conflitti di cache
        base_output_dir = os.path.dirname(os.path.abspath(output_html_path))
        safe_project_filename = project_name.replace(" ", "_").replace("-", "_")
        
        final_html_name = f"{safe_project_filename}_Architecture_Codex.html"
        output_html_path = os.path.join(base_output_dir, final_html_name)

        if not os.access(os.path.dirname(os.path.abspath(output_html_path)), os.W_OK):
            return False, "Permessi di scrittura negati", False

        project_key = os.path.abspath(source_code_folder)

        # STADIO 1: Scansione Strutturale (Utilizza .atlasignore internamente)
        scanner = AtlasScanner(self.analyzer, source_code_folder, project_type)
        raw_nodes, edges, class_map, current_files_snapshot = scanner.scan_structure(status_callback)

        total_files = len(raw_nodes)
        if total_files == 0: 
            return False, "Nessun file compatibile trovato dopo il filtraggio .atlasignore.", False
        if total_files > 400 and not force_proceed: 
            return False, f"LARGE_PROJECT_WARNING:{total_files}", False

        # Controllo dello Snapshot di Cache
        all_snaps = self._load_all_snapshots()
        if project_key in all_snaps and os.path.exists(output_html_path):
            s = all_snaps[project_key]
            if (s.get("project_type") == project_type and s.get("target_lang") == target_lang and 
                s.get("provider") == self.analyzer.provider_config["provider"] and s.get("files") == current_files_snapshot):
                if status_callback: status_callback("Mappa coerente. Caricata dalla memoria.", 100)
                
                # Calcoliamo la cartella corretta dell'ecosistema per l'apertura
                expected_viewer_dir = os.path.join(base_output_dir, "AtlasCodex_Viewer")
                return True, expected_viewer_dir, False

        # STADIO 2: Analisi AI & Arricchimento delle metriche
        ai_analyzer = AtlasAIAnalyzer(self.analyzer, self.project_root)
        enriched_nodes = ai_analyzer.process_nodes(raw_nodes, target_lang, project_type, status_callback)

        # STADIO 3: Compilazione Ecosistema Visivo
        if status_callback: status_callback("Generazione Ecosistema Visivo in corso...", 95)
        
        payload = {
            "scan_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_name": project_name,
            "language": target_lang,
            "total_scripts": len(enriched_nodes),
            "total_god_objects": sum(1 for n in enriched_nodes if n.get("is_god_object")),
            "total_debt": sum(len(n.get("todos", [])) for n in enriched_nodes),
            "defcon1": sum(1 for n in enriched_nodes if n.get("defcon_level") == 1),
            "defcon2": sum(1 for n in enriched_nodes if n.get("defcon_level") == 2),
            "defcon3": sum(1 for n in enriched_nodes if n.get("defcon_level") == 3),
            "nodes": enriched_nodes, 
            "edges": edges  
        }
        
        success, res_viewer_dir = AtlasRenderer.write_ecosystem(payload, output_html_path, self.project_root)
        
        if success: 
            # FIX PRIVILEGI: Passiamo il nome del file JSON esplicito basato sul progetto anziché la cartella
            specific_json_payload = os.path.join(res_viewer_dir, f"{safe_project_filename}_LLM_Payload.json")
            ai_analyzer.export_llm_payload_direct(enriched_nodes, specific_json_payload, project_type)
            
            all_snaps[project_key] = {
                "source_path": source_code_folder, "project_type": project_type, "target_lang": target_lang,
                "provider": self.analyzer.provider_config["provider"], "model": self.analyzer.provider_config["model"],
                "output_html_path": res_viewer_dir, "files": current_files_snapshot
            }
            with open(self.snapshots_file, 'w', encoding='utf-8') as f: json.dump(all_snaps, f, indent=4)

        return success, res_viewer_dir, True

    def _load_all_snapshots(self):
        if os.path.exists(self.snapshots_file):
            try:
                with open(self.snapshots_file, 'r', encoding='utf-8') as f: return json.load(f)
            except: pass
        return {}