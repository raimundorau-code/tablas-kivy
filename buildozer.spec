[app]
title = Tablas
package.name = tablas
package.domain = org.tuempresa
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,mp3,wav
# main.py debe estar en la raíz

requirements = python3,kivy==2.3.0,numpy==1.26.5
p4a.bootstrap = sdl2

android.api = 34
android.minapi = 24
android.ndk_api = 24
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
