# app/config/navigation.py
navigation_tree = {
    "Computadoras y Notebooks": {
        "Computadoras": {
            "All-in-One": ["Celeron", "Core i5", "Core i7"],
            "Gaming": [],
            "Workstation": [],
            "Barebones": ["Para AIO", "Para PC"]
        },
        "Notebooks": {
            "Uso General": ["Core i3", "Core i5", "Core i7", "Core i9", "Ryzen 3", "Ryzen 5", "Ryzen 7", "Celeron", "Athlon", "Qualcomm"],
            "Gaming": ["Core i5", "Core i7", "Core i9", "Ryzen 5", "Ryzen 7"],
            "Core Ultra": ["Ultra 5", "Ultra 7", "Ultra 9"],
            "Workstation": [],
            "2-in-1": ["Celeron"],
            "Chromebook": [],
            "Accesorios": ["Maletines y Mochilas", "Notebooks Propietarios", "Otros Accesorios"]
        }
    },
    "Componentes de Hardware": {
        "Procesadores": {
            "Intel": ["Core i3", "Core i5", "Core i7", "Core i9", "Core Ultra", "Celeron", "Pentium"],
            "AMD Ryzen": ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]
        },
        "Placas Madre": ["Socket 1200", "Socket 1700", "Socket 1851", "Socket AM4", "Socket AM5"],
        "Memorias": ["DDR3", "DDR4", "DDR5", "SODIMM", "Flash"],
        "Almacenamiento": ["SSDs", "Discos Duros", "DVD-Writer"],
        "Tarjetas de Video": ["NVIDIA", "Radeon", "Accesorios"],
        "Gabinetes": ["ATX", "Micro ATX", "Con Fuente", "Sin Fuente", "Accesorios"]
    },
    "Periféricos y Accesorios": {
        "Periféricos": ["Teclados", "Mouse", "Kits", "Otros"],
        "Accesorios": ["Coolers", "Audio", "USB", "Ensamblaje", "Mouse Pads", "Otros"]
    },
    "Monitores y Pantallas": {
        "Monitores": ["Planos", "Curvos", "Gaming", "Portátiles", "Pizarras Táctiles", "LFD", "Accesorios"]
    },
    "Redes y Conectividad": {
        "Redes": ["Switches", "WiFi", "Cámaras IP", "Hubs", "Racks", "Patch Cords", "Seguridad", "Accesorios"]
    },
    "Impresoras y Suministros": {
        "Impresoras": ["Láser", "Tinta", "Térmica", "Ticketera", "Diseño", "Accesorios"],
        "Suministros": ["Tintas", "Botellas", "Bolsas", "Cintas", "Tanque de Tinta", "Plotters", "Tape Backup", "Genéricos"]
    },
    "Audio y Multimedia": {
        "Audio": ["Auriculares", "Parlantes", "Accesorios"]
    },
    "Energía y Climatización": {
        "UPS": ["Interactivo", "Online", "Accesorios", "Otros"],
        "Energía": ["Estabilizadores", "Estaciones Portátiles"],
        "Energía Renovable": ["Paneles Solares"],
        "Climatización": ["Aire Acondicionado", "Accesorios"]
    },
    "Servidores y Software": {
        "Servidores": ["Genéricos", "NAS/SAN", "Software", "Tape Backup", "Tarjetas", "CPUs Propietarios", "Memorias", "Fuentes", "CDROM/DVD", "Accesorios"],
        "Software": ["Microsoft", "Antivirus", "Otros"]
    },
    "Smart Home y Dispositivos Móviles": {
        "Smart Home": ["Cámaras", "Luces", "Enchufes"],
        "Teléfonos Celulares": ["Smartphones Android", "Celulares Básicos", "Smartwatches", "Accesorios"],
        "Tablets": ["Android", "Windows", "Accesorios"]
    },
    "Televisores y Consolas": {
        "Televisores": ["LED/Smart TV", "Racks"],
        "Consolas": ["PlayStation 5", "Otras Marcas"]
    },
    "Otros": {
        "Imágenes": ["Webcams", "Escáneres", "Proyectores", "Accesorios"],
        "Protección": ["Máscaras", "Medidores de Calor"],
        "Servicios": ["Técnico", "Ventas", "Garantía Extendida", "Internet", "Otros"],
        "Repuestos": ["PCBA", "LCD", "Otros Hardware", "Varios"],
        "Mobiliario": ["Sillas Gaming"],
        "Sin Clasificar": ["Precio Estándar", "Muestras", "Sin Clasificar"]
    }
}