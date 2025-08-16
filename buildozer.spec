[app]
title = Tablas
package.name = tablas
package.domain = org.tuempresa
version = 0.1.0

# Código fuente
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,mp3,wav

# DEPENDENCIAS (combo estable)
# Nota: NO uses URLs de GitHub aquí; PyPI funciona mejor con p4a.
# Corregido: Se añadió la 'v' a la versión de numpy
requirements = python3,kivy==2.2.1,numpy==v1.26.4

# Bootstrap
p4a.bootstrap = sdl2

# Recipes recientes de python-for-android
p4a.fork = kivy
p4a.branch = develop

# Android
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.ndk = 25b
# Corregido: Se cambió 'android.arch' por 'android.archs'
android.archs = arm64-v8a

# UI
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
