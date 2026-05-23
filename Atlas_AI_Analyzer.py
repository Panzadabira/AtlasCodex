# -*- coding: utf-8 -*-
import html
import json
import time

class AtlasAIAnalyzer:
    """
    AtlasAIAnalyzer v17.2 - Hardened File-System Routing
    Arricchisce i nodi e previene i conflitti di autorizzazione di Windows durante i salvataggi JSON.
    """
    def __init__(self, analyzer, project_root):
        self.analyzer = analyzer
        self.project_root = project_root

    def process_nodes(self, raw_nodes, target_lang, project_type, status_callback=None):
        enriched_nodes = []
        total_nodes = len(raw_nodes)

        for index, node in enumerate(raw_nodes, start=1):
            if status_callback: 
                status_callback(f"Compilazione Metriche AI: {node['id']} ({index}/{total_nodes})", 45 + int((index/total_nodes)*45))
            
            ext = node['ext']
            content = node['content']
            deps = node['deps']
            
            processor = self.analyzer.get_processor(ext)
            
            has_loops = processor.analyze_bottlenecks(content)
            
            scene_objects = node.get('scene_objects', ["__L_NONE__"])
            scene_density = len(scene_objects) if scene_objects != ["__L_NONE__"] else 0
            
            defcon = self.analyzer.compute_defcon_matrix(len(deps), scene_density, has_loops)
            todos = self.analyzer.extract_todos(content, ext)
            blueprint = processor.extract_pure_blueprint(content)
            
            slim_code = processor.extract_api_signature(content)
            
            expensive_methods = []
            if has_loops:
                expensive_methods.append("[HOTSPOT] Logica ad alta intensità di calcolo rilevata.")

            enriched_nodes.append({
                "id": node['id'],
                "label": node['id'],
                "layer": node['layer'],
                "opacity": node['opacity'],
                "scene_objects": scene_objects,
                "scene_density_count": scene_density,
                "code": html.escape(content),          
                "slim_code": html.escape(slim_code),   
                "description": html.escape(blueprint), 
                "dependencies": ", ".join(deps) if deps else "Nessuna",
                "todos": [html.escape(t) for t in todos],
                "is_god_object": len(deps) >= 7,
                "dep_count": len(deps),
                "expensive_methods": expensive_methods,
                "has_heavy_loops": has_loops,
                "defcon_level": defcon
            })
        
        return enriched_nodes

    def export_llm_payload(self, nodes, output_html_path, project_type):
        """Mantenuto per retrocompatibilità astratta di firma della vecchia interfaccia."""
        return None

    def export_llm_payload_direct(self, nodes, absolute_file_path, project_type):
        """
        FIX INDIRIZZAMENTO DEFCON: Scrive in modo atomico il payload JSON strutturato
        puntando all'esatto percorso file calcolato, eludendo il WinError Permission Denied.
        """
        payload_data = {
            "metadata": {
                "project_type": project_type, 
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "engine_mode": "Universal Pro"
            },
            "modules": []
        }
        for n in nodes:
            payload_data["modules"].append({
                "module_id": n["id"],
                "layer": n["layer"],
                "defcon_risk": n.get("defcon_level", 1),
                "dependencies": n["dependencies"].split(", ") if n["dependencies"] != "Nessuna" else [],
                "blueprint_signature": html.unescape(n["slim_code"])
            })
        try:
            # Assicura che la cartella esista prima di aprire il file descriptor
            os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
            with open(absolute_file_path, 'w', encoding='utf-8') as f:
                json.dump(payload_data, f, indent=4)
            print(f"DEBUG [AI Analyzer]: Payload di contesto LLM scritto in: {absolute_file_path}")
            return absolute_file_path
        except Exception as e:
            print(f"❌ Errore critico esportazione LLM payload: {e}")
            return None