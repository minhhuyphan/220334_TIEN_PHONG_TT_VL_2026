#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎨 CUSTOM AI BANNER CREATOR (MODERN UI)
========================================
Quy trình:
1. Chọn ảnh sản phẩm (hoặc tạo mới)
2. Chọn/tạo background
3. Nhập text (tiêu đề, mô tả, CTA)
4. AI ghép tất cả → Banner hoàn chỉnh

AI Features:
- rembg: Tách nền
- Stable Diffusion: Tạo background
- Groq: Tạo text thông minh
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import threading
from datetime import datetime
import os
import json

# ================= COLORS & STYLES =================
COLORS = {
    'bg_main': '#1e1e2e',       # Dark blue-grey
    'bg_panel': '#262b3d',      # Lighter panel
    'text_main': '#ffffff',     # White
    'text_dim': '#a6accd',      # Dimmed text
    'accent': '#7aa2f7',        # Blue accent
    'accent_hover': '#5d86da',  # Darker blue
    'success': '#9ece6a',       # Green
    'warning': '#e0af68',       # Orange/Yellow
    'danger': '#f7768e',        # Red
    'input_bg': '#181825',      # Darker input
    'border': '#414868'         # Border color
}

FONTS = {
    'h1': ('Segoe UI', 24, 'bold'),
    'h2': ('Segoe UI', 16, 'bold'),
    'h3': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9)
}

# ================= AI IMPORTS =================
try:
    from rembg import remove
    HAS_REMBG = True
except:
    HAS_REMBG = False

try:
    from diffusers import StableDiffusionPipeline
    import torch
    HAS_SD = True
except Exception as e:
    HAS_SD = False

try:
    from groq import Groq
    HAS_GROQ = True
except:
    HAS_GROQ = False


class ModernButton(tk.Button):
    """Custom styled button"""
    def __init__(self, master, **kwargs):
        bg = kwargs.pop('bg', COLORS['accent'])
        fg = kwargs.pop('fg', 'white')
        font = kwargs.pop('font', FONTS['body'])
        
        super().__init__(master, bg=bg, fg=fg, font=font, 
                         relief=tk.FLAT, activebackground=COLORS['accent_hover'],
                         activeforeground='white', cursor='hand2', **kwargs)
        self.bind('<Enter>', lambda e: self.config(bg=COLORS['accent_hover']))
        self.bind('<Leave>', lambda e: self.config(bg=bg))


