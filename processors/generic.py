# -*- coding: utf-8 -*-
from .base import BaseLanguageProcessor

class GenericProcessor(BaseLanguageProcessor):
    def extract_api_signature(self, code):
        return "// [Config/Data Module] - Struttura dati memorizzata."

    def extract_dependencies(self, code, class_map, current_name):
        return []

    def extract_pure_blueprint(self, code):
        return "File di asset statico o configurazione dell'ambiente."

def register():
    return {
        '.generic': GenericProcessor(), '.txt': GenericProcessor(), '.md': GenericProcessor(),
        '.json': GenericProcessor(), '.xml': GenericProcessor(), '.yaml': GenericProcessor()
    }