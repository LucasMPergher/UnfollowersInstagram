# 📊 Unfollowers Instagram

Un script Python para analizar tus seguidores y seguidos en Instagram, identificando quién **no te sigue de vuelta** y a quién **vos no seguís de vuelta**.

## ✨ Características

- ✅ Compara automáticamente seguidores vs seguidos
- ✅ Soporta archivos en formato **JSON** y **HTML**
- ✅ Detección automática del formato de archivo
- ✅ Estadísticas completas y detalladas
- ✅ Validación de inconsistencias en los datos
- ✅ Normalización de nombres (minúsculas, espacios)
- ✅ Salida formateada y fácil de leer
- ✅ **Detecta cambios históricos** (quién te dejó de seguir)

## 📋 Requisitos

- Python 3.6+
- Módulos estándar: `json`, `re` (no necesita instalación)

## 🚀 Instalación

1. **Clona el repositorio**:
```bash
git clone https://github.com/tuusuario/UnfollowersInstagram.git
cd UnfollowersInstagram
```

2. **Descarga tus datos de Instagram**:
   - Ve a Instagram → Configuración → Privacidad y seguridad
   - Busca "Descargar información" o "Download your information"
   - Instagram te enviará un archivo comprimido en 24-96 horas

3. **Extrae los archivos necesarios**:
   Los archivos están en:
   ```
   connections/followers_and_following/
   ├── followers_1.json
   └── following.json
   ```

## 🎯 Uso

```bash
python unfollowers.py
```

**Importante**: Asegúrate de tener los archivos JSON en el directorio:
```
connections/followers_and_following/
├── followers_1.json
├── following.json
```

O modifica las rutas en el código según tu estructura.

## 📤 Salida del Script

```
==================================================
📊 RESUMEN ESTADÍSTICAS
==================================================
Total de seguidores: 450
Total de seguidos: 520
🚫 NO te siguen de vuelta: 95
👀 Vos no seguís de vuelta: 25
==================================================

🚫 NO te siguen de vuelta (95 personas):
  • usuario1
  • usuario2
  • usuario3
  ...

👀 Vos no seguís de vuelta (25 personas):
  • usuario4
  • usuario5
  ...
```

## 📊 Interpretación de Resultados

### 🚫 NO te siguen de vuelta
**Personas que TÚ SIGUES pero que NO te siguen**

Estos son usuarios a los que les prestas atención pero ellos no te siguen.

### 👀 Vos no seguís de vuelta
**Personas que TE SIGUEN pero que TÚ NO los sigues**

Estos son usuarios que te seguís pero tú no retribuyes el seguimiento.

## 🔄 Formatos Soportados

### ✅ JSON (Recomendado)
Formato estándar de descarga de datos de Instagram

### ✅ HTML
Archivos HTML exportados de Instagram

**El script detecta automáticamente el formato** sin necesidad de configuración.

## 💔 Detectar quién te dejó de seguir

### ¿Cómo funciona?

Este script puede comparar tus seguidores en **diferentes momentos del tiempo** para detectar quién te dejó de seguir.

### Instrucciones

**Paso 1**: Guarda una copia de tu archivo actual como:
```
followers_1_old.json
```

También funciona con estos nombres:
- `followers_old.json`
- `followers_1_backup.json`

**Paso 2**: En el futuro, descarga nuevos datos de Instagram:
- Instagram → Configuración → Privacidad y seguridad
- Descargar información

**Paso 3**: Reemplaza tu `followers_1.json` con la nueva descarga y ejecuta:
```bash
python unfollowers.py
```

### Salida esperada

```
==================================================
💔 CAMBIOS HISTÓRICOS
==================================================

Comparación entre:
  Archivo viejo: followers_1_old.json
  Archivo nuevo: followers_1.json

💔 Te dejaron de seguir (25 personas):
  • usuario1
  • usuario2
  • usuario3
  ...

✨ Empezaron a seguirte (5 personas):
  • usuario_nuevo1
  • usuario_nuevo2
  ...
```

### ⚠️ Cosas importantes

- ⚠️ Instagram no actualiza esto en tiempo real (tenés que volver a descargar datos)
- ⚠️ Es 100% seguro porque no das tu contraseña a nadie
- ⚠️ Funciona mejor que apps externas (que piden acceso a tu cuenta)
- ⚠️ No deja rastros en tu historial de Instagram

## ⚙️ Cómo Funciona el Script

```python
# Calcula quien NO te sigue (TÚ los sigues)
not_following_back = seguidos - seguidores

# Calcula a quien NO sigues (ELLOS te siguen)
you_dont_follow_back = seguidores - seguidos
```

**Proceso**:
1. Carga los archivos (JSON o HTML)
2. Extrae usernames y normaliza
3. Usa operaciones de sets para encontrar diferencias
4. Valida inconsistencias en los datos
5. Genera reporte con estadísticas

## ⚠️ Notas Importantes

- ⚠️ **Privacidad**: Este script solo funciona con TUS datos personales descargados
- ⚠️ **Datos desactualizados**: El download de Instagram no es real-time
- ⚠️ **Cambios frecuentes**: Los datos pueden cambiar entre descargas
- ⚠️ **Uso responsable**: No uses para automatizar acciones masivas

## 🐛 Solución de Problemas

### Error: `FileNotFoundError: [Errno 2] No such file`
**Solución**: Verifica la ruta de los archivos JSON. Asegúrate de que están en:
```
connections/followers_and_following/
```

### Error: `KeyError: 'value'`
**Solución**: La estructura del JSON puede haber cambiado. Intenta con archivos HTML o descarga nuevos datos.

### Ves inconsistencias en los resultados
**Solución**: 
- Descarga nuevos datos de Instagram
- Verifica que los archivos se descargaron al mismo tiempo
- Busca caracteres especiales o duplicados en los usernames

## 📝 Ejemplos de Uso

### Guardar resultados en archivo
```python
# Agregar al final del script
with open('unfollowers_report.txt', 'w', encoding='utf-8') as f:
    f.write(f"NO te siguen: {len(not_following_back)}\n")
    for user in sorted(not_following_back):
        f.write(f"{user}\n")
```

### Filtrar por criterio
```python
# Solo usuarios que no te siguen y tienen nombres cortos
nombres_cortos = {u for u in not_following_back if len(u) < 10}
```

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Ver archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Haz un Fork del proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agrega mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 💡 Ideas para Mejorar

- [ ] Exportar datos a CSV/Excel
- [ ] Gráficos visuales con matplotlib
- [ ] Interfaz gráfica con tkinter
- [ ] Integración con API de Instagram (donde sea posible)
- [x] Detectar cambios históricos (quién dejó de seguirte) ✅ IMPLEMENTADO

## ⭐ ¿Te fue útil?

Si este script te ayudó, ¡considera dejar una ⭐ en el repositorio!

---

**Desarrollado con ❤️ por Lucas**  
*Última actualización: 27 de marzo de 2026*

