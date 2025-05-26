# main.py

from game import Game # Impor kelas utama game dari file game.py

# Jalankan kode ini hanya jika file ini dieksekusi langsung (bukan diimpor)
if __name__ == "__main__":
    game_instance = Game() # 1. Buat objek game (inisialisasi semua setup)
    game_instance.run()    # 2. Jalankan game loop utama