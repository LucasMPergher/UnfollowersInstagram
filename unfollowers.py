import json
import re
import os

def cargar_datos(archivo):
    """Carga datos desde JSON o HTML"""
    try:
        # Intentar cargar como JSON
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f), "json"
    except json.JSONDecodeError:
        # Si falla, intentar como HTML
        with open(archivo, 'r', encoding='utf-8') as f:
            content = f.read()
            return content, "html"
    except FileNotFoundError:
        return None, "no_existe"

def extraer_usernames_json(data, es_followers=True):
    """Extrae usernames desde estructura JSON"""
    usernames = set()
    if es_followers:
        # followers_1.json es una lista
        for user in data:
            username = user['string_list_data'][0]['value'].lower().strip()
            usernames.add(username)
    else:
        # following.json tiene estructura diferente
        for user in data['relationships_following']:
            username = user['title'].lower().strip()
            usernames.add(username)
    return usernames

def extraer_usernames_html(html_content):
    """Extrae usernames desde HTML"""
    usernames = set()
    
    # Buscar patrones de enlaces a perfiles de Instagram
    # Patrón 1: href="https://www.instagram.com/_u/username"
    pattern1 = r'href=["\']https://www\.instagram\.com/_u/([a-zA-Z0-9._-]+)["\']'
    matches = re.findall(pattern1, html_content)
    usernames.update([m.lower().strip() for m in matches])
    
    # Patrón 2: href="https://www.instagram.com/username/"
    pattern2 = r'href=["\']https://www\.instagram\.com/([a-zA-Z0-9._-]+)/?["\']'
    matches = re.findall(pattern2, html_content)
    usernames.update([m.lower().strip() for m in matches if m])
    
    # Patrón 3: Texto dentro de <a> tags
    pattern3 = r'<a[^>]*>([a-zA-Z0-9._-]+)</a>'
    matches = re.findall(pattern3, html_content)
    usernames.update([m.lower().strip() for m in matches if len(m) > 2])
    
    return usernames

# Cargar seguidores
seguidores_data, formato_followers = cargar_datos('followers_1.json')
if formato_followers == "json":
    seguidores = extraer_usernames_json(seguidores_data, es_followers=True)
else:
    seguidores = extraer_usernames_html(seguidores_data)
    print(f"ⓘ Archivo 'followers_1.json' cargado como HTML")

# Cargar seguidos
seguidos_data, formato_following = cargar_datos('following.json')
if formato_following == "json":
    seguidos = extraer_usernames_json(seguidos_data, es_followers=False)
else:
    seguidos = extraer_usernames_html(seguidos_data)
    print(f"ⓘ Archivo 'following.json' cargado como HTML")

# ============================================================
# SECCIÓN: Detectar quién te dejó de seguir (comparación histórica)
# ============================================================
seguidores_viejos = None
dejaron_de_seguir = None
archivos_antiguos = ['followers_1_old.json', 'followers_old.json', 'followers_1_backup.json']

# Buscar archivos antiguos
archivo_viejo_encontrado = None
for archivo_viejo in archivos_antiguos:
    if os.path.exists(archivo_viejo):
        archivo_viejo_encontrado = archivo_viejo
        break

# Si existe archivo viejo, calcular quién dejó de seguir
if archivo_viejo_encontrado:
    print(f"\n📂 Se encontró archivo histórico: {archivo_viejo_encontrado}")
    seguidores_viejos_data, formato_old = cargar_datos(archivo_viejo_encontrado)
    if formato_old != "no_existe":
        if formato_old == "json":
            seguidores_viejos = extraer_usernames_json(seguidores_viejos_data, es_followers=True)
        else:
            seguidores_viejos = extraer_usernames_html(seguidores_viejos_data)
        
        # Calcular quién te dejó de seguir
        dejaron_de_seguir = seguidores_viejos - seguidores
else:
    print(f"\n💡 Para detectar quién te dejó de seguir:")
    print(f"   1. Guarda una copia vieja: {archivos_antiguos[0]}")
    print(f"   O renómbrala como uno de estos: {', '.join(archivos_antiguos)}")

# Personas que NO te siguen
not_following_back = seguidos - seguidores

# Personas que vos no seguís
you_dont_follow_back = seguidores - seguidos

# Control: Verificar inconsistencias
inconsistencias = not_following_back & seguidores  # No debería haber nada aquí
inconsistencias2 = you_dont_follow_back & seguidos  # No debería haber nada aquí

# Mostrar totales
print("\n" + "="*50)
print("📊 RESUMEN ESTADÍSTICAS")
print("="*50)
print(f"Total de seguidores: {len(seguidores)}")
print(f"Total de seguidos: {len(seguidos)}")
print(f"🚫 NO te siguen de vuelta: {len(not_following_back)}")
print(f"👀 Vos no seguís de vuelta: {len(you_dont_follow_back)}")

# Mostrar advertencia si hay inconsistencias
if inconsistencias:
    print(f"\n⚠️ INCONSISTENCIAS DETECTADAS en 'no te siguen':")
    print(f"   Usuarios que aparecen en AMBAS listas: {len(inconsistencias)}")
    for user in sorted(inconsistencias)[:5]:
        print(f"   • {user}")
        
if inconsistencias2:
    print(f"\n⚠️ INCONSISTENCIAS DETECTADAS en 'vos no seguís':")
    print(f"   Usuarios que aparecen en AMBAS listas: {len(inconsistencias2)}")
    for user in sorted(inconsistencias2)[:5]:
        print(f"   • {user}")

print("="*50)

print("\n🚫 NO te siguen de vuelta ({} personas):".format(len(not_following_back)))
for user in sorted(not_following_back):
    print(f"  • {user}")

print("\n👀 Vos no seguís de vuelta ({} personas):".format(len(you_dont_follow_back)))
for user in sorted(you_dont_follow_back):
    print(f"  • {user}")

# ============================================================
# Mostrar quién te dejó de seguir (si hay archivo histórico)
# ============================================================
if dejaron_de_seguir is not None and len(dejaron_de_seguir) > 0:
    print("\n" + "="*50)
    print("💔 CAMBIOS HISTÓRICOS")
    print("="*50)
    print(f"\nComparación entre:")
    print(f"  Archivo viejo: {archivo_viejo_encontrado}")
    print(f"  Archivo nuevo: followers_1.json")
    print(f"\n💔 Te dejaron de seguir ({len(dejaron_de_seguir)} personas):")
    for user in sorted(dejaron_de_seguir):
        print(f"  • {user}")
    
    # Personas que empezaron a seguirte
    empezaron_a_seguir = seguidores - seguidores_viejos
    if len(empezaron_a_seguir) > 0:
        print(f"\n✨ Empezaron a seguirte ({len(empezaron_a_seguir)} personas):")
        for user in sorted(empezaron_a_seguir):
            print(f"  • {user}")

elif archivo_viejo_encontrado is None:
    print("\n" + "="*50)
    print("💡 PRÓXIMOS PASOS PARA DETECTAR CAMBIOS")
    print("="*50)
    print("\nPara saber quién te dejó de seguir con el tiempo:")
    print(f"  1. Guarda tu followers_1.json actual como:")
    print(f"     'followers_1_old.json'")
    print(f"  2. En el futuro, descarga nuevamente followers_1.json")
    print(f"  3. Ejecuta este script para comparar y ver cambios")
    print(f"\n✅ El script detectará automáticamente el archivo histórico")