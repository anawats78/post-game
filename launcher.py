import pygame
import sys
import subprocess
import os
import csv

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
        
        self.state = "menu"

        self.title_font = pygame.font.SysFont("arial", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 28, bold=True)
        self.button_font = pygame.font.SysFont("arial", 32, bold=True)
        self.large_button_font = pygame.font.SysFont("arial", 36, bold=True)
        self.score_font = pygame.font.SysFont("consolas", 24) # ฟอนต์คะแนน

        self.btn_pose = pygame.Rect(280, 190, 400, 60)
        self.btn_mole = pygame.Rect(280, 270, 400, 60)
        self.btn_leaderboard = pygame.Rect(280, 350, 400, 60)
        
        self.btn_campaign = pygame.Rect(230, 460, 500, 80) 
        self.btn_quit = pygame.Rect(380, 570, 200, 60)
        self.btn_back = pygame.Rect(380, 630, 200, 60)

    def run(self):
        while self.running:
            self.handle_events()
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "menu":
                    self.check_clicks_menu(event.pos)
                elif self.state == "leaderboard":
                    self.check_clicks_leaderboard(event.pos)

    def check_clicks_menu(self, pos):
        python_exe = sys.executable 
        if self.btn_pose.collidepoint(pos):
            self.launch_game([python_exe, "main.py"])
        elif self.btn_mole.collidepoint(pos):
            mole_path = os.path.join("Whack-a-Mole", "game.py")
            self.launch_game([python_exe, mole_path])
        elif self.btn_leaderboard.collidepoint(pos):
            self.state = "leaderboard"
        elif self.btn_campaign.collidepoint(pos):
            self.launch_campaign(python_exe)
        elif self.btn_quit.collidepoint(pos):
            self.running = False

    def check_clicks_leaderboard(self, pos):
        if self.btn_back.collidepoint(pos):
            self.state = "menu"

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
        with open("is_campaign.txt", "w") as f:
            f.write("yes")
        try:
            subprocess.run([python_exe, "main.py"])
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
            
        if os.path.exists("is_campaign.txt"):
            os.remove("is_campaign.txt")
            
        if os.path.exists("campaign_temp.txt"):
            mole_path = os.path.join("Whack-a-Mole", "game.py")
            try:
                subprocess.run([python_exe, mole_path])
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")
        pygame.display.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # 🌟 ฟังก์ชันโหลดคะแนนเฉพาะโหมด Campaign (ดึงมาสูงสุด 20 อันดับ)
    def get_campaign_scores(self):
        paths = [os.path.join("Whack-a-Mole", "campaign_leaderboard.csv"), "campaign_leaderboard.csv"]
        for path in paths:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    data.sort(key=lambda x: int(x.get("score", 0)), reverse=True)
                    return data[:20]  # ดึง 20 อันดับ
        return []

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        title = self.title_font.render("AI MINI-GAME ARCADE", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, 80)))
        
        subtitle = self.subtitle_font.render("Select a Single Game", True, ACCENT_COLOR)
        self.screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_WIDTH//2, 140)))

        self.draw_button(self.btn_pose, "1. POSE MATCH", mouse_pos, (255, 90, 120))
        self.draw_button(self.btn_mole, "2. WHACK-A-MOLE", mouse_pos, (90, 255, 120))
        
        # เปลี่ยนชื่อปุ่มให้ชัดเจนว่าเป็นคะแนนของ Campaign
        self.draw_button(self.btn_leaderboard, "LEADERBOARD", mouse_pos, (230, 230, 250))
        
        pygame.draw.line(self.screen, (60, 65, 80), (180, 435), (780, 435), 3)
        
        self.draw_button(self.btn_campaign, "CAMPAIGN MODE", mouse_pos, (255, 215, 0), font=self.large_button_font)
        self.draw_button(self.btn_quit, "QUIT", mouse_pos, (120, 130, 145), is_small=True)

    def draw_leaderboard(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        title = self.title_font.render(" CAMPAIGN TOP 20 ", True, (255, 215, 0))
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, 80)))

        # 🌟 วาดกรอบใหญ่ตรงกลางกรอบเดียว 🌟
        pygame.draw.rect(self.screen, PANEL_COLOR, (130, 140, 700, 460), border_radius=12)

        scores = self.get_campaign_scores()
        
        if not scores:
            empty_text = self.subtitle_font.render("No scores yet. Play Campaign Mode!", True, (170, 180, 195))
            self.screen.blit(empty_text, empty_text.get_rect(center=(WINDOW_WIDTH//2, 350)))

        # วาดฝั่งซ้าย (อันดับ 1-10)
        for i in range(10):
            if i < len(scores):
                row = scores[i]
                name = str(row.get("name", "Player"))[:12]
                score = int(row.get("score", 0))
                text = f"{i+1:>2}. {name:<12} {score:>6}"
                lbl = self.score_font.render(text, True, TEXT_COLOR)
                self.screen.blit(lbl, (170, 170 + i * 40))

        # วาดฝั่งขวา (อันดับ 11-20)
        for i in range(10, 20):
            if i < len(scores):
                row = scores[i]
                name = str(row.get("name", "Player"))[:12]
                score = int(row.get("score", 0))
                text = f"{i+1:>2}. {name:<12} {score:>6}"
                lbl = self.score_font.render(text, True, TEXT_COLOR)
                self.screen.blit(lbl, (520, 170 + (i - 10) * 40))

        self.draw_button(self.btn_back, "BACK TO MENU", mouse_pos, (120, 130, 145), is_small=True)

    def draw_button(self, rect, text, mouse_pos, border_color, is_small=False, font=None):
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else PANEL_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, rect, width=3, border_radius=12)
        if font is None:
            font = self.subtitle_font if is_small else self.button_font
        label = font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

if __name__ == "__main__":
    ArcadeHub().run()