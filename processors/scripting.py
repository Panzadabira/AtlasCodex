# -*- coding: utf-8 -*-
import re
from .base import BaseLanguageProcessor

class ScriptingProcessor(BaseLanguageProcessor):
    def extract_api_signature(self, code):
        """Mappa la struttura Python/Scripting estraendo solo firme di funzioni e classi."""
        if not code: return ""
        lines = code.splitlines()
        stripped = []
        
        for line in lines:
            cleaned = line.strip()
            # Mantiene solo le righe di dichiarazione strutturale
            if cleaned.startswith(("class ", "def ", "import ", "from ", "async def ")):
                # Aggiunge una firma pulita per far capire che il corpo è stato rimosso
                if cleaned.endswith(":"):
                    stripped.append(line + " ... [Code Body Svuotato]")
                else:
                    stripped.append(line)
            elif cleaned.startswith("@"):
                stripped.append(line)
                
        result = "\n".join(stripped)
        return result if len(result) > 10 else "# [Blueprint Strutturale Scripting]"

    def analyze_bottlenecks(self, code):
        if not code: return False
        # Rileva annidamenti pesanti o funzioni pericolose
        patterns = [r"for\s+.*:\s*\n\s+for\s+.*:", r"eval\s*\(", r"exec\s*\("]
        return any(re.search(p, code) for p in patterns)

    def extract_dependencies(self, code, class_map, current_name):
        deps = []
        if not code: return deps
        for o_class, o_file in class_map.items():
            if o_class != current_name:
                if re.search(r'\b(import|from)\s+' + re.escape(o_class) + r'\b', code) or re.search(r'\b' + re.escape(o_class) + r'\b', code):
                    deps.append(o_file)
        return deps

    def extract_pure_blueprint(self, code):
        inheritance = re.search(r"class\s+\w+\((.*?)\):", code)
        base = inheritance.group(1).strip() if inheritance else "Modulo Autonomo"
        return f"Scripting Core. Modello base di derivazione: {base}."

def register():
    return {'.py': ScriptingProcessor(), '.lua': ScriptingProcessor(), '.rb': ScriptingProcessor()}