import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame"],
    "includes": [],
    "include_files": [
        ('data/fonts', 'data/fonts'),
        # Ini akan menyalin isi 'data/images' ke folder 'data/images/entities' di hasil build
        ('data/images', 'data/images/entities'),
        ('data/audio', 'data/audio'),
        # Pastikan script Pygame Anda memuat aset sesuai dengan struktur folder ini
        # Contoh: gambar mungkin dimuat dari 'data/images/entities/nama_gambar.png'
        # audio dari 'data/audio/nama_suara.ogg'
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        icon="data/images/entities/Icon.ico",
        target_name="Journey to Find a Leader.exe"
    )
]

setup(
    name = "Journey to Find a Leader", # Nama ini untuk project/distribusi, tidak langsung nama file .exe
    version = "1.0",
    description = "Deskripsi Game Anda",
    options = {"build_exe": build_exe_options},
    executables = executables
)