import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame"],
    "includes": [],
    "include_files": [
        ('data/fonts', 'data/fonts'),
        ('data/images', 'data/images/entities'),
        ('data/audio', 'data/audio'),
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
    name = "Journey to Find a Leader",
    version = "1.0",
    description = "Deskripsi Game Anda",
    options = {"build_exe": build_exe_options},
    executables = executables
)