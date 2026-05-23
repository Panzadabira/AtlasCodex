# -*- coding: utf-8 -*-
import importlib
import pkgutil
import processors
import os
import hashlib
import json
import requests
import re

class AtlasAnalyzer:
    """
    AtlasAnalyzer v16.1 - Engine Core Modulare (Puro Orchestratore)
    Carica i processori, gestisce la cache e smista le richieste di analisi.
    """
    def __init__(self, project_root, ai_provider_config=None):
        self.project_root = project_root
        self.cache_path = os.path.join(project_root, "Memory", ".atlas_codex_cache.json")
        self.provider_config = ai_provider_config or {
            "provider": "none", "api_key": "", "model": "offline", "url": "local"
        }
        self.processors = {}
        self.cache = {}
        
        self._load_plugins()
        self._load_cache()

    def _load_plugins(self):
        if not hasattr(processors, '__path__'):
            print("ERRORE: La cartella 'processors' deve contenere un file __init__.py")
            return

        for loader, name, is_pkg in pkgutil.iter_modules(processors.__path__):
            if name == "base": continue 
            try:
                module = importlib.import_module(f"processors.{name}")
                if hasattr(module, 'register'):
                    self.processors.update(module.register())
            except Exception as e:
                print(f"DEBUG: Impossibile caricare il plugin {name}: {e}")
        
        print(f"DEBUG: Plugin caricati correttamente: {list(self.processors.keys())}")

    def get_processor(self, ext):
        """Restituisce il processore specifico, o usa il generic come fallback."""
        # Se .generic non è registrato per qualche motivo, istanzia la base dinamicamente.
        if '.generic' not in self.processors:
            from processors.base import BaseLanguageProcessor
            return self.processors.get(ext.lower(), BaseLanguageProcessor())
        return self.processors.get(ext.lower(), self.processors.get('.generic'))

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f: 
                    self.cache = json.load(f)
            except: self.cache = {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f: 
                json.dump(self.cache, f, indent=4)
        except Exception as e: 
            print(f"⚠️ Errore Cache: {e}")

    def _get_file_hash(self, content): 
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    # I metodi compute_defcon_matrix e extract_todos sono spostati qui
    # per praticità operativa dello stadio 2, ma potrebbero teoricamente
    # stare in processors.base. Li manteniamo qui per non alterare le dipendenze
    # già create nello scanner/analyzer.

    def compute_defcon_matrix(self, dependency_count, scene_instances, has_heavy_methods):
        score = 1
        if dependency_count >= 7 or scene_instances > 10: score = 3
        elif dependency_count >= 4 or scene_instances > 3 or has_heavy_methods: score = 2
        return score

    def extract_todos(self, code, ext):
        todos = []
        if not code: return todos
        # Pattern centralizzato, ma che distingue per estensione per evitare falsi positivi in CSS/HTML
        ext_lower = ext.lower()
        if ext_lower in [".css", ".uss", ".html", ".uxml"]:
            pattern = r'/\*\s*(TODO|FIXME|HACK):?\s*(.*?)\s*\*/'
        else:
            pattern = r'//\s*(TODO|FIXME|HACK):?\s*(.*)|#\s*(TODO|FIXME|HACK):?\s*(.*)'

        for match in re.finditer(pattern, code, re.IGNORECASE):
            # Gestione sicura dei gruppi matchati (evita NoneType errors)
            groups = [g for g in match.groups() if g is not None]
            if len(groups) >= 2:
               todos.append(f"[{groups[0].upper()}] {groups[1].strip()}")
        return todos

    def get_script_summary(self, file_name, code, ext, language="IT", project_type="Generico"):
        if not code: return "Nessuna telemetria."
        code_hash = self._get_file_hash(code)
        
        if file_name in self.cache and self.cache[file_name].get("hash") == code_hash:
            return self.cache[file_name]["summary"]

        processor = self.get_processor(ext)
        
        if "none" in self.provider_config["provider"].lower():
            # Ora deleghiamo DIRETTAMENTE al processore per ottenere il blueprint tecnico
            summary = processor.extract_pure_blueprint(code)
        else:
            # Qui andrà la logica LLM futura
            summary = processor.extract_pure_blueprint(code) 

        self.cache[file_name] = {"hash": code_hash, "summary": summary}
        self._save_cache()
        return summary