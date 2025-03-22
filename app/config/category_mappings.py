# app/config/category_mappings.py

categoria_map = {
    # Entradas existentes (mapeadas previamente)
    "acc, muebles de computo": {"categoria_general": "Accesorios", "subcategoria": "Muebles de Computación"},
    "accesorios": {"categoria_general": "Accesorios", "subcategoria": "Generales"},
    "audio, auricular c/mic": {"categoria_general": "Audio", "subcategoria": "Auriculares con Micrófono"},
    "computadora aio celeron": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Celeron"},
    "televisores led/smart tv": {"categoria_general": "Televisores", "subcategoria": "LED/Smart TV"},
    "notebook core i5": {"categoria_general": "Notebooks", "subcategoria": "Core i5"},
    "notebook core i7": {"categoria_general": "Notebooks", "subcategoria": "Core i7"},
    "notebook core i9": {"categoria_general": "Notebooks", "subcategoria": "Core i9"},
    "notebook core ultra 5": {"categoria_general": "Notebooks", "subcategoria": "Core Ultra 5"},
    "notebook core ultra 7": {"categoria_general": "Notebooks", "subcategoria": "Core Ultra 7"},
    "notebook core ultra 9": {"categoria_general": "Notebooks", "subcategoria": "Core Ultra 9"},
    "notebook gaming core i5": {"categoria_general": "Notebooks", "subcategoria": "Gaming Core i5"},
    "notebook gaming core i7": {"categoria_general": "Notebooks", "subcategoria": "Gaming Core i7"},
    "notebook gaming core i9": {"categoria_general": "Notebooks", "subcategoria": "Gaming Core i9"},
    "notebook gaming ryzen 5": {"categoria_general": "Notebooks", "subcategoria": "Gaming Ryzen 5"},
    "notebook gaming ryzen 7": {"categoria_general": "Notebooks", "subcategoria": "Gaming Ryzen 7"},
    "notebook qualcomm": {"categoria_general": "Notebooks", "subcategoria": "Qualcomm"},
    "notebook workstation": {"categoria_general": "Notebooks", "subcategoria": "Workstations"},
    "notebook, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Notebooks"},
    "notebook, maletin/mochila": {"categoria_general": "Accesorios", "subcategoria": "Maletines y Mochilas"},
    "red, switch basico": {"categoria_general": "Redes", "subcategoria": "Switches Básicos"},
    "sillas gamer": {"categoria_general": "Mobiliario", "subcategoria": "Sillas Gaming"},
    "smart home - camaras": {"categoria_general": "Smart Home", "subcategoria": "Cámaras"},
    "ssd 2.5 sata": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs 2.5 SATA"},
    "ssd m.2 nvme": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs M.2 NVMe"},
    "ssd m.2 sata": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs M.2 SATA"},
    "disco duro externo 2.5": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros Externos 2.5"},
    "disco duro externo 3.5": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros Externos 3.5"},
    "disco solido externo(ssd)": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs Externos"},
    "monitor gaming plano 23": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 23"},
    "monitor gaming curvo 23": {"categoria_general": "Monitores", "subcategoria": "Gaming Curvos 23"},
    "monitor plano 25": {"categoria_general": "Monitores", "subcategoria": "Planos 25"},
    "monitor curvo 31.5": {"categoria_general": "Monitores", "subcategoria": "Curvos 31-32"},
    "red wifi accesorios": {"categoria_general": "Redes", "subcategoria": "Accesorios WiFi"},
    "red wifi ap interiores": {"categoria_general": "Redes", "subcategoria": "Access Points Interiores"},
    "red, switch basico admin": {"categoria_general": "Redes", "subcategoria": "Switches Básicos Administrables"},
    "red, camaras ip": {"categoria_general": "Redes", "subcategoria": "Cámaras IP"},
    "impresora multifun laser": {"categoria_general": "Impresoras", "subcategoria": "Multifuncional Láser"},
    "impresora laser/led": {"categoria_general": "Impresoras", "subcategoria": "Láser/LED"},
    "impresora termica": {"categoria_general": "Impresoras", "subcategoria": "Térmica"},
    "servidores": {"categoria_general": "Servidores", "subcategoria": "Genéricos"},
    "servidores, accesorios": {"categoria_general": "Servidores", "subcategoria": "Accesorios"},
    "servidores, nas/san": {"categoria_general": "Servidores", "subcategoria": "NAS/SAN"},
    "ups online": {"categoria_general": "UPS", "subcategoria": "Online"},
    "cpu ci3 10xxx s1200": {"categoria_general": "Procesadores", "subcategoria": "Core i3 10xxx S1200"},
    "cpu ci5 7xxx s1151": {"categoria_general": "Procesadores", "subcategoria": "Core i5 7xxx S1151"},
    "cpu ci5 10xxx s1200": {"categoria_general": "Procesadores", "subcategoria": "Core i5 10xxx S1200"},
    "cpu ci5 11xxx s1200": {"categoria_general": "Procesadores", "subcategoria": "Core i5 11xxx S1200"},
    "cpu ci5 12xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i5 12xxx S1700"},
    "cpu ci5 13xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i5 13xxx S1700"},
    "cpu ci5 14xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i5 14xxx S1700"},
    "cpu ci7 12xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i7 12xxx S1700"},
    "cpu ci7 13xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i7 13xxx S1700"},
    "cpu ci7 14xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i7 14xxx S1700"},
    "cpu ci9 12xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i9 12xxx S1700"},
    "cpu ci9 13xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i9 13xxx S1700"},
    "cpu ci9 14xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i9 14xxx S1700"},
    "monitor gaming plano 31.5": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 31-32"},
    "monitor gaming plano 34": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 34"},
    "monitor gaming curvo 31.5": {"categoria_general": "Monitores", "subcategoria": "Gaming Curvos 31-32"},
    "monitor curvo 23": {"categoria_general": "Monitores", "subcategoria": "Curvos 23"},
    "monitor curvo 34": {"categoria_general": "Monitores", "subcategoria": "Curvos 34"},
    "monitor plano 29": {"categoria_general": "Monitores", "subcategoria": "Planos 29"},
    "monitor plano 34": {"categoria_general": "Monitores", "subcategoria": "Planos 34"},
    "red wifi ap empresa inter": {"categoria_general": "Redes", "subcategoria": "Access Points Empresariales Interiores"},
    "red wifi access point ext": {"categoria_general": "Redes", "subcategoria": "Access Points Exteriores"},
    "red wifi antenas exterior": {"categoria_general": "Redes", "subcategoria": "Antenas WiFi Exteriores"},
    "red wifi router-adsl": {"categoria_general": "Redes", "subcategoria": "Routers ADSL"},
    "red, switch distrib smb": {"categoria_general": "Redes", "subcategoria": "Switches Distribución SMB"},
    "red, switch borde small b": {"categoria_general": "Redes", "subcategoria": "Switches Borde Small Business"},
    "mem ddr4 3200 pc4-25600": {"categoria_general": "Memorias", "subcategoria": "DDR4 3200"},
    "mem ddr5 5200 pc5-41600": {"categoria_general": "Memorias", "subcategoria": "DDR5 5200"},
    "mem sodimm ddr4 2666": {"categoria_general": "Memorias", "subcategoria": "SODIMM DDR4 2666"},
    "mem sodimm ddr5 4800": {"categoria_general": "Memorias", "subcategoria": "SODIMM DDR5 4800"},
    "impresora multifun tinta": {"categoria_general": "Impresoras", "subcategoria": "Multifuncional Tinta"},
    "servicio tecnico": {"categoria_general": "Servicios", "subcategoria": "Técnico"},
    "software, otros": {"categoria_general": "Software", "subcategoria": "Otros"},
    "ms office": {"categoria_general": "Software", "subcategoria": "Microsoft Office"},
    "ups, accesorios": {"categoria_general": "UPS", "subcategoria": "Accesorios"},
    "tablet windows": {"categoria_general": "Tablets", "subcategoria": "Windows"},
    "t smartphones android": {"categoria_general": "Teléfonos Celulares", "subcategoria": "Smartphones Android"},
    "fan cooler cpu": {"categoria_general": "Accesorios", "subcategoria": "Coolers CPU"},
    "mb socket am4 amd": {"categoria_general": "Placas Madre", "subcategoria": "Socket AM4 AMD"},
    "mb socket am5 amd": {"categoria_general": "Placas Madre", "subcategoria": "Socket AM5 AMD"},

    # Nuevas categorías añadidas (todas las no mapeadas)
    "cpu ci7 7xxx s2066": {"categoria_general": "Procesadores", "subcategoria": "Core i7 7xxx S2066"},
    "notebook 2-in-1 celeron": {"categoria_general": "Notebooks", "subcategoria": "2-in-1 Celeron"},
    "cpu amd ryzen 5 sam4 3xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5 AM4 3xxx"},
    "monitor plano 23": {"categoria_general": "Monitores", "subcategoria": "Planos 23"},
    "video, pci exp nvidia gam": {"categoria_general": "Tarjetas de Video", "subcategoria": "NVIDIA Gaming"},
    "y gabinetes": {"categoria_general": "Gabinetes", "subcategoria": "Genéricos"},
    "protec - mascaras simples": {"categoria_general": "Protección", "subcategoria": "Máscaras Simples"},
    "barebones para aio": {"categoria_general": "Computadoras", "subcategoria": "Barebones AIO"},
    "serv, cpu propietarios": {"categoria_general": "Servidores", "subcategoria": "CPUs Propietarios"},
    "televisores, racks para": {"categoria_general": "Accesorios", "subcategoria": "Racks para Televisores"},
    "monitores lfd 41 - 50": {"categoria_general": "Monitores", "subcategoria": "LFD 41-50"},
    "protec - medidor de calor": {"categoria_general": "Protección", "subcategoria": "Medidores de Calor"},
    "servidores, tarjetas": {"categoria_general": "Servidores", "subcategoria": "Tarjetas"},
    "aire acond. de precision": {"categoria_general": "Climatización", "subcategoria": "Aire Acondicionado de Precisión"},
    "energia r - est. portatil": {"categoria_general": "Energía", "subcategoria": "Estaciones Portátiles"},
    "servidores, software": {"categoria_general": "Servidores", "subcategoria": "Software"},
    "impresora, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Impresoras"},
    "cpu amd ryzen 7 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 7 AM5 7xxx"},
    "cpu amd ryzen 3 sam5 8xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 3 AM5 8xxx"},
    "imagenes, scan/cod/barras": {"categoria_general": "Imágenes", "subcategoria": "Escáneres de Códigos de Barras"},
    "ms windows server": {"categoria_general": "Software", "subcategoria": "Windows Server"},
    "aire acond precision, acc": {"categoria_general": "Climatización", "subcategoria": "Accesorios Aire Acondicionado de Precisión"},
    "mouse pad/mat, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Mouse Pads"},
    "servidores, tape backup": {"categoria_general": "Servidores", "subcategoria": "Tape Backup"},
    "video, pci express nvidia": {"categoria_general": "Tarjetas de Video", "subcategoria": "NVIDIA Genéricas"},
    "serv, mem pc/nb/svr propt": {"categoria_general": "Servidores", "subcategoria": "Memorias Propietarias"},
    "notebook core i3": {"categoria_general": "Notebooks", "subcategoria": "Core i3"},
    "mem sodimm ddr3 1600": {"categoria_general": "Memorias", "subcategoria": "SODIMM DDR3 1600"},
    "mb ci9 s1700 ddr5 gaming": {"categoria_general": "Placas Madre", "subcategoria": "Core i9 S1700 DDR5 Gaming"},
    "imagenes, accesorios disp": {"categoria_general": "Imágenes", "subcategoria": "Accesorios de Dispositivos"},
    "dvd-writer": {"categoria_general": "Almacenamiento", "subcategoria": "DVD-Writer"},
    "soft, licenciamiento corp": {"categoria_general": "Software", "subcategoria": "Licenciamiento Corporativo"},
    "cpu amd ryzen 5 sam4 5xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5 AM4 5xxx"},
    "tablet android": {"categoria_general": "Tablets", "subcategoria": "Android"},
    "accesorios usb": {"categoria_general": "Accesorios", "subcategoria": "USB"},
    "mb ci9 s1700 ddr4": {"categoria_general": "Placas Madre", "subcategoria": "Core i9 S1700 DDR4"},
    "red wifi tarjetas interna": {"categoria_general": "Redes", "subcategoria": "Tarjetas WiFi Internas"},
    "audio, auricular c/mic gm": {"categoria_general": "Audio", "subcategoria": "Auriculares con Micrófono Gaming"},
    "productos sin clasificar": {"categoria_general": "Sin Clasificar", "subcategoria": "Sin Clasificar"},
    "cpu amd ryzen 9 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 9 AM5 9xxx"},
    "ms windows business": {"categoria_general": "Software", "subcategoria": "Windows Business"},
    "audio, parlante inalamb": {"categoria_general": "Audio", "subcategoria": "Parlantes Inalámbricos"},
    "monitor curvo 27": {"categoria_general": "Monitores", "subcategoria": "Curvos 27"},
    "smart home - luces": {"categoria_general": "Smart Home", "subcategoria": "Luces"},
    "suminist p/impres, cintas": {"categoria_general": "Suministros", "subcategoria": "Cintas para Impresoras"},
    "mem ddr5 6000 pc5-48000": {"categoria_general": "Memorias", "subcategoria": "DDR5 6000"},
    "materiales_suministros": {"categoria_general": "Suministros", "subcategoria": "Genéricos"},
    "camara, webcam": {"categoria_general": "Imágenes", "subcategoria": "Webcams"},
    "cases, fuente para gaming": {"categoria_general": "Gabinetes", "subcategoria": "Con Fuente Gaming"},
    "mem ddr4 4000 pc4-32000": {"categoria_general": "Memorias", "subcategoria": "DDR4 4000"},
    "cases sin fuente p/gamers": {"categoria_general": "Gabinetes", "subcategoria": "Sin Fuente Gaming"},
    "consumo tanque tinta mult": {"categoria_general": "Suministros", "subcategoria": "Tanque de Tinta Multifuncional"},
    "mem ddr5 7200 pc5-57600": {"categoria_general": "Memorias", "subcategoria": "DDR5 7200"},
    "mem ddr5 4800 pc5-38400": {"categoria_general": "Memorias", "subcategoria": "DDR5 4800"},
    "cooler liquido cpu 120": {"categoria_general": "Accesorios", "subcategoria": "Cooler Líquido CPU 120mm"},
    "cpu amd ryzen 7 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 7 AM5 9xxx"},
    "monitor plano 21.45": {"categoria_general": "Monitores", "subcategoria": "Planos 21-22"},
    "mem ddr4 2666 pc4-21300": {"categoria_general": "Memorias", "subcategoria": "DDR4 2666"},
    "notebook amd ryzen 7": {"categoria_general": "Notebooks", "subcategoria": "Ryzen 7"},
    "video, pci exp radeon gam": {"categoria_general": "Tarjetas de Video", "subcategoria": "Radeon Gaming"},
    "video, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Tarjetas de Video"},
    "disco duro propietario": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros Propietarios"},
    "computadora aio core i7": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Core i7"},
    "estabilizador de tension": {"categoria_general": "Energía", "subcategoria": "Estabilizadores de Tensión"},
    "red, hub": {"categoria_general": "Redes", "subcategoria": "Hubs"},
    "muestra, otros": {"categoria_general": "Sin Clasificar", "subcategoria": "Muestras"},
    "disco duro 3.5 sata": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros 3.5 SATA"},
    "cases, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Gabinetes"},
    "ups interactivo": {"categoria_general": "UPS", "subcategoria": "Interactivo"},
    "monitor gaming plano 27": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 27"},
    "monitor plano 31.5": {"categoria_general": "Monitores", "subcategoria": "Planos 31-32"},
    "ms esd windows business": {"categoria_general": "Software", "subcategoria": "ESD Windows Business"},
    "scooter electrico, acc": {"categoria_general": "Accesorios", "subcategoria": "Scooters Eléctricos"},
    "t celulares, smartwatches": {"categoria_general": "Teléfonos Celulares", "subcategoria": "Smartwatches"},
    "consumo tanque tinta": {"categoria_general": "Suministros", "subcategoria": "Tanque de Tinta"},
    "t celulares basicos": {"categoria_general": "Teléfonos Celulares", "subcategoria": "Celulares Básicos"},
    "monitor plano 27": {"categoria_general": "Monitores", "subcategoria": "Planos 27"},
    "servicios otros": {"categoria_general": "Servicios", "subcategoria": "Otros"},
    "mouse inalambrico": {"categoria_general": "Periféricos", "subcategoria": "Mouse Inalámbrico"},
    "cpu amd ryzen 7 sam5 8xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 7 AM5 8xxx"},
    "chromebook": {"categoria_general": "Notebooks", "subcategoria": "Chromebook"},
    "suminist p/ plotters": {"categoria_general": "Suministros", "subcategoria": "Para Plotters"},
    "y rack": {"categoria_general": "Redes", "subcategoria": "Racks"},
    "monitor gaming curvo 27": {"categoria_general": "Monitores", "subcategoria": "Gaming Curvos 27"},
    "comercial laser": {"categoria_general": "Impresoras", "subcategoria": "Láser Comercial"},
    "mb cu9 s1851 ddr5": {"categoria_general": "Placas Madre", "subcategoria": "Core Ultra 9 S1851 DDR5"},
    "mem flash, compact flash": {"categoria_general": "Memorias", "subcategoria": "Compact Flash"},
    "ms aplicaciones": {"categoria_general": "Software", "subcategoria": "Aplicaciones Microsoft"},
    "cpu celeron s1200 gxxxx": {"categoria_general": "Procesadores", "subcategoria": "Celeron S1200 Gxxxx"},
    "teclado+mouse kit inalamb": {"categoria_general": "Periféricos", "subcategoria": "Kit Teclado y Mouse Inalámbrico"},
    "audio, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Audio"},
    "comercial ticketera": {"categoria_general": "Impresoras", "subcategoria": "Ticketera Comercial"},
    "suminist p/impres, tintas": {"categoria_general": "Suministros", "subcategoria": "Tintas para Impresoras"},
    "cases, fuente para": {"categoria_general": "Gabinetes", "subcategoria": "Con Fuente"},
    "mem ddr4 3600 pc4-28800": {"categoria_general": "Memorias", "subcategoria": "DDR4 3600"},
    "precio standard": {"categoria_general": "Sin Clasificar", "subcategoria": "Precio Estándar"},
    "cpu ci3 9xxx s1151-v2": {"categoria_general": "Procesadores", "subcategoria": "Core i3 9xxx S1151-v2"},
    "servicios ventas": {"categoria_general": "Servicios", "subcategoria": "Ventas"},
    "suminist p/tape backup": {"categoria_general": "Suministros", "subcategoria": "Para Tape Backup"},
    "comercial laser multi": {"categoria_general": "Impresoras", "subcategoria": "Láser Multifuncional Comercial"},
    "cpu cu7 2xx s1851": {"categoria_general": "Procesadores", "subcategoria": "Core Ultra 7 2xx S1851"},
    "monitores, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Monitores"},
    "cpu ci3 13xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i3 13xxx S1700"},
    "red, router y componentes": {"categoria_general": "Redes", "subcategoria": "Routers y Componentes"},
    "cpu ci5 9xxx s1151-v2": {"categoria_general": "Procesadores", "subcategoria": "Core i5 9xxx S1151-v2"},
    "imagenes, proyector": {"categoria_general": "Imágenes", "subcategoria": "Proyectores"},
    "cpu amd ryzen 3 sam4 3xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 3 AM4 3xxx"},
    "rep tb - pcba": {"categoria_general": "Repuestos", "subcategoria": "PCBA"},
    "repuestos varios": {"categoria_general": "Repuestos", "subcategoria": "Varios"},
    "barebones para pc": {"categoria_general": "Computadoras", "subcategoria": "Barebones PC"},
    "computadora gaming": {"categoria_general": "Computadoras", "subcategoria": "Gaming"},
    "audio, parlante usb": {"categoria_general": "Audio", "subcategoria": "Parlantes USB"},
    "teclado inalambrico": {"categoria_general": "Periféricos", "subcategoria": "Teclado Inalámbrico"},
    "mb cu9 s1851 ddr5 gaming": {"categoria_general": "Placas Madre", "subcategoria": "Core Ultra 9 S1851 DDR5 Gaming"},
    "teclado+mouse combo kit": {"categoria_general": "Periféricos", "subcategoria": "Kit Teclado y Mouse"},
    "mem flash, usb drive": {"categoria_general": "Memorias", "subcategoria": "USB Drive"},
    "mouse para gamers": {"categoria_general": "Periféricos", "subcategoria": "Mouse Gaming"},
    "cpu amd ryzen 7 sam4 5xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 7 AM4 5xxx"},
    "comercial tanque tinta mu": {"categoria_general": "Impresoras", "subcategoria": "Tanque de Tinta Multifuncional Comercial"},
    "ms licencias": {"categoria_general": "Software", "subcategoria": "Licencias Microsoft"},
    "suminist p/impres, bolsas": {"categoria_general": "Suministros", "subcategoria": "Bolsas para Impresoras"},
    "computadora workstation": {"categoria_general": "Computadoras", "subcategoria": "Workstation"},
    "tablet, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Tablets"},
    "mem ddr5 5600 pc5-44800": {"categoria_general": "Memorias", "subcategoria": "DDR5 5600"},
    "t celulares, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Teléfonos Celulares"},
    "ms esd windows consumer": {"categoria_general": "Software", "subcategoria": "ESD Windows Consumer"},
    "asterisk, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Asterisk"},
    "teclado usb": {"categoria_general": "Periféricos", "subcategoria": "Teclado USB"},
    "accesorios ensamblaje": {"categoria_general": "Accesorios", "subcategoria": "Ensamblaje"},
    "dvd-writer sata": {"categoria_general": "Almacenamiento", "subcategoria": "DVD-Writer SATA"},
    "cpu cu5 2xx s1851": {"categoria_general": "Procesadores", "subcategoria": "Core Ultra 5 2xx S1851"},
    "protec - mascaras kn95": {"categoria_general": "Protección", "subcategoria": "Máscaras KN95"},
    "mb socket am4 amd gaming": {"categoria_general": "Placas Madre", "subcategoria": "Socket AM4 AMD Gaming"},
    "mb ci9 s1200 ddr4": {"categoria_general": "Placas Madre", "subcategoria": "Core i9 S1200 DDR4"},
    "mb socket am5 amd gaming": {"categoria_general": "Placas Madre", "subcategoria": "Socket AM5 AMD Gaming"},
    "red, seguridad": {"categoria_general": "Redes", "subcategoria": "Seguridad"},
    "cpu ci3 12xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i3 12xxx S1700"},
    "mem sodimm ddr4 3200": {"categoria_general": "Memorias", "subcategoria": "SODIMM DDR4 3200"},
    "disco duro externo": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros Externos Genéricos"},
    "pizarras tactiles interc": {"categoria_general": "Monitores", "subcategoria": "Pizarras Táctiles Interactivas"},
    "ms esd office": {"categoria_general": "Software", "subcategoria": "ESD Office"},
    "serv, cdrom / dvd drives": {"categoria_general": "Servidores", "subcategoria": "CDROM/DVD Drives"},
    "mem ddr5 6400 pc5-51200": {"categoria_general": "Memorias", "subcategoria": "DDR5 6400"},
    "mem sodimm ddr5 5600": {"categoria_general": "Memorias", "subcategoria": "SODIMM DDR5 5600"},
    "comercial tanque tinta": {"categoria_general": "Impresoras", "subcategoria": "Tanque de Tinta Comercial"},
    "garantia extendida": {"categoria_general": "Servicios", "subcategoria": "Garantía Extendida"},
    "monitores / pizarras, acc": {"categoria_general": "Accesorios", "subcategoria": "Monitores y Pizarras"},
    "ms esd aplicaciones": {"categoria_general": "Software", "subcategoria": "ESD Aplicaciones"},
    "smart home - enchufes": {"categoria_general": "Smart Home", "subcategoria": "Enchufes"},
    "monitor portable 14": {"categoria_general": "Monitores", "subcategoria": "Portátiles 14"},
    "notebook amd ryzen 5": {"categoria_general": "Notebooks", "subcategoria": "Ryzen 5"},
    "mem flash, secure digital": {"categoria_general": "Memorias", "subcategoria": "Secure Digital"},
    "consolas ps5": {"categoria_general": "Consolas", "subcategoria": "PlayStation 5"},
    "materiales-administracion": {"categoria_general": "Suministros", "subcategoria": "Administrativos"},
    "cpu amd ryzen 5 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5 AM5 9xxx"},
    "mouse, touchpad, puntero": {"categoria_general": "Periféricos", "subcategoria": "Mouse, Touchpad y Punteros"},
    "ups, otros": {"categoria_general": "UPS", "subcategoria": "Otros"},
    "mb socket i c/cpu intel": {"categoria_general": "Placas Madre", "subcategoria": "Socket Intel con CPU"},
    "disco duro, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Discos Duros"},
    "cpu ci3 14xxx s1700": {"categoria_general": "Procesadores", "subcategoria": "Core i3 14xxx S1700"},
    "cpu pentium s1200 gxxxx": {"categoria_general": "Procesadores", "subcategoria": "Pentium S1200 Gxxxx"},
    "mem ddr5 7600 pc5-60800": {"categoria_general": "Memorias", "subcategoria": "DDR5 7600"},
    "monitor gaming plano 25": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 25"},
    "rep tb - otros hw": {"categoria_general": "Repuestos", "subcategoria": "Otros Hardware"},
    "mb ci9 s1700 ddr5": {"categoria_general": "Placas Madre", "subcategoria": "Core i9 S1700 DDR5"},
    "cases micro atx": {"categoria_general": "Gabinetes", "subcategoria": "Micro ATX"},
    "notebook amd ryzen 3": {"categoria_general": "Notebooks", "subcategoria": "Ryzen 3"},
    "monitores gaming": {"categoria_general": "Monitores", "subcategoria": "Gaming Genéricos"},
    "teclado para gamers": {"categoria_general": "Periféricos", "subcategoria": "Teclado Gaming"},
    "y patch cord - cobre": {"categoria_general": "Redes", "subcategoria": "Patch Cords de Cobre"},
    "internet, servicios": {"categoria_general": "Servicios", "subcategoria": "Internet"},
    "red, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Redes"},
    "computadora core i7": {"categoria_general": "Computadoras", "subcategoria": "Core i7"},
    "notebook celeron": {"categoria_general": "Notebooks", "subcategoria": "Celeron"},
    "ms esd office 365": {"categoria_general": "Software", "subcategoria": "ESD Office 365"},
    "consolas, otras marcas": {"categoria_general": "Consolas", "subcategoria": "Otras Marcas"},
    "computadora core i5": {"categoria_general": "Computadoras", "subcategoria": "Core i5"},
    "notebook, acc propietario": {"categoria_general": "Accesorios", "subcategoria": "Notebooks Propietarios"},
    "suminist p/impr, botellas": {"categoria_general": "Suministros", "subcategoria": "Botellas para Impresoras"},
    "mem ddr3 1600 pc3-12800": {"categoria_general": "Memorias", "subcategoria": "DDR3 1600"},
    "servidores, fuentes": {"categoria_general": "Servidores", "subcategoria": "Fuentes de Alimentación"},
    "imagenes, escaner de": {"categoria_general": "Imágenes", "subcategoria": "Escáneres"},
    "impresion_corte_diseño": {"categoria_general": "Impresoras", "subcategoria": "Impresión, Corte y Diseño"},
    "software, antivirus": {"categoria_general": "Software", "subcategoria": "Antivirus"},
    "cooler liquido cpu 240": {"categoria_general": "Accesorios", "subcategoria": "Cooler Líquido CPU 240mm"},
    "rep tb - lcd": {"categoria_general": "Repuestos", "subcategoria": "LCD"},
    "merchandising": {"categoria_general": "Suministros", "subcategoria": "Merchandising"},
    "mb ci9 s1700 ddr4 gaming": {"categoria_general": "Placas Madre", "subcategoria": "Core i9 S1700 DDR4 Gaming"},
    "notebook amd athlon": {"categoria_general": "Notebooks", "subcategoria": "Athlon"},
    "cpu amd ryzen 9 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 9 AM5 7xxx"},
    "mouse usb": {"categoria_general": "Periféricos", "subcategoria": "Mouse USB"},
    "cases, fan": {"categoria_general": "Accesorios", "subcategoria": "Ventiladores para Gabinetes"},
    "notebook amd": {"categoria_general": "Notebooks", "subcategoria": "AMD Genérico"},
    "energia r - panel solar": {"categoria_general": "Energía Renovable", "subcategoria": "Paneles Solares"},
    "ms windows consumer": {"categoria_general": "Software", "subcategoria": "Windows Consumer"},
    "cpu amd ryzen 5 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5 7000"},
    "cpu cu9 2xx s1851": {"categoria_general": "Procesadores", "subcategoria": "Core i9 200"},
    "ms licencias csp": {"categoria_general": "Software", "subcategoria": "Licencias CSP"},
    "productos sin clasificar": {"categoria_general": "Sin Clasificar", "subcategoria": "Sin Clasificar"},
    "cases atx ver2.0": {"categoria_general": "Gabinetes", "subcategoria": "ATX v2.0"},
    "cooler liquido cpu 360": {"categoria_general": "Refrigeración", "subcategoria": "Líquida 360mm"},
    "red wifi adaptadores usb": {"categoria_general": "Redes", "subcategoria": "Adaptadores Wi-Fi USB"},
    "energia r - panel solar": {"categoria_general": "Energía Renovable", "subcategoria": "Paneles Solares"},
    "ms windows consumer": {"categoria_general": "Software", "subcategoria": "Windows Consumer"},
    "cpu amd ryzen 5 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5 7000"},
    "cpu cu9 2xx s1851": {"categoria_general": "Procesadores", "subcategoria": "Core i9 200"},
    "ms licencias csp": {"categoria_general": "Software", "subcategoria": "Licencias CSP"},
    "productos sin clasificar": {"categoria_general": "Sin Clasificar", "subcategoria": "Sin Clasificar"},
    "cases atx ver2.0": {"categoria_general": "Gabinetes", "subcategoria": "ATX v2.0"},
    "cooler liquido cpu 360": {"categoria_general": "Refrigeración", "subcategoria": "Líquida 360mm"},
    "red wifi adaptadores usb": {"categoria_general": "Redes", "subcategoria": "Adaptadores Wi-Fi USB"},
}

