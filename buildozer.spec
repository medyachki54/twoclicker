[app]

# (str) Title of your application
title = Кликер

# (str) Package name
package.name = twoclicker

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Path to the application icon
icon.filename = icon.png

# (list) Application requirements
requirements = python3,kivy

# (str) Application version / current project state
version = 4.0

# (int) Orientation (portrait, landscape or all)
orientation = portrait

# (bool) Use fullscreen or not
fullscreen = 1

# =========================================================
# Настройки Android
# =========================================================

# (int) Android API to use (Target SDK)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android Build-Tools version
android.build_tools_version = 33.0.0

# (bool) Use private data directory
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET

# (list) Architectures to build for
android.archs = armeabi-v7a, arm64-v8a

# (bool) Allow backup
android.allow_backup = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
