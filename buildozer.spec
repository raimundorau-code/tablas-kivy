[app]
title = Tablas
package.name = tablas
package.domain = org.tuempresa
version = 0.1.0

source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,mp3,wav

# Kivy + NumPy (combo estable)
requirements = python3,kivy==2.3.0,numpy==1.26.5
p4a.bootstrap = sdl2
p4a.branch = develop

# Android
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.ndk = 25b
android.arch = arm64-v8a

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
