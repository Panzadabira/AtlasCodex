# -*- coding: utf-8 -*-
class BaseLanguageProcessor:
    def extract_api_signature(self, code):
        """Metodo di ripiego universale: estrae le prime linee significative (es. definizioni)."""
        if not code: return ""
        lines = code.splitlines()
        # Prende le prime 35 righe non vuote come firma di fallback strutturale
        return "\n".join([line for line in lines if len(line.strip()) > 0][:35])

    def analyze_bottlenecks(self, code): 
        """Analisi generica di loop o hotspot."""
        if not code: return False
        c_lower = code.lower()
        return "while true" in c_lower or "for(;;)" in c_lower

    def extract_dependencies(self, code, class_map, current_name): 
        """Ricerca accoppiamenti universale basata sulle menzioni delle classi nel progetto."""
        deps = []
        if not code: return deps
        for o_class, o_file in class_map.items():
            if o_class != current_name and f"{o_class}" in code:
                deps.append(o_file)
        return deps

    def identify_layer(self, fname, rel_path, code):
        """Logica di Layerizzazione Centralizzata Universale basata su convenzioni architetturali."""
        f_lower = fname.lower()
        p_lower = rel_path.lower()
        c_lower = code[:1000].lower() if code else ""

        if "interface" in c_lower or "ievent" in f_lower or "abstract" in f_lower or "base" in f_lower:
            return "L0"  # Contratti, Interfacce, Astrazioni
        if "data" in p_lower or "so_" in f_lower or "config" in f_lower or "entity" in f_lower or "dto" in f_lower or "model" in f_lower:
            return "L1"  # Strutture Dati, Configurazione, DNA
        if "manager" in f_lower or "controller" in f_lower or "system" in f_lower or "orchestrator" in f_lower or "core" in p_lower or "agent" in f_lower:
            return "L2"  # Sistemi Centrali, Orchestratori, Logica Core
        if "view" in f_lower or "panel" in f_lower or "canvas" in f_lower or "ui" in p_lower or "uxml" in f_lower or "gui" in p_lower or "screen" in f_lower:
            return "L4"  # Interfaccia Utente, Presentazione Visiva
        
        return "L3"  # Moduli Logici Specifici, Componenti, Utility

    def extract_pure_blueprint(self, code): 
        """Descrizione strategica di fallback."""
        return "Modulo logico di esecuzione standard."