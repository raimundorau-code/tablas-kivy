[app]
title = Tablas
package.name = tablas
package.domain = org.tuempresa
version = 0.1.0

# Código fuente
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,mp3,wav

# Dependencias (combo estable)
requirements = python3,kivy==2.2.1,numpy==1.26.4
p4a.bootstrap = sdl2

# Android (API objetivo y NDK fijo)
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.ndk = 25b
android.arch = arm64-v8a

# UI
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
