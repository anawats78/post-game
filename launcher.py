import pygame
import sys
import subprocess
import os

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
FPS = 60

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

        self.title_font = pygame.font.SysFont("arial", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 28, bold=True)
        self.button_font = pygame.font.SysFont("arial", 32, bold=True)

        self.btn_pose = pygame.Rect(280, 250, 400, 70)
        self.btn_mole = pygame.Rect(280, 340, 400, 70)
        self.btn_campaign = pygame.Rect(230, 440, 500, 80)
        self.btn_quit = pygame.Rect(380, 540, 200, 60)

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
        python_exe = sys.executable 

        if self.btn_pose.collidepoint(pos):
            self.launch_game([python_exe, "main.py"])
            
        elif self.btn_mole.collidepoint(pos):
            mole_path = os.path.join("Whack-a-Mole", "game.py")
            self.launch_game([python_exe, mole_path])
            
        elif self.btn_campaign.collidepoint(pos):
            self.launch_campaign(python_exe)
            
        elif self.btn_quit.collidepoint(pos):
            self.running = False

    def launch_game(self, command):
        pygame.display.quit()
        try:
            subprocess.run(command)
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
        pygame.display.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def launch_campaign(self, python_exe):
        pygame.display.quit()
        
        # 1. สร้างตั๋วบอกเกมว่ากำลังเล่นโหมด Campaign
        with open("is_campaign.txt", "w") as f:
            f.write("yes")
            
        # 2. รันเกมที่ 1: Pose Match
        try:
            subprocess.run([python_exe, "main.py"])
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
            
        # ลบตั๋วทิ้ง
        if os.path.exists("is_campaign.txt"):
            os.remove("is_campaign.txt")
            
        # 3. ตรวจสอบว่ามีไฟล์ส่งต่อคะแนนไหม (ถ้ามีแปลว่าเล่นเกมแรกจบ ไม่ได้กดปิดกลางคัน)
        if os.path.exists("campaign_temp.txt"):
            # รันเกมที่ 2: ตีตุ่นต่อทันที
            mole_path = os.path.join("Whack-a-Mole", "game.py")
            try:
                subprocess.run([python_exe, mole_path])
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")
                
        pygame.display.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw_ui(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        title = self.title_font.render("AI MINI-GAME ARCADE", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, 110)))
        
        subtitle = self.subtitle_font.render("Select a game mode", True, ACCENT_COLOR)
        self.screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_WIDTH//2, 170)))

        self.draw_button(self.btn_pose, "POSE MATCH", mouse_pos, (255, 90, 120))
        self.draw_button(self.btn_mole, "WHACK-A-MOLE", mouse_pos, (90, 255, 120))
        
        # 🌟 ปุ่มโหมดใหม่ สีทองสะดุดตา
        self.draw_button(self.btn_campaign, "CAMPAIGN MODE", mouse_pos, (255, 215, 0))
        
        self.draw_button(self.btn_quit, "QUIT", mouse_pos, (120, 130, 145), is_small=True)

    def draw_button(self, rect, text, mouse_pos, border_color, is_small=False):
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else PANEL_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, rect, width=3, border_radius=12)
        
        font = self.subtitle_font if is_small else self.button_font
        label = font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

if __name__ == "__main__":
    ArcadeHub().run()