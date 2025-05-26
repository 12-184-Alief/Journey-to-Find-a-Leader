# subtitle.py
import pygame

class Subtitle:
    def __init__(self, screen, font_size=28, text_color=(240,240,240), 
                 y_pos_from_bottom=100, typing_speed=30, 
                 bg_color=(20,20,20,200), padding=(25,15), line_spacing=5): # Warna BG lebih gelap, padding disesuaikan
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self.font_path = "data/fonts/dogicapixelbold.otf" # Pastikan path benar
        try:
            self.font = pygame.font.Font(self.font_path, font_size)
        except pygame.error:
            print(f"Font file '{self.font_path}' not found in Subtitle, using default font.")
            self.font = pygame.font.Font(None, font_size + 4) # Default font sedikit lebih besar

        self.text_color = text_color
        self.y_pos_from_bottom = y_pos_from_bottom 
        self.typing_speed = typing_speed 
        self.bg_color = bg_color
        self.padding = padding
        self.line_spacing = line_spacing # Jarak antar baris

        self.reset()

    def reset(self):
        self.full_text = "" 
        self.typed_text = "" 
        self.char_index = 0 
        self.last_char_time = pygame.time.get_ticks() 
        self.typing_finished = False
        self.rendered_lines_cache = [] # Cache untuk baris yang sudah di-render

    def show(self, text):
        self.reset() 
        self.full_text = text 
        self.typing_finished = (len(text) == 0)

    def update(self):
        if not self.typing_finished and self.char_index < len(self.full_text):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_char_time >= self.typing_speed:
                self.typed_text += self.full_text[self.char_index] 
                self.char_index += 1 
                self.last_char_time = current_time
                if self.char_index == len(self.full_text):
                    self.typing_finished = True
                self.rendered_lines_cache = [] # Invalidate cache saat teks berubah
        elif not self.full_text: 
            self.typing_finished = True

    def _wrap_text(self, text, max_width):
        """Helper function untuk word wrap."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            # Coba tambahkan kata ke baris saat ini
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # Jika baris saat ini bukan kosong, tambahkan ke lines
                if current_line:
                    lines.append(current_line.strip())
                # Mulai baris baru dengan kata saat ini
                # Jika kata itu sendiri lebih panjang dari max_width, ia akan tetap terpotong oleh render
                current_line = word + " "
        if current_line: # Tambahkan sisa baris terakhir
            lines.append(current_line.strip())
        return lines

    def draw(self):
        if not self.is_showing():
            return

        # Gunakan cache jika teks tidak berubah dan belum selesai mengetik sepenuhnya
        # Atau jika sudah selesai mengetik, cache akan selalu digunakan.
        if not self.rendered_lines_cache or (self.typing_finished and not self.rendered_lines_cache):
            max_text_width_in_box = self.screen_width * 0.85 - self.padding[0] * 2 # Maks 85% lebar layar untuk teks
            self.rendered_lines_cache = self._wrap_text(self.typed_text, max_text_width_in_box)
        
        if not self.rendered_lines_cache: # Jika tidak ada yang di-render (misal teks kosong)
            return

        # Hitung tinggi total semua baris teks
        total_text_height = 0
        line_surfaces = []
        max_line_width = 0
        for line_str in self.rendered_lines_cache:
            line_surface = self.font.render(line_str, True, self.text_color)
            line_surfaces.append(line_surface)
            total_text_height += line_surface.get_height()
            if line_surface.get_width() > max_line_width:
                max_line_width = line_surface.get_width()
        
        if len(line_surfaces) > 1:
            total_text_height += (len(line_surfaces) - 1) * self.line_spacing

        # Buat kotak latar belakang berdasarkan konten
        box_width = max_line_width + self.padding[0] * 2
        box_height = total_text_height + self.padding[1] * 2
        
        box_x = (self.screen_width - box_width) // 2
        box_y = self.screen_height - self.y_pos_from_bottom - box_height

        if self.bg_color:
            subtitle_box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            subtitle_box_surface.fill(self.bg_color)
            self.screen.blit(subtitle_box_surface, (box_x, box_y))

        # Gambar setiap baris teks
        current_y_text = box_y + self.padding[1]
        for line_surface in line_surfaces:
            # Pusatkan setiap baris teks di dalam kotak jika diinginkan, atau rata kiri
            # Rata kiri:
            text_blit_x = box_x + self.padding[0]
            # Rata tengah (horizontal):
            # text_blit_x = box_x + (box_width - line_surface.get_width()) // 2
            self.screen.blit(line_surface, (text_blit_x, current_y_text))
            current_y_text += line_surface.get_height() + self.line_spacing


    def is_animating(self):
        return not self.typing_finished and len(self.full_text) > 0

    def is_showing(self):
        return len(self.full_text) > 0

    def is_finished(self):
        return self.typing_finished
    
    def fast_forward(self):
        if not self.typing_finished:
            self.typed_text = self.full_text
            self.char_index = len(self.full_text)
            self.typing_finished = True
            self.rendered_lines_cache = [] # Invalidate cache
            print("Subtitle fast-forwarded.")