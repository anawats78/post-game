import pygame
import sys
import subprocess
import os

# การตั้งค่าหน้าจอ
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
FPS = 60

# โทนสี (ธีม Arcade มืดๆ คูลๆ)
BG_COLOR = (18, 20, 28)
PANEL_COLOR = (32, 36, 48)
TEXT_COLOR = (245, 246, 250)
ACCENT_COLOR = (0, 220, 255)
BUTTON_HOVER = (50, 56, 75)

class ArcadeHub:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Mini-Game Arcade")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # โหลดฟอนต์ระบบ
        self.title_font = pygame.font.SysFont("arial", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 28, bold=True)
        self.button_font = pygame.font.SysFont("arial", 32, bold=True)

        # สร้างปุ่ม 2 เกม
        self.btn_pose = pygame.Rect(280, 280, 400, 80)
        self.btn_mole = pygame.Rect(280, 400, 400, 80)
        self.btn_quit = pygame.Rect(380, 550, 200, 60)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_clicks(event.pos)

    def check_clicks(self, pos):
        # ถ้ารันผ่าน Python ปกติ ให้ใช้ sys.executable เพื่อความชัวร์
        python_exe = sys.executable 

        if self.btn_pose.collidepoint(pos):
            # 🌟 ลิงก์ไปหาไฟล์เกม Pose Match (ไฟล์ main.py ที่อยู่โฟลเดอร์เดียวกัน)
            self.launch_game([python_exe, "main.py"])
            
        elif self.btn_mole.collidepoint(pos):
            # 🌟 ลิงก์ไปหาไฟล์เกม Whack-a-Mole (อ้างอิง path เข้าโฟลเดอร์ไปหา game.py)
            mole_path = os.path.join("Whack-a-Mole", "game.py")
            self.launch_game([python_exe, mole_path])
            
        elif self.btn_quit.collidepoint(pos):
            self.running = False

    def launch_game(self, command):
        """ ปิดหน้าต่าง Hub ชั่วคราว -> รันเกม -> พอเกมจบ ค่อยเปิด Hub ขึ้นมาใหม่ """
        pygame.display.quit() # ปิดหน้าต่าง UI นี้ไปก่อนเพื่อคืนทรัพยากรให้เครื่อง
        
        try:
            # รันไฟล์เกมที่เลือก (โปรแกรมจะหยุดรอตรงนี้จนกว่าจะกด Quit ออกจากมินิเกม)
            subprocess.run(command)
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเปิดเกม: {e}")
            
        # พอเล่นจบและกดปิดมินิเกมแล้ว ให้ปลุกหน้าต่าง Hub กลับมาทำงานต่อ
        pygame.display.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw_ui(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # วาดหัวข้อ
        title = self.title_font.render("AI MINI-GAME ARCADE", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, 120)))
        
        subtitle = self.subtitle_font.render("Select a game to play", True, ACCENT_COLOR)
        self.screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_WIDTH//2, 180)))

        # วาดปุ่ม Pose Match
        self.draw_button(self.btn_pose, "1. POSE MATCH ", mouse_pos, (255, 90, 120))
        
        # วาดปุ่ม Whack-a-Mole
        self.draw_button(self.btn_mole, "2. WHACK-A-MOLE ", mouse_pos, (90, 255, 120))
        
        # วาดปุ่ม Quit
        self.draw_button(self.btn_quit, "QUIT", mouse_pos, (120, 130, 145), is_small=True)

    def draw_button(self, rect, text, mouse_pos, border_color, is_small=False):
        # เอฟเฟกต์เวลาเอาเมาส์ชี้
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else PANEL_COLOR
        
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, rect, width=3, border_radius=12)
        
        font = self.subtitle_font if is_small else self.button_font
        label = font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

if __name__ == "__main__":
    ArcadeHub().run()