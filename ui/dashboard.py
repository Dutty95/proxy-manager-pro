import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import asyncio
import threading
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw
import io
import base64

from utils.proxy_rotator import ProxyRotator
from proxy_router import launch_app_with_proxy 
from utils.logger import get_logger
from proxy_loader import load_proxies
from proxy_checker import check_all_proxies
from utils.proxy_saver import save_proxies_by_type

logger = get_logger("dashboard")

class ProxyAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Router by Dotty")
        self.root.geometry("850x750")
        self.root.configure(bg="#f0f0f0")
        
        # Set custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)
        
        # Define colors
        self.primary_color = "#4a6fa5"  # Blue
        self.secondary_color = "#6b8e23"  # Olive green
        self.warning_color = "#d9534f"  # Red
        self.success_color = "#5cb85c"  # Green
        self.bg_color = "#f0f0f0"  # Light gray
        self.frame_bg = "#ffffff"  # White
        self.highlight_color = "#e9ecef"  # Light blue-gray for hover effects
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.frame_bg, relief="raised", borderwidth=2)
        self.style.configure("RoundedCard.TFrame", background=self.frame_bg, relief="raised", borderwidth=2)
        
        # Label styles
        self.style.configure("TLabel", background=self.bg_color, font=self.normal_font)
        self.style.configure("Header.TLabel", font=self.header_font, background=self.bg_color)
        self.style.configure("Title.TLabel", font=self.title_font, background=self.bg_color, foreground=self.primary_color)
        self.style.configure("Card.TLabel", background=self.frame_bg, font=self.normal_font)
        self.style.configure("CardHeader.TLabel", background=self.frame_bg, font=self.header_font, foreground=self.primary_color)
        
        # Button styles with improved appearance
        self.style.configure("Primary.TButton", font=self.normal_font, background=self.primary_color, relief="raised", borderwidth=2)
        self.style.map("Primary.TButton",
                    foreground=[("pressed", "white"), ("active", "white")],
                    background=[("pressed", "!disabled", "#3a5a85"), ("active", "!disabled", "#5a7fb5")])
        
        self.style.configure("Success.TButton", font=self.normal_font, background=self.success_color, relief="raised", borderwidth=2)
        self.style.map("Success.TButton",
                    foreground=[("pressed", "white"), ("active", "white")],
                    background=[("pressed", "!disabled", "#4a9d4a"), ("active", "!disabled", "#6cc86c")])
        
        self.style.configure("Warning.TButton", font=self.normal_font, background=self.warning_color, relief="raised", borderwidth=2)
        self.style.map("Warning.TButton",
                    foreground=[("pressed", "white"), ("active", "white")],
                    background=[("pressed", "!disabled", "#c9302c"), ("active", "!disabled", "#e96663")])
        
        # Variables
        self.proxy_file = tk.StringVar()
        self.categorized = {}
        self.rotator = None
        self.selected_proxy_type = tk.StringVar(value="SOCKS5")
        self.selected_proxy = tk.StringVar()
        self.app_path = tk.StringVar()
        self.country_filter = tk.StringVar(value="All Countries")
        
        self.browser_launched = False
        self.current_proxy = None
        
        # Create logo
        self.create_logo()
        
        # Build the UI
        self.build_ui()
        
    def create_logo(self):
        # Create a modern programmatically-generated logo
        try:
            # Create a gradient background
            width, height = 100, 100
            logo_img = Image.new('RGB', (width, height), color="white")
            draw = ImageDraw.Draw(logo_img)
            
            # Create a gradient background
            for y in range(height):
                r = int(74 + (106 - 74) * y / height)  # 4a6fa5 to 6a8fc5
                g = int(111 + (143 - 111) * y / height)
                b = int(165 + (197 - 165) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Draw a modern network/proxy icon
            # Center circle
            draw.ellipse([35, 35, 65, 65], outline="white", width=3)
            
            # Connection lines
            draw.line([50, 15, 50, 35], fill="white", width=3)  # Top
            draw.line([50, 65, 50, 85], fill="white", width=3)  # Bottom
            draw.line([15, 50, 35, 50], fill="white", width=3)  # Left
            draw.line([65, 50, 85, 50], fill="white", width=3)  # Right
            
            # Corner nodes
            draw.ellipse([10, 10, 20, 20], fill="white")
            draw.ellipse([80, 10, 90, 20], fill="white")
            draw.ellipse([10, 80, 20, 90], fill="white")
            draw.ellipse([80, 80, 90, 90], fill="white")
            
            # Convert to PhotoImage
            self.logo_image = ImageTk.PhotoImage(logo_img)
        except Exception as e:
            print(f"Error creating logo: {e}")
            # Fallback to no logo if there's an error
            self.logo_image = None

    def build_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced header with modern logo and title
        header_frame = ttk.Frame(main_container, style="TFrame")
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo with shadow effect on the left
        if self.logo_image:
            logo_frame = ttk.Frame(header_frame, style="Card.TFrame")
            logo_frame.pack(side='left', padx=(0, 20))
            
            logo_label = ttk.Label(logo_frame, image=self.logo_image, background=self.frame_bg)
            logo_label.pack(padx=5, pady=5)
        
        # Title and enhanced subtitle on the right
        title_frame = ttk.Frame(header_frame, style="TFrame")
        title_frame.pack(side='left')
        ttk.Label(title_frame, text="Proxy Router Pro", style="Title.TLabel").pack(anchor='w')
        ttk.Label(title_frame, text="Secure and efficient proxy management with advanced filtering", style="TLabel").pack(anchor='w')
        
        # Version info
        version_label = ttk.Label(header_frame, text="v1.0", foreground="#6c757d", background=self.bg_color)
        version_label.pack(side='right', padx=15)
        
        # Left panel (configuration) with rounded corners and shadow effect
        left_panel = ttk.Frame(main_container, style="Card.TFrame")
        left_panel.pack(side='left', fill='y', padx=(0, 15), pady=10, ipadx=15, ipady=15)
        
        # Configuration section title
        ttk.Label(left_panel, text="Configuration", style="Header.TLabel", background=self.frame_bg).pack(pady=(0, 10))
        
        # Proxy file selection
        ttk.Label(left_panel, text="Select Proxy List File:", background=self.frame_bg).pack(pady=(5, 2), anchor='w')
        proxy_file_frame = ttk.Frame(left_panel, style="TFrame", padding=5)
        proxy_file_frame.pack(fill='x')
        ttk.Entry(proxy_file_frame, textvariable=self.proxy_file, width=30, state='readonly').pack(side='left', padx=(0, 5))
        ttk.Button(proxy_file_frame, text="Browse", command=self.browse_proxy_file, style="Primary.TButton").pack(side='left')
        
        # Validate proxies button with enhanced styling
        self.validate_btn = ttk.Button(left_panel, text="✓ Validate Proxies", command=self.start_proxy_validation, 
                                     style="Success.TButton")
        self.validate_btn.pack(pady=10, fill='x', ipady=5)
        
        # App selection
        ttk.Label(left_panel, text="Select Application:", background=self.frame_bg).pack(pady=(10, 2), anchor='w')
        app_frame = ttk.Frame(left_panel, style="TFrame", padding=5)
        app_frame.pack(fill='x')
        self.app_entry = ttk.Entry(app_frame, textvariable=self.app_path, width=30, state='disabled')
        self.app_entry.pack(side='left', padx=(0, 5))
        self.browse_app_btn = ttk.Button(app_frame, text="Browse", command=self.browse_app, state='disabled')
        self.browse_app_btn.pack(side='left')
        
        # Proxy type selection
        ttk.Label(left_panel, text="Proxy Type:", background=self.frame_bg).pack(pady=(10, 2), anchor='w')
        proxy_types = ["SOCKS5", "SOCKS4", "HTTP"]
        self.proxy_menu = ttk.OptionMenu(left_panel, self.selected_proxy_type, "SOCKS5", *proxy_types)
        self.proxy_menu.pack(fill='x', pady=(0, 10))
        
        # Country filter
        ttk.Label(left_panel, text="Filter by Country:", background=self.frame_bg).pack(pady=(10, 2), anchor='w')
        self.country_filter_combo = ttk.Combobox(left_panel, textvariable=self.country_filter, state="readonly")
        self.country_filter_combo.pack(fill='x', pady=(0, 10))
        self.country_filter_combo['values'] = ["All Countries"]
        self.country_filter_combo.bind("<<ComboboxSelected>>", self.filter_proxies_by_country)
        
        # Routing buttons with enhanced styling
        ttk.Label(left_panel, text="Proxy Control:", background=self.frame_bg).pack(pady=(10, 5), anchor='w')
        btn_frame = ttk.Frame(left_panel, style="TFrame")
        btn_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(btn_frame, text="🚀 Start Routing", command=self.start_routing, 
                  style="Success.TButton").pack(side='left', padx=5, fill='x', expand=True, ipady=5)
        ttk.Button(btn_frame, text="🛑 Stop Routing", command=self.stop_routing, 
                  style="Warning.TButton").pack(side='left', padx=5, fill='x', expand=True, ipady=5)
        
        # Right panel (content)
        right_panel = ttk.Frame(main_container, style="TFrame")
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Top section - Proxy selector and table with enhanced styling
        top_section = ttk.Frame(right_panel, style="Card.TFrame")
        top_section.pack(fill='both', expand=True, pady=(0, 15), ipady=15)
        
        # Proxy selector dropdown
        selector_frame = ttk.Frame(top_section, style="TFrame", padding=10)
        selector_frame.pack(fill='x')
        ttk.Label(selector_frame, text="Select Proxy:", background=self.frame_bg).pack(side='left', padx=(0, 10))
        self.proxy_selector = ttk.Combobox(selector_frame, textvariable=self.selected_proxy, state="readonly", width=40)
        self.proxy_selector.pack(side='left', fill='x', expand=True)
        self.proxy_selector.bind("<<ComboboxSelected>>", self.switch_proxy)
        
        # Proxy table with enhanced columns
        ttk.Label(top_section, text="Validated Proxies", style="Header.TLabel", background=self.frame_bg).pack(pady=(5, 10))
        table_frame = ttk.Frame(top_section, style="TFrame", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10)
        
        # Enhanced proxy table with more columns and improved styling
        self.proxy_table = ttk.Treeview(table_frame, 
                                       columns=("IP", "Port", "Type", "Country", "City", "Speed", "Status"), 
                                       show='headings', 
                                       height=8,
                                       style="Rounded.Treeview")
        
        # Configure custom style for treeview
        self.style.configure("Rounded.Treeview", 
                          background=self.frame_bg,
                          fieldbackground=self.frame_bg,
                          foreground="#212529")
        
        self.style.configure("Rounded.Treeview.Heading", 
                          font=("Helvetica", 10, "bold"),
                          background=self.primary_color, 
                          foreground="white")
        
        self.style.map("Rounded.Treeview", 
                     background=[('selected', self.primary_color)],
                     foreground=[('selected', 'white')])
        
        self.proxy_table.heading("IP", text="IP Address")
        self.proxy_table.heading("Port", text="Port")
        self.proxy_table.heading("Type", text="Type")
        self.proxy_table.heading("Country", text="Country")
        self.proxy_table.heading("City", text="City")
        self.proxy_table.heading("Speed", text="Speed (ms)")
        self.proxy_table.heading("Status", text="Status")
        
        self.proxy_table.column("IP", width=120)
        self.proxy_table.column("Port", width=60)
        self.proxy_table.column("Type", width=70)
        self.proxy_table.column("Country", width=100)
        self.proxy_table.column("City", width=100)
        self.proxy_table.column("Speed", width=80)
        self.proxy_table.column("Status", width=80)
        
        self.proxy_table.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.proxy_table.yview)
        self.proxy_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Bottom section - Log output with country grouping
        bottom_section = ttk.Frame(right_panel, style="Card.TFrame")
        bottom_section.pack(fill='both', expand=True, ipady=15)
        
        # Log header with tabs for different views
        log_header_frame = ttk.Frame(bottom_section, style="TFrame", padding=5)
        log_header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        ttk.Label(log_header_frame, text="Log Output", style="CardHeader.TLabel").pack(side='left')
        
        # Add toggle for country grouping
        self.group_by_country = tk.BooleanVar(value=True)
        self.country_grouping_cb = ttk.Checkbutton(log_header_frame, text="Group by Country", 
                                                variable=self.group_by_country, 
                                                command=self.toggle_country_grouping,
                                                style="TCheckbutton")
        self.country_grouping_cb.pack(side='right')
        
        # Style for the checkbutton
        self.style.configure("TCheckbutton", background=self.frame_bg, font=self.normal_font)
        
        # Log content frame
        log_frame = ttk.Frame(bottom_section, style="TFrame", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Create a more visually appealing log text area
        self.log_text = tk.Text(log_frame, height=10, wrap='word', bg="#f8f9fa", fg="#212529",
                              font=self.normal_font, padx=5, pady=5, borderwidth=1, relief="solid")
        self.log_text.pack(side='left', fill='both', expand=True)
        self.log_text.configure(state='disabled')
        
        # Add country headers for grouping
        self.country_logs = {}
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        log_scrollbar.pack(side='right', fill='y')
        
    def filter_proxies_by_country(self, event=None):
        """Filter proxies by selected country"""
        if not self.categorized:
            return
            
        proxy_type = self.selected_proxy_type.get()
        proxies = self.categorized.get(proxy_type, [])
        
        selected_country = self.country_filter.get()
        if selected_country == "All Countries":
            self.display_proxies_in_table(proxies)
        else:
            filtered_proxies = [p for p in proxies if p.get("country", "Unknown") == selected_country]
            self.display_proxies_in_table(filtered_proxies)

    def browse_proxy_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self.proxy_file.set(path)
            self.log(f"📁 Selected proxy file: {path}")

    def browse_app(self):
        path = filedialog.askopenfilename(
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if path:
            self.app_path.set(path)

    def start_proxy_validation(self):
        if not self.proxy_file.get() or not os.path.exists(self.proxy_file.get()):
            messagebox.showerror("Missing File", "Proxy list not found!")
            return
        self.log("🔄 Validating proxies...")
        threading.Thread(target=lambda: asyncio.run(self.check_and_launch())).start()

    def start_routing(self):
        if not self.categorized:
            messagebox.showerror("No Proxies", "No validated proxies available. Please validate first.")
            return

        if not self.app_path.get():
            messagebox.showerror("Missing App", "Please select an app to launch.")
            return

        proxy_type = self.selected_proxy_type.get()
        proxies = self.categorized.get(proxy_type, [])
        if not proxies:
            messagebox.showerror("Unavailable", f"No working {proxy_type} proxies found.")
            return
            
        # Get the first proxy with its details
        proxy = proxies[0]
        ip = proxy.get("ip")
        port = proxy.get("port")
        country = proxy.get("country", "Unknown")
        city = proxy.get("city", "Unknown")
        speed = proxy.get("speed", "N/A")
        
        location_info = f" ({country}, {city})" if country != "Unknown" else ""
        speed_info = f", {speed} ms" if speed != "N/A" else ""
        
        # Check if proxy is flagged as abused
        abuse_warning = ""
        if proxy.get("is_abused", False):
            abuse_score = proxy.get("abuse_score", 0)
            abuse_warning = f" - ⚠️ Abuse score: {abuse_score}%"
        
        self.log(f"🚀 Starting app with proxy {ip}:{port}{location_info}{speed_info}{abuse_warning}")
        self.launch_proxy(proxy)

    async def check_and_launch(self):
        proxy_list = load_proxies(self.proxy_file.get())
        if not proxy_list:
            messagebox.showerror("No Proxies", "No proxies found in file.")
            return

        self.categorized = await check_all_proxies(proxy_list)
        save_proxies_by_type(self.categorized)

        proxy_type = self.selected_proxy_type.get()
        proxies = self.categorized.get(proxy_type, [])
        if not proxies:
            messagebox.showerror("Unavailable", f"No working {proxy_type} proxies found.")
            return

        self.display_proxies_in_table(proxies)
        self.populate_proxy_selector(proxies)

        self.rotator = ProxyRotator(self.categorized, interval_seconds=90, max_uses=3)
        first_proxy = proxies[0]
        self.selected_proxy.set(f"{first_proxy['ip']}:{first_proxy['port']}")
        self.current_proxy = first_proxy

        self.log(f"✅ Validated {len(proxies)} {proxy_type} proxies.")
        self.app_entry.config(state='normal')
        self.browse_app_btn.config(state='normal')

    def stop_routing(self):
        self.rotator = None
        self.browser_launched = False
        self.current_proxy = None
        self.log("🛑 Routing stopped.")

    def display_proxies_in_table(self, proxies):
        self.proxy_table.delete(*self.proxy_table.get_children())
        
        # Collect unique countries for the filter
        countries = set(["All Countries"])
        
        # Group proxies by country for summary
        country_stats = {}
        abuse_stats = {"good": 0, "flagged": 0, "abused": 0}
        
        for proxy in proxies:
            ip = proxy.get("ip")
            port = proxy.get("port")
            proxy_type = proxy.get("type", self.selected_proxy_type.get())
            country = proxy.get("country", "Unknown")
            city = proxy.get("city", "Unknown")
            speed = proxy.get("speed", "N/A")
            
            # Add country to the filter list and stats
            if country != "Unknown":
                countries.add(country)
                if country not in country_stats:
                    country_stats[country] = 0
                country_stats[country] += 1
            
            # Determine status based on abuse score
            status = "Good"
            status_tag = "good"
            if proxy.get("is_abused", False):
                abuse_score = proxy.get("abuse_score", 0)
                if abuse_score > 50:
                    status = f"Abused ({abuse_score}%)"
                    status_tag = "high_abuse"
                    abuse_stats["abused"] += 1
                else:
                    status = f"Flagged ({abuse_score}%)"
                    status_tag = "low_abuse"
                    abuse_stats["flagged"] += 1
            else:
                abuse_stats["good"] += 1
            
            # Insert into table with tags for coloring
            item_id = self.proxy_table.insert("", "end", values=(ip, port, proxy_type, country, city, 
                                                              f"{speed} ms" if speed != "N/A" else "N/A", 
                                                              status), 
                                            tags=(status_tag,))
            
            # Configure tag colors with hover effect
            self.proxy_table.tag_configure("good", background="#e6ffe6")
            self.proxy_table.tag_configure("low_abuse", background="#fff2e6")
            self.proxy_table.tag_configure("high_abuse", background="#ffe6e6")
        
        # Update country filter dropdown
        self.country_filter_combo['values'] = sorted(list(countries))
        
        # Log summary with country and abuse statistics
        summary = f"📋 Displayed {len(proxies)} proxies with location and status info.\n"
        
        # Add country breakdown
        if country_stats:
            self.log(summary)
            self.log("📊 Country breakdown:")
            for country, count in sorted(country_stats.items(), key=lambda x: x[1], reverse=True):
                self.log(f"   🌍 {country}: {count} proxies")
        
        # Add abuse stats
        if proxies:
            self.log("🔍 Status summary:")
            self.log(f"   ✅ Good: {abuse_stats['good']} proxies")
            if abuse_stats['flagged'] > 0:
                self.log(f"   ⚠️ Flagged: {abuse_stats['flagged']} proxies")
            if abuse_stats['abused'] > 0:
                self.log(f"   ❌ Abused: {abuse_stats['abused']} proxies")
        
        # If no country is selected, select "All Countries"
        if self.country_filter.get() not in countries:
            self.country_filter.set("All Countries")

    def populate_proxy_selector(self, proxies):
        proxy_list = [f"{p['ip']}:{p['port']}" for p in proxies]
        self.proxy_selector['values'] = proxy_list
        if proxy_list:
            self.selected_proxy.set(proxy_list[0])

    def launch_proxy(self, proxy):
        launch_app_with_proxy(proxy, proxy_type=self.selected_proxy_type.get(), app_path=self.app_path.get())
        self.browser_launched = True
        self.current_proxy = proxy

    def switch_proxy(self, event):
        selected = self.selected_proxy.get()
        ip, port = selected.split(":")
        for proxy in self.categorized.get(self.selected_proxy_type.get(), []):
            if proxy["ip"] == ip and str(proxy["port"]) == port:
                country = proxy.get("country", "Unknown")
                city = proxy.get("city", "Unknown")
                speed = proxy.get("speed", "N/A")
                
                location_info = f" ({country}, {city})" if country != "Unknown" else ""
                speed_info = f", {speed} ms" if speed != "N/A" else ""
                
                # Check if proxy is flagged as abused
                abuse_warning = ""
                if proxy.get("is_abused", False):
                    abuse_score = proxy.get("abuse_score", 0)
                    abuse_warning = f" - ⚠️ Abuse score: {abuse_score}%"
                
                self.log(f"🔁 Switching to proxy {ip}:{port}{location_info}{speed_info}{abuse_warning}")
                self.current_proxy = proxy
                launch_app_with_proxy(proxy, proxy_type=self.selected_proxy_type.get(), app_path=self.app_path.get())
                break

    def toggle_country_grouping(self):
        # Refresh the log display when toggling country grouping
        self.refresh_log_display()
    
    def refresh_log_display(self):
        # This method will be called when toggling between grouped and chronological views
        # For now, we'll just clear and redisplay all logs
        if hasattr(self, 'log_history'):
            self.log_text.configure(state='normal')
            self.log_text.delete(1.0, 'end')
            
            if self.group_by_country.get():
                # Display logs grouped by country
                for country, logs in self.country_logs.items():
                    if logs:  # Only show countries with logs
                        # Add country header
                        self.log_text.insert('end', f"\n=== {country} ===\n", "country_header")
                        
                        # Add logs for this country
                        for log_entry in logs:
                            timestamp, msg, tag = log_entry
                            self.log_text.insert('end', f"[{timestamp}] ", "timestamp")
                            self.log_text.insert('end', msg + "\n", tag)
            else:
                # Display logs chronologically
                for log_entry in self.log_history:
                    timestamp, msg, tag = log_entry
                    self.log_text.insert('end', f"[{timestamp}] ", "timestamp")
                    self.log_text.insert('end', msg + "\n", tag)
            
            self.log_text.configure(state='disabled')
            self.log_text.yview_moveto(1)
    
    def log(self, message):
        self.log_text.configure(state='normal')
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Determine message type and tag
        if "✅" in message:
            tag = "success"
        elif "🛑" in message or "failed" in message.lower() or "error" in message.lower():
            tag = "error"
        elif "🔄" in message:
            tag = "info"
        elif "🚀" in message:
            tag = "action"
        elif "🔁" in message:
            tag = "switch"
        else:
            tag = "normal"
        
        # Initialize log history if it doesn't exist
        if not hasattr(self, 'log_history'):
            self.log_history = []
        
        # Store the log entry
        self.log_history.append((timestamp, message, tag))
        
        # Extract country information if present
        country = "General"
        if "(" in message and ")" in message:
            # Try to extract country from messages like "... (United States, New York) ..."
            start_idx = message.find("(")
            end_idx = message.find(")")
            if start_idx < end_idx:
                location_info = message[start_idx+1:end_idx]
                if "," in location_info:
                    country = location_info.split(",")[0].strip()
        
        # Initialize country logs if needed
        if not hasattr(self, 'country_logs'):
            self.country_logs = {}
        
        # Add to country-specific logs
        if country not in self.country_logs:
            self.country_logs[country] = []
        self.country_logs[country].append((timestamp, message, tag))
        
        # Display based on current grouping setting
        if self.group_by_country.get():
            # Clear and redisplay all logs grouped by country
            self.refresh_log_display()
        else:
            # Just append the new log entry
            self.log_text.insert('end', f"[{timestamp}] ", "timestamp")
            self.log_text.insert('end', message + "\n", tag)
        
        # Configure tags for colored text
        self.log_text.tag_configure("timestamp", foreground="#666666")
        self.log_text.tag_configure("success", foreground="#5cb85c")
        self.log_text.tag_configure("error", foreground="#d9534f")
        self.log_text.tag_configure("info", foreground="#5bc0de")
        self.log_text.tag_configure("action", foreground="#f0ad4e")
        self.log_text.tag_configure("switch", foreground="#6b8e23")
        self.log_text.tag_configure("normal", foreground="#212529")
        self.log_text.tag_configure("country_header", foreground="#4a6fa5", font=self.header_font)
        
        # Highlight abused IPs
        if "Abuse score" in message:
            self.log_text.tag_configure("abuse_warning", background="#fff2e6")
            self.log_text.tag_add("abuse_warning", "end-2l", "end-1c")
        
        self.log_text.configure(state='disabled')
        self.log_text.yview_moveto(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyAppGUI(root)
    root.mainloop()
