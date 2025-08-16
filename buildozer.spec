[app]
title = Tablas
package.name = tablas
package.domain = org.tuempresa
version = 0.1.0

# Código fuente
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,mp3,wav

# DEPENDENCIAS PROBADAS
# Corregido: Quitamos la versión de numpy para permitir que la receta
# estable de python-for-android use su versión interna probada (1.22.4).
requirements = python3,kivy==2.1.0,numpy

# Bootstrap
p4a.bootstrap = sdl2

# Se mantiene la rama 'master' (estable) de python-for-android.
p4a.fork = kivy
p4a.branch = master

# Android
# Se usa la API 31 (Android 12), un objetivo muy estable y compatible.
android.api = 31
android.minapi = 24
android.ndk_api = 24
android.ndk = 25b
android.archs = arm64-v8a

# UI
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