class ModernEntry(tk.Entry):
    """Custom styled entry"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLORS['input_bg'], fg='white', 
                         insertbackground='white', relief=tk.FLAT, 
                         font=FONTS['body'], highlightthickness=1,
                         highlightbackground=COLORS['border'],
                         highlightcolor=COLORS['accent'], **kwargs)

class CustomAIBannerCreator:
    """Tạo banner tùy chỉnh với giao diện hiện đại"""
    
    def __init__(self, root):
        self.root = root
        self.root.title('🎨 AI Custom Banner Creator')
        self.root.geometry('1400x900')
        self.root.configure(bg=COLORS['bg_main'])
        
        # Determine paths
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.output_folder = self.base_dir / 'output'
        self.output_folder.mkdir(exist_ok=True)
        
        # Data
        self.product_image_path = None
        self.background_image_path = None
        self.current_preview = None
        
        # AI Models
        self.sd_pipeline = None
        self.groq_client = None
        
        # Status variables
        self.status_var = tk.StringVar(value='Ready')
        
        # Input variables
        self.title_var = tk.StringVar(value='IPHONE 15 PRO')
        self.subtitle_var = tk.StringVar(value='Titanium Design. So Strong. So Light.')
        self.description_var = tk.StringVar(value='Experience the next level of performance.')
        self.cta_var = tk.StringVar(value='BUY NOW')
        self.bg_prompt_var = tk.StringVar(value='abstract modern technology background, blue and purple gradient, neon lights, 8k, minimalist')
        
        # Checkboxes
        self.use_rembg_var = tk.BooleanVar(value=HAS_REMBG)
        self.use_ai_text_var = tk.BooleanVar(value=HAS_GROQ)
        
        # Init AI
        self.check_ai_status()
        
        # Setup UI
        self.setup_ui()
        
        # Load AI in background
        threading.Thread(target=self.init_ai_models, daemon=True).start()

    def check_ai_status(self):
        print(f'Checking AI Status: Groq={HAS_GROQ}, SD={HAS_SD}, rembg={HAS_REMBG}')
        
    def init_ai_models(self):
        """Initialize AI models in background thread"""
        # Groq
        if HAS_GROQ:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                try:
                    self.groq_client = Groq(api_key=api_key)
                    self.update_status('✓ Groq API connected')
                except Exception as e:
                    print(f'Groq Init Error: {e}')
        
        # Stable Diffusion
        if HAS_SD:
            try:
                self.update_status('Charging Stable Diffusion...')
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                pass
            except Exception:
                pass
        
        self.update_status('Ready')
    
    def setup_ui(self):
        """Setup main interface layout"""
        
        # --- HEADER ---
        header = tk.Frame(self.root, bg=COLORS['bg_panel'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text='🎨 AI BANNER STUDIO', font=FONTS['h1'], 
                 bg=COLORS['bg_panel'], fg=COLORS['text_main']).pack(side=tk.LEFT, padx=30, pady=20)
        
        status_frame = tk.Frame(header, bg=COLORS['bg_panel'])
        status_frame.pack(side=tk.RIGHT, padx=30)
        
        self.ai_status_label = tk.Label(status_frame, text='Checking AI...', 
                                      font=FONTS['small'], bg=COLORS['bg_panel'], fg=COLORS['text_dim'])
        self.ai_status_label.pack()
        
        # --- MAIN CONTENT ---
        main = tk.Frame(self.root, bg=COLORS['bg_main'])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # LEFT PANEL (Controls)
        left_panel = tk.Frame(main, bg=COLORS['bg_panel'], width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.setup_controls(left_panel)
        
        # RIGHT PANEL (Preview)
        right_panel = tk.Frame(main, bg=COLORS['bg_main']) # Transparent main bg
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_preview(right_panel)
        
        # --- STATUS BAR ---
        statusbar = tk.Frame(self.root, bg=COLORS['bg_panel'], height=30)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_lbl = tk.Label(statusbar, textvariable=self.status_var, 
                                 bg=COLORS['bg_panel'], fg=COLORS['accent'],
                                 font=('Consolas', 9))
        self.status_lbl.pack(side=tk.LEFT, padx=10)

    def setup_controls(self, parent):
        """Setup controls in the left panel"""
        
        # Scrollable frame for controls
        canvas = tk.Canvas(parent, bg=COLORS['bg_panel'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_panel'])

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=430) # Width slightly less than parent
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # PADDING WRAPPER
        frame = tk.Frame(scrollable_frame, bg=COLORS['bg_panel'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 1. IMAGES SECTION
        self.create_section_label(frame, '1. VISUAL ASSETS')
        
        # Product Image
        p_frame = tk.Frame(frame, bg=COLORS['bg_panel'])
        p_frame.pack(fill=tk.X, pady=5)
        tk.Label(p_frame, text='Product Image', bg=COLORS['bg_panel'], fg=COLORS['text_dim'], font=FONTS['body']).pack(anchor='w')
        
        btn_row = tk.Frame(p_frame, bg=COLORS['bg_panel'])
        btn_row.pack(fill=tk.X, pady=5)
        
        ModernButton(btn_row, text='📂 Upload', command=self.choose_product_image, width=12).pack(side=tk.LEFT, padx=(0,5))
        ModernButton(btn_row, text='🎲 Sample', command=self.create_sample_product, bg=COLORS['bg_main'], width=10).pack(side=tk.LEFT)
        
        self.lbl_product = tk.Label(p_frame, text='No file selected', bg=COLORS['bg_panel'], fg=COLORS['text_dim'], font=FONTS['small'])
        self.lbl_product.pack(anchor='w', pady=2)
        
        # Checkbox Remove BG
        if HAS_REMBG:
            chk = tk.Checkbutton(p_frame, text='Auto Remove Background (AI)', variable=self.use_rembg_var,
                               bg=COLORS['bg_panel'], fg=COLORS['text_main'], selectcolor=COLORS['bg_main'],
                               activebackground=COLORS['bg_panel'], activeforeground=COLORS['text_main'])
            chk.pack(anchor='w', pady=5)
        
        # Background Image
        bg_frame = tk.Frame(frame, bg=COLORS['bg_panel'])
        bg_frame.pack(fill=tk.X, pady=(15, 5))
        tk.Label(bg_frame, text='Background', bg=COLORS['bg_panel'], fg=COLORS['text_dim'], font=FONTS['body']).pack(anchor='w')
        
        bg_btn_row = tk.Frame(bg_frame, bg=COLORS['bg_panel'])
        bg_btn_row.pack(fill=tk.X, pady=5)
        
        ModernButton(bg_btn_row, text='📂 Upload', command=self.choose_background_image, width=12).pack(side=tk.LEFT, padx=(0,5))
        
        if HAS_SD:
            ModernButton(bg_btn_row, text='✨ AI Generate', command=self.toggle_ai_bg_prompt, 
                       bg=COLORS['success'], width=15).pack(side=tk.LEFT)
        else:
            tk.Label(bg_btn_row, text='(AI BG Unavailable)', bg=COLORS['bg_panel'], fg=COLORS['text_dim']).pack(side=tk.LEFT)

        self.lbl_bg = tk.Label(bg_frame, text='No file selected', bg=COLORS['bg_panel'], fg=COLORS['text_dim'], font=FONTS['small'])
        self.lbl_bg.pack(anchor='w', pady=2)
        
        # AI Prompt area (Hidden by default)
        self.ai_prompt_frame = tk.Frame(frame, bg=COLORS['bg_panel'])
        tk.Label(self.ai_prompt_frame, text='AI Background Description:', bg=COLORS['bg_panel'], fg=COLORS['text_dim']).pack(anchor='w')
        self.txt_prompt = tk.Text(self.ai_prompt_frame, height=3, bg=COLORS['input_bg'], fg='white', 
                                font=FONTS['body'], relief=tk.FLAT, wrap=tk.WORD)
        self.txt_prompt.insert('1.0', self.bg_prompt_var.get())
        self.txt_prompt.pack(fill=tk.X, pady=5)
        ModernButton(self.ai_prompt_frame, text='Generate Now', command=self.generate_background_ai, bg=COLORS['success']).pack(fill=tk.X)
        
        
        # 2. CONTENT SECTION
        self.create_section_label(frame, '2. TEXT CONTENT', pady=(20, 10))
        
        # AI Text Generation Button
        if HAS_GROQ:
            ai_text_frame = tk.Frame(frame, bg=COLORS['bg_panel'])
            ai_text_frame.pack(fill=tk.X, pady=5)
            ModernButton(ai_text_frame, text='✨ Auto-Write Text with AI', command=self.generate_text_ai, 
                       bg=COLORS['accent'], fg='white').pack(fill=tk.X)

        # Fields
        self.create_input_field(frame, 'Headline', self.title_var)
        self.create_input_field(frame, 'Subtitle', self.subtitle_var)
        self.create_input_field(frame, 'Description', self.description_var)
        self.create_input_field(frame, 'Button Text (CTA)', self.cta_var)
        
        # 3. ACTION SECTION
        tk.Frame(frame, bg=COLORS['border'], height=1).pack(fill=tk.X, pady=20)
        
        ModernButton(frame, text='🚀 CREATE BANNER', command=self.create_banner, 
                   bg=COLORS['success'], font=('Segoe UI', 14, 'bold'), height=2).pack(fill=tk.X, pady=10)

        ModernButton(frame, text='🔄 Reset All', command=self.reset_form, 
                   bg=COLORS['bg_main'], fg=COLORS['text_dim']).pack(fill=tk.X)

    def create_section_label(self, parent, text, pady=(10, 10)):
        tk.Label(parent, text=text, font=FONTS['h3'], bg=COLORS['bg_panel'], 
                 fg=COLORS['text_main']).pack(anchor='w', pady=pady)

    def create_input_field(self, parent, label, variable):
        f = tk.Frame(parent, bg=COLORS['bg_panel'])
        f.pack(fill=tk.X, pady=5)
        tk.Label(f, text=label, bg=COLORS['bg_panel'], fg=COLORS['text_dim'], font=FONTS['small']).pack(anchor='w')
        ModernEntry(f, textvariable=variable).pack(fill=tk.X, pady=2, ipady=3)

    def setup_preview(self, parent):
        """Setup preview area"""
        
        # Toolbar
        toolbar = tk.Frame(parent, bg=COLORS['bg_main'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(toolbar, text='PREVIEW', font=FONTS['h2'], bg=COLORS['bg_main'], fg=COLORS['text_main']).pack(side=tk.LEFT)
        
        ModernButton(toolbar, text='💾 Save Image', command=self.save_banner, 
                   bg=COLORS['bg_panel'], width=15).pack(side=tk.RIGHT)
        
        # Canvas Container (Shadow effect)
        container = tk.Frame(parent, bg='#000000', padx=1, pady=1) # 1px border
        container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(container, bg='#11111b', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder text
        self.canvas.create_text(400, 200, text='Banner Preview Will Appear Here', 
                              fill=COLORS['border'], font=('Segoe UI', 20))

    # ================= LOGIC =================
    
    def update_status(self, msg):
        self.status_var.set(msg)
        self.root.update_idletasks()
        
    def choose_product_image(self):
        path = filedialog.askopenfilename(filetypes=[('Images', '*.png *.jpg *.jpeg')])
        if path:
            self.product_image_path = path
            self.lbl_product.config(text=f'✓ {Path(path).name}', fg=COLORS['success'])

    def create_sample_product(self):
        # Create a dummy product image
        img = Image.new('RGB', (400, 400), color='#3b4261')
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 100, 350, 300], fill='#7aa2f7')
        draw.text((120, 180), 'PRODUCT', fill='white', font=ImageFont.load_default())
        
        path = self.output_folder / 'sample_product.png'
        img.save(path)
        self.product_image_path = str(path)
        self.lbl_product.config(text=f'✓ Sample Created', fg=COLORS['success'])

    def choose_background_image(self):
        path = filedialog.askopenfilename(filetypes=[('Images', '*.png *.jpg *.jpeg')])
        if path:
            self.background_image_path = path
            self.lbl_bg.config(text=f'✓ {Path(path).name}', fg=COLORS['success'])
            # Hide prompt if manual BG selected
            self.ai_prompt_frame.pack_forget()

    def toggle_ai_bg_prompt(self):
        if self.ai_prompt_frame.winfo_ismapped():
            self.ai_prompt_frame.pack_forget()
        else:
            self.ai_prompt_frame.pack(fill=tk.X, after=self.lbl_bg, pady=10)

    def generate_background_ai(self):
        if not HAS_SD:
            messagebox.showerror('Error', 'Stable Diffusion module not available.')
            return

        prompt = self.txt_prompt.get('1.0', tk.END).strip()
        if not prompt: return
        
        self.update_status('🎨 Generating background... Please wait...')
        
        def run():
            try:
                # Load SD if not loaded
                if not self.sd_pipeline:
                    device = 'cuda' if torch.cuda.is_available() else 'cpu'
                    self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
                        'runwayml/stable-diffusion-v1-5',
                        torch_dtype=torch.float16 if device == 'cuda' else torch.float32
                    ).to(device)
                
                image = self.sd_pipeline(prompt, num_inference_steps=20, width=800, height=400).images[0]
                path = self.output_folder / f'bg_ai_{int(datetime.now().timestamp())}.png'
                image.save(path)
                
                self.background_image_path = str(path)
                self.root.after(0, lambda: self.lbl_bg.config(text='✓ AI Generate Success', fg=COLORS['success']))
                self.root.after(0, lambda: self.update_status('Background generated!'))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror('AI Error', str(e)))
                self.root.after(0, lambda: self.update_status('Generation failed'))
                
        threading.Thread(target=run, daemon=True).start()

    def generate_text_ai(self):
        if not HAS_GROQ or not self.groq_client:
            messagebox.showerror('Error', 'Groq API not configured.')
            return

        prod_name = self.title_var.get()
        self.update_status('📝 Writing marketing copy...')
        
        def run():
            try:
                system_prompt = 'You are a marketing expert. Output ONLY JSON. No markdown.'
                user_prompt = f'Write catchy copy for a banner for product: "{prod_name}". Return JSON with keys: title, subtitle, description, cta. Short and punchy.'
                
                completion = self.groq_client.chat.completions.create(
                    model='llama3-8b-8192',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    response_format={'type': 'json_object'}
                )
                
                content = completion.choices[0].message.content
                data = json.loads(content)
                
                self.root.after(0, lambda: self.title_var.set(data.get('title', prod_name)))
                self.root.after(0, lambda: self.subtitle_var.set(data.get('subtitle', '')))
                self.root.after(0, lambda: self.description_var.set(data.get('description', '')))
                self.root.after(0, lambda: self.cta_var.set(data.get('cta', 'BUY NOW')))
                self.root.after(0, lambda: self.update_status('Text generated!'))
                
            except Exception as e:
                print(e)
                self.root.after(0, lambda: self.update_status('Text gen failed'))
        
        threading.Thread(target=run, daemon=True).start()

    def create_banner(self):
        self.update_status('🚀 Processing Banner...')
        
        def run():
            try:
                # 1. Base Canvas
                W, H = 1200, 600
                banner = Image.new('RGB', (W, H), color='#1a1b26')
                
                # 2. Background
                if self.background_image_path:
                    bg = Image.open(self.background_image_path).convert('RGB')
                    bg = bg.resize((W, H), Image.Resampling.LANCZOS)
                    banner.paste(bg, (0,0))
                
                # 3. Product
                if self.product_image_path:
                    prod = Image.open(self.product_image_path).convert('RGBA')
                    
                    # Remove Background
                    if HAS_REMBG and self.use_rembg_var.get():
                        self.root.after(0, lambda: self.update_status('Removing Background...'))
                        try:
                            prod = remove(prod)
                        except Exception as e:
                            print(f'Rembg error: {e}')

                    # Resize & Place
                    h_target = int(H * 0.8)
                    ratio = prod.width / prod.height
                    w_target = int(h_target * ratio)
                    prod = prod.resize((w_target, h_target), Image.Resampling.LANCZOS)
                    
                    # Place on right side
                    x_pos = W - w_target - 50
                    y_pos = (H - h_target) // 2
                    banner.paste(prod, (x_pos, y_pos), prod)
                
                # 4. Text Overlay
                draw = ImageDraw.Draw(banner)
                
                # Determine font sizes
                try:
                    font_h1 = ImageFont.truetype('arial.ttf', 70)
                    font_h2 = ImageFont.truetype('arial.ttf', 35)
                    font_body = ImageFont.truetype('arial.ttf', 25)
                    font_cta = ImageFont.truetype('arial.ttf', 28)
                except:
                    font_h1 = ImageFont.load_default()
                    font_h2 = ImageFont.load_default()
                    font_body = ImageFont.load_default()
                    font_cta = ImageFont.load_default()

                # Draw Text (Left side)
                pad_x = 60
                curr_y = 120
                
                # Title
                draw.text((pad_x, curr_y), self.title_var.get().upper(), font=font_h1, fill='white')
                curr_y += 90
                
                # Subtitle
                draw.text((pad_x, curr_y), self.subtitle_var.get(), font=font_h2, fill=COLORS['accent'])
                curr_y += 50
                
                # Desc
                draw.text((pad_x, curr_y), self.description_var.get(), font=font_body, fill='#b4befe')
                curr_y += 100
                
                # CTA Button
                cta_text = self.cta_var.get()
                if cta_text:
                    btn_w, btn_h = 240, 60
                    draw.rectangle([pad_x, curr_y, pad_x + btn_w, curr_y + btn_h], fill=COLORS['success'])
                    
                    # Centered text in button
                    # Simple centering estimation
                    draw.text((pad_x + 40, curr_y + 15), cta_text, font=font_cta, fill='black')

                self.current_preview = banner
                self.show_preview(banner)
                self.root.after(0, lambda: self.update_status('Banner Created Successfully!'))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: messagebox.showerror('Error', str(e)))
        
        threading.Thread(target=run, daemon=True).start()

    def show_preview(self, image):
        # Resize for display
        w_canvas = self.canvas.winfo_width()
        h_canvas = self.canvas.winfo_height()
        
        if w_canvas < 10: w_canvas = 800
        
        # Calculate resize
        ratio = min(w_canvas / image.width, h_canvas / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        
        img_tk = ImageTk.PhotoImage(image.resize(new_size, Image.Resampling.LANCZOS))
        
        self.canvas.delete('all')
        # Center image
        x_center = w_canvas // 2
        y_center = h_canvas // 2
        self.canvas.create_image(x_center, y_center, image=img_tk)
        self.canvas.image = img_tk # Keep ref

    def save_banner(self):
        if self.current_preview:
            path = filedialog.asksaveasfilename(defaultext='.png', filetypes=[('PNG', '*.png')])
            if path:
                self.current_preview.save(path)
                messagebox.showinfo('Saved', f'Saved to {path}')

    def reset_form(self):
        self.product_image_path = None
        self.background_image_path = None
        self.lbl_product.config(text='No file selected', fg=COLORS['text_dim'])
        self.lbl_bg.config(text='No file selected', fg=COLORS['text_dim'])
        self.canvas.delete('all')
        self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                              text='Preview Area', fill=COLORS['border'], font=('Segoe UI', 20))
        self.status_var.set('Reset complete')

if __name__ == '__main__':
    root = tk.Tk()
    app = CustomAIBannerCreator(root)
    root.mainloop()

