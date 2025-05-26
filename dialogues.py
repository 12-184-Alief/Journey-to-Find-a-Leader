# dialogues.py
from constants import GameConstants as GC

GAME_DIALOGUES = {
    GC.STATE_STAGE_PROLOG: [
        "Raja: Bimas, anakku...",
        "Bimas: Ayahanda?",
        "Raja: Negeri kita membutuhkan pemimpin baru. Pergilah, temukan kebijaksanaan.",
        "Bimas: Baik, Ayahanda. Akan kulakukan."
    ],
    # Dialog untuk STATE_PRE_STAGE_1B sekarang dikelola oleh key spesifik ini:
    "pre_stage_1b_npc_dialog": [
        "Penduduk Desa: Selamat datang, ksatria!",
        "Penduduk Desa: Ada labirin berbahaya di depan sana.",
        "Penduduk Desa: Konon, tanaman berharga tumbuh di dalamnya, tapi dijaga ketat!",
        "Ksatria: Aku akan memeriksanya."
    ],
    # GC.STATE_PRE_STAGE_1B: [ # Key ini mungkin tidak lagi digunakan jika dialog di atas dipakai
    #    "Kepala Desa: Kamu kesatria utusan raja, ya?",
    #    "Kesatria: Benar. Ada apa dengan desa ini?",
    # ],
    GC.STATE_AFT_STAGE_1B: [ # Dialog setelah Pacman
        "Penduduk Desa: Kau berhasil! Luar biasa!",
        "Penduduk Desa: Perjalananmu belum berakhir. Langit memanggilmu selanjutnya.",
        "Ksatria: Aku mengerti. Terima kasih."
    ],
    # Anda perlu menambahkan dialog untuk state lain jika diperlukan
    # Misalnya untuk STATE_AWAN jika ada dialog, atau STATE_DESA_2, dll.
    # GC.STATE_AWAN: [
    #    "Suara Aneh: Siapa yang berani melintasi kerajaanku...?"
    # ],
    GC.STATE_STAGE_2: [ # Dialog untuk Spot Difference (jika ada sebelum game dimulai)
       "NPC Desa 2: Desa kami terkena kutukan ilusi!",
       "NPC Desa 2: Bisakah kau melihat perbedaan dan mematahkannya?"
    ],
    GC.STATE_DESA_2: [ # Dialog di Desa 2 setelah Spot Difference
        "NPC Desa 2: Terima kasih ksatria! Ilusi telah sirna!",
        "NPC Desa 2: Penyihir itu pasti ada di kuil terkutuk di puncak gunung!"
    ],
    GC.STATE_FINAL: [ # Dialog sebelum atau selama final stage
        "Penyihir: Jadi kau berhasil sampai sini, bocah ingusan!",
        "Ksatria: Kejahatanmu akan berakhir hari ini!"
    ],
    GC.STATE_GAME_OVER: [
        "Permainanmu telah berakhir...",
        "Namun, semangat kepemimpinan sejati tidak pernah padam.",
        "Tekan tombol di bawah untuk kembali ke Menu Utama."
     ]
}