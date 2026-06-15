# -*- coding: utf-8 -*-
import os
import re
import time
import fnmatch

class AtlasScanner:
    """
    AtlasScanner v16.8 - Modulo Operativo Stadio 1 (Ignore-Aware & UI-Override)
    Mappa il filesystem escludendo i pattern dichiarati in .atlasignore, blinda
    l'analisi ignorando l'ecosistema di rendering, e forza i file visivi a L4.
    """
    def __init__(self, analyzer, source_code_folder, project_type):
        self.analyzer = analyzer
        self.source_code_folder = source_code_folder
        self.project_type = project_type
        self.scene_ref_db = {}
        
        # Include esplicitamente estensioni web/UI per consentire il rilevamento 
        # anche se non hanno un processore dedicato (sfruttando il .generic)
        base_extensions = list(self.analyzer.processors.keys())
        for ext in [".html", ".uxml", ".uss", ".css"]:
            if ext not in base_extensions:
                base_extensions.append(ext)
        self.supported_extensions = tuple(base_extensions)
        
        self.ignore_patterns = self._load_atlasignore()

    def _load_atlasignore(self):
        """Carica i pattern da un file .atlasignore se presente, altrimenti usa regole di fallback."""
        ignore_path = os.path.join(self.source_code_folder, ".atlasignore")
        patterns = [
            "*.git*", "*node_modules*", "*bin*", "*obj*", "*library*",
            "*memory*", "*atlascodex_viewer*", "*_llm_payload.json*", "*.log"
        ]
        
        if os.path.exists(ignore_path):
            try:
                with open(ignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Normalizza le cartelle per il matching flessibile
                            if line.endswith("/"):
                                line = line[:-1]
                            patterns.append(f"*{line}*")
            except Exception as e:
                print(f"⚠️ Impossibile leggere .atlasignore, uso i fallback di sicurezza: {e}")
        else:
            # Crea un file .atlasignore di cortesia se manca
            try:
                with open(ignore_path, 'w', encoding='utf-8') as f:
                    f.write("# .atlasignore - Configurazione di esclusione per Atlas Codex\n")
                    f.write("memory/\natlascodex_viewer/\n*.log\nnode_modules/\nbin/\nobj/\n")
            except:
                pass
        return list(set(patterns))

    def _is_ignored(self, path):
        """Verifica se il percorso corrisponde a uno dei pattern di esclusione."""
        normalized_path = path.replace(os.sep, "/").lower()
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(normalized_path, pattern.lower()):
                return True
        return False

    def parse_unity_scene_hierarchy(self, assets_path, status_callback=None):
        guid_to_classname = {}
        for root, _, files in os.walk(assets_path):
            if self._is_ignored(root): continue
            
            # Salto di sicurezza esplicito per la cartella di output
            if "atlascodex_viewer" in root.lower() or "memory" in root.lower():
                continue
                
            for file in files:
                if self._is_ignored(os.path.join(root, file)): continue
                if file.endswith(".cs.meta"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            guid_match = re.search(r"guid:\s*([a-f0-9]{32})", f.read())
                        if guid_match: 
                            name_no_ext = file.replace(".cs.meta", "")
                            if name_no_ext: guid_to_classname[guid_match.group(1)] = name_no_ext
                    except: pass
        
        for root, _, files in os.walk(assets_path):
            if self._is_ignored(root): continue
            if "atlascodex_viewer" in root.lower() or "memory" in root.lower():
                continue
            if any(ex in os.path.split(root) for ex in ["Plugins", "Resources", "Editor"]): continue
            for file in files:
                if self._is_ignored(os.path.join(root, file)): continue
                if file.endswith((".unity", ".prefab")):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
                        for guid, classname in guid_to_classname.items():
                            if guid in content:
                                if classname not in self.scene_ref_db: self.scene_ref_db[classname] = []
                                r = f"{os.path.basename(file)} (Istanziato)"
                                if r not in self.scene_ref_db[classname]: self.scene_ref_db[classname].append(r)
                    except: pass

    def _calculate_freshness(self, filepath):
        if not filepath or not os.path.exists(filepath): return 1.0
        try:
            days_old = (time.time() - os.path.getmtime(filepath)) / (24 * 3600)
            if days_old < 7: return 1.0
            if days_old < 30: return 0.8
            if days_old < 90: return 0.6
            return 0.3
        except: return 1.0

    def scan_structure(self, status_callback=None):
        scanned_files, class_map, current_files_snapshot = [], {}, {}
        
        for root, _, files in os.walk(self.source_code_folder):
            # 1. PROTEZIONE DI LIVELLO 1: Esclusione deterministica basata sui segmenti di percorso relativi
            rel_root = os.path.relpath(root, self.source_code_folder)
            rel_segments = [seg.lower() for seg in rel_root.split(os.sep)]
            
            if any(ex in rel_segments for ex in ["atlascodex_viewer", "memory", "plugins", "resources", ".git", "node_modules", "bin", "obj", "library", "temp"]): 
                continue
            
            # 2. PROTEZIONE DI LIVELLO 2: Controllo tramite .atlasignore
            if self._is_ignored(root): 
                continue
                
            for file in files:
                # 3. PROTEZIONE DI LIVELLO 3: Esclusione file critici di configurazione e script di visualizzazione distribuiti
                if file.lower() in ["atlas_data.js", "atlas_gui_config.json", "atlas_engine_errors.log", "atlas_gui_config.json.bak"]:
                    continue
                
                # Impedisce l'auto-mappatura delle traduzioni locali e file JS del viewer se eseguiti nella stessa radice
                if file.lower() in ["en.js", "it.js", "de.js", "fr.js", "es.js", "ru.js", "zh.js", "ja.js"]:
                    continue
                    
                full_p = os.path.join(root, file)
                if self._is_ignored(full_p): 
                    continue
                    
                if file.endswith(self.supported_extensions):
                    rel_p = os.path.relpath(full_p, self.source_code_folder)
                    class_map[os.path.splitext(file)[0]] = file
                    scanned_files.append((file, rel_p, full_p))
                    current_files_snapshot[rel_p] = os.path.getmtime(full_p)

        total_files = len(scanned_files)
        if total_files == 0: return [], [], {}, current_files_snapshot

        if self.project_type == "Unity Game": 
            self.parse_unity_scene_hierarchy(self.source_code_folder, status_callback)

        raw_nodes = []
        edges = []

        for index, (file, rel_p, full_p) in enumerate(scanned_files, start=1):
            if status_callback: status_callback(f"Scansione Strutturale: {file} ({index}/{total_files})", 15 + int((index/total_files)*30))
            
            try:
                with open(full_p, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
            except: continue

            ext = os.path.splitext(file)[1].lower()
            processor = self.analyzer.get_processor(ext)
            
            deps = processor.extract_dependencies(content, class_map, os.path.splitext(file)[0])
            layer = processor.identify_layer(file, rel_p, content)
            
            # ---------------------------------------------------------
            # OVERRIDE FORZATO: Assegna sempre L4 ai formati UI/Visivi
            # ---------------------------------------------------------
            if ext in [".html", ".uxml", ".uss", ".css"]:
                layer = "L4"
            
            raw_nodes.append({
                "id": file,
                "rel_path": rel_p,
                "full_path": full_p,
                "ext": ext,
                "content": content,
                "layer": layer,
                "deps": deps,
                "opacity": self._calculate_freshness(full_p),
                "scene_objects": self.scene_ref_db.get(os.path.splitext(file)[0], ["__L_NONE__"])
            })

            for dep in deps: 
                edges.append({"from": file, "to": dep})

        return raw_nodes, edges, class_map, current_files_snapshot