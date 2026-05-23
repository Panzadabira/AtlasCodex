# -*- coding: utf-8 -*-
import re
from .base import BaseLanguageProcessor

class CFamilyProcessor(BaseLanguageProcessor):
    def extract_api_signature(self, code):
        """Svuota chirurgicamente i corpi di metodi e proprietà mantenendo solo firme ed enum."""
        if not code: return ""
        
        # Rimozione preventiva di tutti i commenti
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        code = re.sub(r'//.*', '', code)
        
        lines = code.splitlines()
        stripped = []
        in_enum = False
        
        for line in lines:
            cleaned = line.strip()
            if not cleaned: continue
            
            # Gestione ingresso/uscita blocchi enum
            if "enum " in cleaned:
                in_enum = True
                stripped.append(line)
                continue
            
            if in_enum:
                if "}" in cleaned:
                    in_enum = False
                    stripped.append(line)
                else:
                    stripped.append(line)
                continue

            # Mappatura direttive di preelaborazione, namespace, classi, interfacce, strutture
            if cleaned.startswith("#include") or any(k in cleaned for k in ["using ", "namespace ", "class ", "interface ", "struct "]):
                stripped.append(line)
                continue
                
            # Filtro visibilità metodi e proprietà
            if any(k in cleaned for k in ["public ", "private ", "protected ", "internal "]):
                if "{" in cleaned:
                    signature = cleaned.split("{")[0].strip()
                    if "(" not in signature and "=" not in signature:
                        # Proprietà C# (get; set;)
                        stripped.append(line.replace(line.strip(), f"{signature} {{ get; set; }}"))
                    else:
                        stripped.append(line.replace(line.strip(), f"{signature} {{ /* ... */ }}"))
                elif "(" in cleaned and ")" in cleaned and not cleaned.endswith(";"):
                    stripped.append(line + " { /* ... */ }")
                else:
                    stripped.append(line)
                    
        result = "\n".join(stripped)
        return result if len(result) > 10 else "// [Blueprint Strutturale C-Family]"

    def analyze_bottlenecks(self, code):
        if not code: return False
        # Identifica Update continui di Unity o cicli for intensivi
        loop_pattern = r"\b(Update|FixedUpdate|LateUpdate)\s*\(\s*\)"
        if re.search(loop_pattern, code):
            return "GetComponent" in code or "Find" in code
        return any(p in code for p in ["malloc(", "new item[", "goto "])

    def extract_dependencies(self, code, class_map, current_name):
        deps = []
        if not code: return deps
        for o_class, o_file in class_map.items():
            if o_class != current_name:
                if f'#include "{o_class}' in code or re.search(r'\b' + re.escape(o_class) + r'\b', code):
                    deps.append(o_file)
        return deps

    def extract_pure_blueprint(self, code):
        inheritance = re.search(r"(?:class|struct)\s+\w+\s*:\s*([\w\s,<>]+)", code)
        base = inheritance.group(1).strip() if inheritance else "Nativa Indipendente"
        return f"Architettura ad oggetti. Derivazione: {base}."

def register():
    return {
        '.cs': CFamilyProcessor(), '.cpp': CFamilyProcessor(), 
        '.c': CFamilyProcessor(), '.h': CFamilyProcessor(), '.hpp': CFamilyProcessor()
    }