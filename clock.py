import tkinter as tk
from datetime import datetime
import math

class ClassicClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Classic 24h Analog Clock")
        
        # Color Palette matching the HTML version
        self.face_color = "#fcfaf2"  # Classic cream
        self.rim_color = "#111111"   # Strong dark rim
        self.text_color = "#1a1a1a"
        self.second_hand_color = "#d00000"  # Classic red
        self.bg_color = "#f3f4f6"    # Light gray background for the window
        
        self.root.configure(bg=self.bg_color)
        self.root.geometry("650x850")

        # Fonts
        self.header_font = ("Times New Roman", 32, "bold")
        self.digital_font = ("Times New Roman", 42, "bold")
        self.number_font = ("Times New Roman", 24, "bold")

        # UI Layout
        self.setup_ui()
        
        # Start the update loop
        self.update_clock()

    def setup_ui(self):
        """Initializes the layout and widgets."""
        # 1. Date Header
        self.date_label = tk.Label(
            self.root, 
            text="JANUARY 15, 2026", 
            font=self.header_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.date_label.pack(pady=(40, 20))

        # 2. Analog Clock Canvas
        self.canvas_size = 500
        self.center = self.canvas_size / 2
        self.canvas = tk.Canvas(
            self.root, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg=self.bg_color, 
            highlightthickness=0
        )
        self.canvas.pack()

        # 3. Digital Clock Footer
        self.digital_label = tk.Label(
            self.root, 
            text="00:00:00", 
            font=self.digital_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.digital_label.pack(pady=20)

    def draw_face(self):
        """Draws the static parts of the clock face."""
        self.canvas.delete("face")
        
        # Draw Outer Rim
        rim_width = 15
        self.canvas.create_oval(
            rim_width, rim_width, 
            self.canvas_size - rim_width, self.canvas_size - rim_width,
            fill=self.face_color, 
            outline=self.rim_color, 
            width=rim_width,
            tags="face"
        )

        # Draw Numbers 1-12
        radius = (self.canvas_size / 2) * 0.75
        for i in range(1, 13):
            # Calculate position
            angle = math.radians(i * 30 - 90)
            x = self.center + radius * math.cos(angle)
            y = self.center + radius * math.sin(angle)
            
            self.canvas.create_text(
                x, y, 
                text=str(i), 
                fill="black", 
                font=self.number_font,
                tags="face"
            )

    def update_clock(self):
        """Main animation loop for the clock hands."""
        now = datetime.now()
        
        # Update Labels
        date_str = now.strftime("%B %d, %Y").upper()
        self.date_label.config(text=date_str)
        
        digital_str = now.strftime("%H:%M:%S")
        self.digital_label.config(text=digital_str)

        # Redraw hands
        self.canvas.delete("hands")
        self.draw_face() # Draw face under hands
        
        # Calculate rotations
        ms = now.microsecond / 1000000
        sec = now.second + ms
        min_ = now.minute + sec / 60
        hr = (now.hour % 12) + min_ / 60

        # Draw Hands
        # Seconds (Red)
        self.draw_hand(sec * 6, self.center * 0.85, 3, self.second_hand_color, "hands")
        # Minutes (Dark)
        self.draw_hand(min_ * 6, self.center * 0.75, 8, "#222222", "hands")
        # Hours (Thickest)
        self.draw_hand(hr * 30, self.center * 0.50, 14, "#000000", "hands")

        # Center Dot
        dot_radius = 12
        self.canvas.create_oval(
            self.center - dot_radius, self.center - dot_radius,
            self.center + dot_radius, self.center + dot_radius,
            fill=self.second_hand_color,
            outline="white",
            width=3,
            tags="hands"
        )

        # Schedule next update (approx 60fps for smooth sweep)
        self.root.after(16, self.update_clock)

    def draw_hand(self, degrees, length, width, color, tag):
        """Utility to draw a single hand at a specific angle."""
        angle = math.radians(degrees - 90)
        x = self.center + length * math.cos(angle)
        y = self.center + length * math.sin(angle)
        
        # We draw from center to calculated point
        self.canvas.create_line(
            self.center, self.center, x, y, 
            fill=color, 
            width=width, 
            capstyle=tk.ROUND, 
            tags=tag
        )

if __name__ == "__main__":
    root = tk.Tk()
    # Attempt to set a modern look on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    app = ClassicClock(root)
    root.mainloop()