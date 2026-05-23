# -*- coding: utf-8 -*-
import re
from .base import BaseLanguageProcessor

class WebUIProcessor(BaseLanguageProcessor):
    def extract_api_signature(self, code):
        """Isola le definizioni strutturali di stili, tag DOM e funzioni JS."""
        if not code: return ""
        lines = code.splitlines()
        stripped = []
        
        # Analisi file CSS / USS
        if any(line.strip().startswith((".", "#", "@")) for line in lines[:20] if line.strip()):
            for line in lines:
                cleaned = line.strip()
                if "{" in cleaned:
                    stripped.append(line.split("{")[0].strip() + " { /* Regole Omesse */ }")
                elif cleaned.startswith((".", "#")):
                    if not cleaned.endswith("}") and ":" not in cleaned:
                        stripped.append(line)
            return "\n".join(stripped)
            
        # Analisi file HTML / UXML / JS
        for line in lines:
            cleaned = line.strip()
            # Estrazione nodi di Layout con ID o Classi (ancore di binding)
            if "<" in cleaned and re.search(r'\b(id|class|name)\s*=', cleaned):
                tag_only = re.sub(r'>.*', '>', line)
                stripped.append(tag_only)
            # Estrazione funzioni JavaScript
            elif any(k in cleaned for k in ["function ", "const ", "class "]) and "(" in cleaned:
                if "{" in cleaned:
                    stripped.append(cleaned.split("{")[0].strip() + " { /* JS logic */ }")
                else:
                    stripped.append(cleaned)
        
        result = "\n".join(stripped)
        return result if len(result) > 10 else "// [Blueprint Strutturale Interfaccia]"

    def analyze_bottlenecks(self, code):
        if not code: return False
        return "document.write(" in code or "localStorage.set" in code

    def extract_dependencies(self, code, class_map, current_name):
        deps = []
        if not code: return deps
        for o_class, o_file in class_map.items():
            if o_class != current_name and re.search(r'\b' + re.escape(o_class) + r'\b', code):
                deps.append(o_file)
        return deps

    def extract_pure_blueprint(self, code):
        return "Componente di orchestrazione visiva / Layout UI."

def register():
    return {'.html': WebUIProcessor(), '.css': WebUIProcessor(), '.js': WebUIProcessor(), '.uxml': WebUIProcessor(), '.uss': WebUIProcessor()}