# 📤 Instrucciones para Subir a GitHub

## Opción 1: Usando Git en la Terminal (Recomendado)

### Paso 1: Navega a la carpeta del proyecto
```bash
cd /home/anderson/Escritorio/Directorio/directorio_contactos
```

### Paso 2: Inicializar Git
```bash
git init
```

### Paso 3: Configurar Git (primera vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

### Paso 4: Agregar todos los archivos
```bash
git add .
```

### Paso 5: Hacer el primer commit
```bash
git commit -m "Directorio de Contactos - Proyecto inicial completo"
```

### Paso 6: Agregar el repositorio remoto
```bash
git remote add origin https://github.com/andersonseren/Directorio_contactos.git
```

### Paso 7: Cambiar rama a main (si es necesario)
```bash
git branch -M main
```

### Paso 8: Subir los archivos
```bash
git push -u origin main
```

---

## Opción 2: Usar GitHub Desktop (Si prefieres interfaz gráfica)

1. Descarga [GitHub Desktop](https://desktop.github.com)
2. Abre GitHub Desktop
3. Haz clic en "File" → "Clone Repository"
4. Ingresa: `https://github.com/andersonseren/Directorio_contactos.git`
5. Elige la ubicación
6. Haz clic en "Fetch Origin"
7. Copia los archivos del proyecto a esa carpeta
8. En GitHub Desktop, verás los cambios
9. Abajo a la izquierda, escribe un mensaje (ej: "Proyecto inicial")
10. Haz clic en "Commit to main"
11. Luego "Push origin"

---

## Opción 3: Subir Manualmente desde GitHub Web

1. Ve a https://github.com/andersonseren/Directorio_contactos
2. Haz clic en "Add file" → "Upload files"
3. Arrastra todos los archivos y carpetas
4. Haz clic en "Commit changes"

---

## Archivos que se subirán

```
directorio_contactos/
├── app.py
├── requirements.txt
├── Procfile
├── .env.example
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── registro.html
│   └── contactos.html
└── static/
    └── style.css
```

**NOTA**: El archivo `.env` NO se sube (está en .gitignore por seguridad)

---

## Verificar que se subió correctamente

1. Ve a https://github.com/andersonseren/Directorio_contactos
2. Deberías ver todos los archivos listados
3. Haz clic en "commits" para ver el historial

---

¡Listo! Una vez subido, puedes desplegar en Render 🚀
