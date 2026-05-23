# -*- coding: utf-8 -*-

"""
Atlas_Localization v2.8 - Universal Commercial Translation Matrix
Centralizza le traduzioni sia per il Launcher Desktop nativo che per il report finale HTML.
Garantisce la conformità UTF-8 assoluta per glifi complessi (cirillico, cinese, umlaut).
Copertura totale per Dashboard dinamica e impaginazione flessibile.
"""

LOCALIZATION_MATRIX = {
    "EN": {
        
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 PROJECT SOURCE & ARCHITECTURE CONTEXT ",
        "UI_SRC_TYPE": "Source Type:", "UI_PROJ_TYPE": "Project Type:",
        "UI_PATH_FOLDER": "Project Folder Path:", "UI_PATH_GIT": "Git Repository URL:",
        "UI_BROWSE": "Browse...", "UI_ENGINE_FRAME": " 🧠 ANALYSIS ENGINE SETTINGS ",
        "UI_MOTOR": "Analysis Motor:", "UI_MODEL": "Model Name:",
        "UI_URL": "URL Endpoint:", "UI_KEY": "Private API Key:",
        "UI_LANG_FRAME": " 🌍 SYSTEM LOCALIZATION ", "UI_LANG_LABEL": "Select Interface & Output Language:",
        "UI_STATUS_FRAME": " 📊 WORKFLOW PROGRESS STATUS ",
        "UI_RUN_BTN": "🚀 GENERATE AND OPEN ADAPTIVE ARCHITECTURE CODEX",
        "UI_FOOTER": "Pre-scan opening and asynchronous loading are managed by the Delta Engine.",
        "UI_STATUS_READY": "Select a source folder to activate adaptive analysis.",
        "UI_STATUS_RECOGNIZED": "Recognized previous Codex configuration in Memory for path: '{}'.",

	    "__L_CONTEXT_MODE__": "LLM Context Configuration",
        "__L_MODE_MAP__": "API / Method Map Only",
        "__L_MODE_TARGET__": "Target Full",
        "__L_MODE_FULL__": "Full Code",
        "__L_TOKENS__": "Estimated Tokens: ~",
    },
    "IT": {
      
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 ORIGINE PROGETTO & CONTESTO ARCHITETTURALE ",
        "UI_SRC_TYPE": "Tipo di Origine:", "UI_PROJ_TYPE": "Tipo di Progetto:",
        "UI_PATH_FOLDER": "Cartella del Progetto:", "UI_PATH_GIT": "URL Repository Git:",
        "UI_BROWSE": "Sfoglia...", "UI_ENGINE_FRAME": " 🧠 IMPOSTAZIONI MOTORE DI ANALISI ",
        "UI_MOTOR": "Motore Analisi:", "UI_MODEL": "Nome Modello:",
        "UI_URL": "URL Endpoint:", "UI_KEY": "Chiave API Privata:",
        "UI_LANG_FRAME": " 🌍 LOCALIZZAZIONE DI SISTEMA ", "UI_LANG_LABEL": "Seleziona Lingua Interfaccia ed Output:",
        "UI_STATUS_FRAME": " 📊 STATO AVANZAMENTO WORKFLOW ",
        "UI_RUN_BTN": "🚀 GENERA ED APRI ARCHITECTURE CODEX ADATTIVO",
        "UI_FOOTER": "L'apertura pre-scansione e il caricamento asincrono sono gestiti dal Delta Engine.",
        "UI_STATUS_READY": "Seleziona la cartella sorgente per attivare l'analisi adattiva.",
        "UI_STATUS_RECOGNIZED": "Rilevata configurazione Codex esistente in Memory per il percorso: '{}'.",

	"__L_CONTEXT_MODE__": "Configurazione Contesto LLM",
        "__L_MODE_MAP__": "Solo API / Mappa dei Metodi",
        "__L_MODE_TARGET__": "Target Full",
        "__L_MODE_FULL__": "Codice Completo",
        "__L_TOKENS__": "Token Stimati: ~",
    },

    "DE": {
       
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 PROJEKTQUELLE UND ARCHITEKTURKONTEXT ",
        "UI_SRC_TYPE": "Quellentyp:", "UI_PROJ_TYPE": "Projekttyp:",
        "UI_PATH_FOLDER": "Projektordner-Pfad:", "UI_PATH_GIT": "Git-Repository-URL:",
        "UI_BROWSE": "Durchsuchen...", "UI_ENGINE_FRAME": " 🧠 ANALYSE-ENGINE-EINSTELLUNGEN ",
        "UI_MOTOR": "Analyse-Motor:", "UI_MODEL": "Modellname:",
        "UI_URL": "URL-Endpunkt:", "UI_KEY": "Privater API-Schlüssel:",
        "UI_LANG_FRAME": " 🌍 SYSTEM-LOKALISIERUNG ", "UI_LANG_LABEL": "Schnittstellen- und Ausgabesprache wählen:",
        "UI_STATUS_FRAME": " 📊 WORKFLOW-FORTSCHRITTSSTATUS ",
        "UI_RUN_BTN": "🚀 ADAPTIVEN ARCHITEKTUR-CODEX GENERIEREN UND ÖFFNEN",
        "UI_FOOTER": "Das Öffnen vor dem Scannen und das asynchrone Laden werden von der Delta Engine verwaltet.",
        "UI_STATUS_READY": "Wählen Sie einen Quellordner aus, um die adaptive Analyse zu aktivieren.",
        "UI_STATUS_RECOGNIZED": "Vorherige Codex-Konfiguration im Speicher für Pfad erkannt: '{}'.",

	"__L_CONTEXT_MODE__": "LLM-Kontextkonfiguration",
        "__L_MODE_MAP__": "Nur API / Methoden-Map",
        "__L_MODE_TARGET__": "Ziel Vollständig",
        "__L_MODE_FULL__": "Vollständiger Code",
        "__L_TOKENS__": "Geschätzte Tokens: ~",
    },
    "FR": {
               
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 SOURCE DU PROJET & CONTEXTE D'ARCHITECTURE ",
        "UI_SRC_TYPE": "Type de Source :", "UI_PROJ_TYPE": "Type de Projet :",
        "UI_PATH_FOLDER": "Chemin du Dossier Projet :", "UI_PATH_GIT": "URL du Dépôt Git :",
        "UI_BROWSE": "Parcourir...", "UI_ENGINE_FRAME": " 🧠 PARAMÈTRES DU MOTEUR D'ANALYSE ",
        "UI_MOTOR": "Moteur d'Analyse :", "UI_MODEL": "Nom du Modèle :",
        "UI_URL": "Point de Terminaison URL :", "UI_KEY": "Clé API Privata :",
        "UI_LANG_FRAME": " 🌍 LOCALISATION DU SYSTÈME ", "UI_LANG_LABEL": "Sélectionnez la Langue de l'Interface & de Sortie :",
        "UI_STATUS_FRAME": " 📊 STATUT DE PROGRESSION DU WORKFLOW ",
        "UI_RUN_BTN": "🚀 GÉNÉRER ET OUVRIR LE CODEX D'ARCHITECTURE ADAPTATIF",
        "UI_FOOTER": "L'ouverture pré-scan et le chargement asynchrone sont gérés par le Delta Engine.",
        "UI_STATUS_READY": "Sélectionnez un dossier source pour activer l'analyse adaptative.",
        "UI_STATUS_RECOGNIZED": "Configuration Codex précédente reconnue en mémoire pour le chemin : '{}'.",

	"__L_CONTEXT_MODE__": "Configuration du Contexte LLM",
        "__L_MODE_MAP__": "API / Carte des Méthodes Uniquement",
        "__L_MODE_TARGET__": "Cible Complète",
        "__L_MODE_FULL__": "Code Complet",
        "__L_TOKENS__": "Jetons Estimés : ~",
    },
    "ES": {
     
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 FUENTE DEL PROYECTO Y CONTEXTO DE ARQUITECTURA ",
        "UI_SRC_TYPE": "Tipo de Origen:", "UI_PROJ_TYPE": "Tipo de Proyecto:",
        "UI_PATH_FOLDER": "Ruta de la Carpeta del Proyecto:", "UI_PATH_GIT": "URL del Repositorio Git:",
        "UI_BROWSE": "Examinar...", "UI_ENGINE_FRAME": " 🧠 CONFIGURACIÓN DEL MOTOR DE ANÁLISIS ",
        "UI_MOTOR": "Motor de Análisis:", "UI_MODEL": "Nombre del Modelo:",
        "UI_URL": "Punto de Extremo URL:", "UI_KEY": "Clve API Privada:",
        "UI_LANG_FRAME": " 🌍 LOCALIZACIÓN DEL SISTEMA ", "UI_LANG_LABEL": "Seleccione Idioma de Interfaz y Salida:",
        "UI_STATUS_FRAME": " 📊 ESTADO DE PROGRESO DEL FLUJO DE TRABAJO ",
        "UI_RUN_BTN": "🚀 GENERAR Y ABRIR CODEX DE ARQUITECTURA ADAPTATIVO",
        "UI_FOOTER": "La apertura de pre-escaneo y la carga asíncrona son gestionadas por el Delta Engine.",
        "UI_STATUS_READY": "Seleccione una carpeta de origen para activar el análisis adaptativo.",
        "UI_STATUS_RECOGNIZED": "Configuración de Codex anterior encontrada en Memory para la ruta: '{}'.",

	"__L_CONTEXT_MODE__": "Configuración de Contexto LLM",
        "__L_MODE_MAP__": "Solo API / Mapa de Métodos",
        "__L_MODE_TARGET__": "Objetivo Completo",
        "__L_MODE_FULL__": "Código Completo",
        "__L_TOKENS__": "Tokens Estimados: ~",
    },
    "RU": {
       
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 ИСХОДНЫЙ КОД ПРОЕКТА И АРХИТЕКТУРНЫЙ КОНТЕКСТ ",
        "UI_SRC_TYPE": "Тип Источника:", "UI_PROJ_TYPE": "Тип Проекта:",
        "UI_PATH_FOLDER": "Путь к Папке Проекта:", "UI_PATH_GIT": "URL Git-Репозитория:",
        "UI_BROWSE": "Обзор...", "UI_ENGINE_FRAME": " 🧠 НАСТРОЙКИ АНАЛИТИЧЕСКОГО ДВИЖКА ",
        "UI_MOTOR": "Аналитический Движок:", "UI_MODEL": "Название Модели:",
        "UI_URL": "URL Точка Подключения:", "UI_KEY": "Приватный Ключ API:",
        "UI_LANG_FRAME": " 🌍 ЛОКАЛИЗАЦИЯ СИСТЕМЫ ", "UI_LANG_LABEL": "Выберите Язык Интерфейса и Вывода:",
        "UI_STATUS_FRAME": " 📊 СТАТУС ВЫПОЛНЕНИЯ РАБОЧЕГО ПРОЦЕССА ",
        "UI_RUN_BTN": "🚀 СГЕНЕРИРОВАТЬ И ОТКРЫТЬ АДАПТИВНЫЙ АРХИТЕКТУРНЫЙ КОДЕКС",
        "UI_FOOTER": "Открытие перед сканированием и асинхронная загрузка управляются движком Delta Engine.",
        "UI_STATUS_READY": "Выберите папку с исходным кодом для активации адаптивного анализа.",
        "UI_STATUS_RECOGNIZED": "Обнаружена сохраненная конфигурация Codex в Memory для пути: '{}'.",

	"__L_CONTEXT_MODE__": "Настройка контекста LLM",
        "__L_MODE_MAP__": "Только API / Карта методов",
        "__L_MODE_TARGET__": "Полный целевой код",
        "__L_MODE_FULL__": "Полный код",
        "__L_TOKENS__": "Оценка токенов: ~",
    },
    "ZH": {
       
        # --- DESKTOP LAUNCHER TOKENS (UI) ---
        "UI_HEADER": "PANZASCOPE CODEX ENGINE - SETUP CENTER",
        "UI_SRC_FRAME": " 📂 项目源码与系统 live 架构上下文 ",
        "UI_SRC_TYPE": "源码类型:", "UI_PROJ_TYPE": "项目类型:",
        "UI_PATH_FOLDER": "项目本地文件夹 路径:", "UI_PATH_GIT": "Git 仓库托管 URL 地址:",
        "UI_BROWSE": "浏览...", "UI_ENGINE_FRAME": " 🧠 局架构分析引擎 算法设置 ",
        "UI_MOTOR": "核心分析引擎:", "UI_MODEL": "底层模型名称:",
        "UI_URL": "URL 访问端点:", "UI_KEY": "私有 API 密钥安全锁:",
        "UI_LANG_FRAME": " 🌍 自动化全球语言 本地化中心 ", "UI_LANG_LABEL": "选择可视化界面与输出报告语言:",
        "UI_STATUS_FRAME": " 📊 核心流水线 实时状态监控面板 ",
        "UI_RUN_BTN": "🚀 立即编译并生成 交互式自适应架构地图报告",
        "UI_FOOTER": "预扫描载入、内存感知与异步刷新流皆由底层 Delta 引擎集群自动化驱动.",
        "UI_STATUS_READY": "请选择需要提取的底层物理源码文件夹以激活自适应解析引擎.",
        "UI_STATUS_RECOGNIZED": "内存成功感知到已有项目配置，底层物理绝对路径为: '{}'.",

	"__L_CONTEXT_MODE__": "LLM 上下文配置",
        "__L_MODE_MAP__": "仅 API / 方法映射",
        "__L_MODE_TARGET__": "目标完整代码",
        "__L_MODE_FULL__": "完整代码",
        "__L_TOKENS__": "预估 Token: ~",
    }
}