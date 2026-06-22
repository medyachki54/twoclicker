[app]

# (str) Title of your application
title = Clicker

# (str) Package name
package.name = clicker

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives (ИСПРАВЛЕНО - теперь сборщик видит файлы!)
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.5

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# ==============================================================================
# Android specific
# ==============================================================================

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b


# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a symbolic link
android.copy_libs = 1

# (str) The Android arch to build for.
android.archs = armeabi-v7a, arm64-v8a

# ==============================================================================
# Buildozer settings
# ==============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