def normalizar_categoria(categoria):
    """Normaliza una categoría eliminando espacios extra, convirtiendo a minúsculas y manejando comas."""
    if not isinstance(categoria, str):  # Maneja valores no string (e.g., NaN)
        return "sin_categoria"
    # Reemplaza separadores inconsistentes y normaliza
    categoria = categoria.strip().lower().replace("  ", " ").replace(", ", ",").replace(" ,", ",").replace(" - ", " ")
    return categoria

def mapear_categoria_dinamica(categoria, mapa=categoria_map):
    """Mapea una categoría usando el mapa estático o reglas dinámicas."""
    categoria_normalizada = normalizar_categoria(categoria)
    
    # Primero, verifica si está en el mapa estático
    if categoria_normalizada in mapa:
        return mapa[categoria_normalizada]
    
    # Reglas dinámicas basadas en patrones comunes
    # Procesadores AMD Ryzen
    if "cpu amd ryzen" in categoria_normalizada:
        if "sam5" in categoria_normalizada:
            if "7xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 7000"}
            elif "8xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 8000"}
            elif "9xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 9000"}
        elif "sam4" in categoria_normalizada:
            if "3xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 3000"}
            elif "4xxx" in categoria_normalizada:  # Nueva regla para Ryzen 4000
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 4000"}
            elif "5xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Ryzen 5000"}
        return {"categoria_general": "Procesadores", "subcategoria": "Ryzen Genérico"}

    # Procesadores Intel
    elif "cpu ci" in categoria_normalizada or "cpu cu" in categoria_normalizada:
        if "s1700" in categoria_normalizada:
            if "12xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Core 12xxx"}
            elif "13xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Core 13xxx"}
            elif "14xxx" in categoria_normalizada:
                return {"categoria_general": "Procesadores", "subcategoria": "Core 14xxx"}
        elif "s1851" in categoria_normalizada and "2xx" in categoria_normalizada:
            return {"categoria_general": "Procesadores", "subcategoria": "Core Ultra 200"}
        return {"categoria_general": "Procesadores", "subcategoria": "Core Genérico"}

    # Notebooks
    elif "notebook" in categoria_normalizada:
        if "core i" in categoria_normalizada:
            return {"categoria_general": "Notebooks", "subcategoria": "Core Genérico"}
        elif "ryzen" in categoria_normalizada:
            return {"categoria_general": "Notebooks", "subcategoria": "Ryzen Genérico"}
        elif "celeron" in categoria_normalizada:
            return {"categoria_general": "Notebooks", "subcategoria": "Celeron"}
        return {"categoria_general": "Notebooks", "subcategoria": "Genérico"}

    # Monitores
    elif "monitor" in categoria_normalizada:
        if "gaming" in categoria_normalizada:
            return {"categoria_general": "Monitores", "subcategoria": "Gaming Genérico"}
        elif "curvo" in categoria_normalizada:
            return {"categoria_general": "Monitores", "subcategoria": "Curvo Genérico"}
        elif "plano" in categoria_normalizada:
            return {"categoria_general": "Monitores", "subcategoria": "Plano Genérico"}
        return {"categoria_general": "Monitores", "subcategoria": "Genérico"}

    # Redes
    elif "red wifi" in categoria_normalizada or "red,wifi" in categoria_normalizada:
        if "adaptadores usb" in categoria_normalizada:
            return {"categoria_general": "Redes", "subcategoria": "Adaptadores Wi-Fi USB"}
        elif "access point" in categoria_normalizada or "ap interiores" in categoria_normalizada:
            return {"categoria_general": "Redes", "subcategoria": "Access Points"}
        return {"categoria_general": "Redes", "subcategoria": "WiFi Genérico"}

    # Impresoras
    elif "impresora" in categoria_normalizada:
        if "laser" in categoria_normalizada:
            return {"categoria_general": "Impresoras", "subcategoria": "Láser Genérica"}
        elif "tinta" in categoria_normalizada:
            return {"categoria_general": "Impresoras", "subcategoria": "Tinta Genérica"}
        return {"categoria_general": "Impresoras", "subcategoria": "Genérica"}

    # Servidores
    elif "servidores" in categoria_normalizada:
        if "nas/san" in categoria_normalizada:
            return {"categoria_general": "Servidores", "subcategoria": "NAS/SAN"}
        elif "software" in categoria_normalizada:
            return {"categoria_general": "Servidores", "subcategoria": "Software"}
        elif "tape backup" in categoria_normalizada:
            return {"categoria_general": "Servidores", "subcategoria": "Tape Backup"}
        elif "tarjetas" in categoria_normalizada:
            return {"categoria_general": "Servidores", "subcategoria": "Tarjetas"}
        return {"categoria_general": "Servidores", "subcategoria": "Genérico"}

    # Sillas
    elif "sillas gamer" in categoria_normalizada:
        return {"categoria_general": "Mobiliario", "subcategoria": "Sillas Gaming"}

    # Smart Home
    elif "smart home" in categoria_normalizada:
        if "camaras" in categoria_normalizada:
            return {"categoria_general": "Smart Home", "subcategoria": "Cámaras"}
        elif "enchufes" in categoria_normalizada:
            return {"categoria_general": "Smart Home", "subcategoria": "Enchufes"}
        elif "luces" in categoria_normalizada:
            return {"categoria_general": "Smart Home", "subcategoria": "Luces"}
        return {"categoria_general": "Smart Home", "subcategoria": "Genérico"}

    # Software
    elif "soft" in categoria_normalizada or "software" in categoria_normalizada:
        if "licenciamiento corp" in categoria_normalizada:
            return {"categoria_general": "Software", "subcategoria": "Licenciamiento Corporativo"}
        elif "antivirus" in categoria_normalizada:
            return {"categoria_general": "Software", "subcategoria": "Antivirus"}
        elif "otros" in categoria_normalizada:
            return {"categoria_general": "Software", "subcategoria": "Otros"}
        return {"categoria_general": "Software", "subcategoria": "Genérico"}

    # Almacenamiento
    elif "ssd" in categoria_normalizada:
        if "2.5 sata" in categoria_normalizada:
            return {"categoria_general": "Almacenamiento", "subcategoria": "SSDs 2.5 SATA"}
        elif "m.2 nvme" in categoria_normalizada:
            return {"categoria_general": "Almacenamiento", "subcategoria": "SSDs M.2 NVMe"}
        elif "m.2 sata" in categoria_normalizada:
            return {"categoria_general": "Almacenamiento", "subcategoria": "SSDs M.2 SATA"}
        return {"categoria_general": "Almacenamiento", "subcategoria": "SSDs Genéricos"}

    # Suministros
    elif "suminist" in categoria_normalizada:
        if "plotters" in categoria_normalizada:
            return {"categoria_general": "Suministros", "subcategoria": "Para Plotters"}
        elif "impr" in categoria_normalizada or "impres" in categoria_normalizada:
            if "botellas" in categoria_normalizada:
                return {"categoria_general": "Suministros", "subcategoria": "Botellas para Impresoras"}
            elif "bolsas" in categoria_normalizada:
                return {"categoria_general": "Suministros", "subcategoria": "Bolsas para Impresoras"}
            elif "cintas" in categoria_normalizada:
                return {"categoria_general": "Suministros", "subcategoria": "Cintas para Impresoras"}
            elif "tintas" in categoria_normalizada:
                return {"categoria_general": "Suministros", "subcategoria": "Tintas para Impresoras"}
        elif "tape backup" in categoria_normalizada:
            return {"categoria_general": "Suministros", "subcategoria": "Para Tape Backup"}
        return {"categoria_general": "Suministros", "subcategoria": "Genérico"}

    # Teléfonos y Tablets
    elif "t celulares" in categoria_normalizada or "t smartphones" in categoria_normalizada:
        if "basicos" in categoria_normalizada:
            return {"categoria_general": "Teléfonos Celulares", "subcategoria": "Celulares Básicos"}
        elif "accesorios" in categoria_normalizada:
            return {"categoria_general": "Accesorios", "subcategoria": "Teléfonos Celulares"}
        elif "smartwatches" in categoria_normalizada:
            return {"categoria_general": "Teléfonos Celulares", "subcategoria": "Smartwatches"}
        elif "android" in categoria_normalizada:
            return {"categoria_general": "Teléfonos Celulares", "subcategoria": "Smartphones Android"}
        return {"categoria_general": "Teléfonos Celulares", "subcategoria": "Genérico"}
    elif "tablet" in categoria_normalizada:
        if "android" in categoria_normalizada:
            return {"categoria_general": "Tablets", "subcategoria": "Android"}
        elif "windows" in categoria_normalizada:
            return {"categoria_general": "Tablets", "subcategoria": "Windows"}
        elif "accesorios" in categoria_normalizada:
            return {"categoria_general": "Accesorios", "subcategoria": "Tablets"}
        return {"categoria_general": "Tablets", "subcategoria": "Genérico"}

    # Periféricos
    elif "teclado" in categoria_normalizada or "mouse" in categoria_normalizada:
        if "inalambrico" in categoria_normalizada:
            return {"categoria_general": "Periféricos", "subcategoria": "Teclado o Mouse Inalámbrico"}
        elif "gamers" in categoria_normalizada:
            return {"categoria_general": "Periféricos", "subcategoria": "Teclado o Mouse Gaming"}
        elif "usb" in categoria_normalizada:
            return {"categoria_general": "Periféricos", "subcategoria": "Teclado o Mouse USB"}
        elif "combo kit" in categoria_normalizada:
            return {"categoria_general": "Periféricos", "subcategoria": "Kit Teclado y Mouse"}
        return {"categoria_general": "Periféricos", "subcategoria": "Genérico"}

    # Televisores
    elif "televisores" in categoria_normalizada:
        if "led/smart tv" in categoria_normalizada:
            return {"categoria_general": "Televisores", "subcategoria": "LED/Smart TV"}
        elif "racks" in categoria_normalizada:
            return {"categoria_general": "Accesorios", "subcategoria": "Racks para Televisores"}
        return {"categoria_general": "Televisores", "subcategoria": "Genérico"}

    # UPS
    elif "ups" in categoria_normalizada:
        if "interactivo" in categoria_normalizada:
            return {"categoria_general": "UPS", "subcategoria": "Interactivo"}
        elif "online" in categoria_normalizada:
            return {"categoria_general": "UPS", "subcategoria": "Online"}
        elif "accesorios" in categoria_normalizada:
            return {"categoria_general": "UPS", "subcategoria": "Accesorios"}
        elif "otros" in categoria_normalizada:
            return {"categoria_general": "UPS", "subcategoria": "Otros"}
        return {"categoria_general": "UPS", "subcategoria": "Genérico"}

    # Tarjetas de Video
    elif "video" in categoria_normalizada:
        if "nvidia gam" in categoria_normalizada:
            return {"categoria_general": "Tarjetas de Video", "subcategoria": "NVIDIA Gaming"}
        elif "radeon gam" in categoria_normalizada:
            return {"categoria_general": "Tarjetas de Video", "subcategoria": "Radeon Gaming"}
        elif "nvidia" in categoria_normalizada:
            return {"categoria_general": "Tarjetas de Video", "subcategoria": "NVIDIA Genéricas"}
        elif "accesorios" in categoria_normalizada:
            return {"categoria_general": "Accesorios", "subcategoria": "Tarjetas de Video"}
        return {"categoria_general": "Tarjetas de Video", "subcategoria": "Genérico"}

    # Casos especiales no mapeados
    if "precio standard" in categoria_normalizada:
        return {"categoria_general": "Sin Clasificar", "subcategoria": "Precio Standard"}
    elif "muestra, otros" in categoria_normalizada:
        return {"categoria_general": "Sin Clasificar", "subcategoria": "Muestras Otros"}

    # Categoría por defecto si no hay coincidencia
    print(f"Categoría no mapeada: {categoria_normalizada}")
    return {"categoria_general": "Sin Clasificar", "subcategoria": "No Mapeada"}