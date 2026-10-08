import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw
from typing import Optional, List

# Add current and parent dir to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from cpp_bridge import CppEngineBridge, SongInfo
from audio_player import AudioPlayer
from auth_manager import AuthManager, UserAccount

# Appearance Configuration - 100% Authentic Spotify Dark Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Spotify Brand Color Palette
COLOR_SPOTIFY_BLACK = "#000000"      # Deep sidebar black
COLOR_SPOTIFY_BG = "#121212"         # Main background dark grey
COLOR_SPOTIFY_CARD = "#181818"       # Card / row background
COLOR_SPOTIFY_CARD_HOVER = "#282828" # Hover background
COLOR_SPOTIFY_PLAYER = "#181818"     # Bottom player bar background
COLOR_SPOTIFY_BORDER = "#282828"     # Subtle dividers
COLOR_SPOTIFY_GREEN = "#1DB954"      # Iconic Spotify Brand Green
COLOR_SPOTIFY_GREEN_HOVER = "#1ED760"# Bright green hover
COLOR_SPOTIFY_TEXT_MAIN = "#FFFFFF"  # Primary white text
COLOR_SPOTIFY_TEXT_MUTED = "#B3B3B3" # Secondary grey text
COLOR_SPOTIFY_SLIDER_BG = "#4D4D4D"  # Unplayed progress bar grey

def create_circular_play_image(is_playing: bool, size: int = 56, bg_color=(29, 185, 84)) -> ctk.CTkImage:
    """Creates Spotify's iconic green circular play/pause button."""
    scale = 2
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Spotify Green circle
    margin = 2 * scale
    draw.ellipse((margin, margin, s - margin, s - margin), fill=bg_color)

    center = s // 2
    if is_playing:
        # Black Pause Bars
        bar_w = 5 * scale
        bar_h = 18 * scale
        gap = 6 * scale
        x1 = center - gap // 2 - bar_w
        x2 = center + gap // 2
        y1 = center - bar_h // 2
        y2 = center + bar_h // 2
        draw.rounded_rectangle([x1, y1, x1 + bar_w, y2], radius=2 * scale, fill=(0, 0, 0, 255))
        draw.rounded_rectangle([x2, y1, x2 + bar_w, y2], radius=2 * scale, fill=(0, 0, 0, 255))
    else:
        # Black Play Triangle
        tri_w = 16 * scale
        tri_h = 20 * scale
        x_left = center - tri_w // 3
        x_right = center + 2 * tri_w // 3
        y_top = center - tri_h // 2
        y_bottom = center + tri_h // 2
        draw.polygon([(x_left, y_top), (x_left, y_bottom), (x_right, center)], fill=(0, 0, 0, 255))

    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=resized, dark_image=resized, size=(size, size))

def create_liked_songs_badge(size: int = 48) -> ctk.CTkImage:
    """Creates the gradient purple Liked Songs badge."""
    img = Image.new("RGBA", (size, size), (69, 10, 245))
    draw = ImageDraw.Draw(img)
    # Heart symbol in white
    draw.ellipse((10, 10, size - 10, size - 10), fill=(100, 50, 255))
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

class SpotifyPlayerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spotify - SoundWave C++ DSA Engine")
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(fg_color=COLOR_SPOTIFY_BLACK)

        # 1. Initialize C++ Engine Bridge
        self.bridge = CppEngineBridge()

        # Load library from JSON
        json_path = os.path.join(parent_dir, "data", "library.json")
        if os.path.exists(json_path):
            self.bridge.load_file(json_path)

        # 2. Audio Player with song completion callback
        self.player = AudioPlayer(on_song_end=self.on_song_finished)

        # 3. Authentication & Role Manager (Default: Admin)
        self.auth = AuthManager()

        # State Variables
        self.current_song: Optional[SongInfo] = None
        self.is_seeking = False
        self.is_shuffled = False
        self.is_repeat = False
        self.active_tab = "home" # "home", "search", "library"

        # Cached play images
        self.img_play_icon = create_circular_play_image(is_playing=False, size=56)
        self.img_pause_icon = create_circular_play_image(is_playing=True, size=56)

        # Build 3-part Spotify layout: Left Sidebar, Main Scroll Content, Bottom Sticky Player Bar
        self._build_layout()

        # Load initial playlist & songs
        self.load_playlist_view(self.bridge.get_active_playlist())

        # Update initial authentication UI
        self.update_auth_ui()

        # Start 100ms smooth audio progress & mixer loop
        self.after(100, self._update_playback_loop)

    def _build_layout(self):
        self.grid_rowconfigure(0, weight=1) # Main Viewport
        self.grid_rowconfigure(1, weight=0) # Bottom Sticky Player Bar
        self.grid_columnconfigure(0, weight=0) # Left Sidebar
        self.grid_columnconfigure(1, weight=1) # Center Content

        self._build_sidebar()
        self._build_main_viewport()
        self._build_bottom_player_bar()

    # -------------------------------------------------------------
    # 1. SPOTIFY LEFT SIDEBAR
    # -------------------------------------------------------------
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=250, corner_radius=0, fg_color=COLOR_SPOTIFY_BLACK,
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)

        # Spotify Logo & Brand
        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.pack(fill="x", padx=24, pady=(22, 18))

        lbl_logo_icon = ctk.CTkLabel(
            logo_box, text="●)))", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_SPOTIFY_GREEN
        )
        lbl_logo_icon.pack(side="left", padx=(0, 8))

        lbl_spotify = ctk.CTkLabel(
            logo_box, text="Spotify", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN
        )
        lbl_spotify.pack(side="left")

        # Top Navigation Menu: Home, Search, Your Library
        nav_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_box.pack(fill="x", padx=12, pady=(0, 10))

        self.btn_nav_home = self._create_sidebar_nav_item(nav_box, "🏠  Home", lambda: self.set_active_tab("home"))
        self.btn_nav_search = self._create_sidebar_nav_item(nav_box, "🔍  Search", lambda: self.set_active_tab("search"))
        self.btn_nav_library = self._create_sidebar_nav_item(nav_box, "📚  Your Library", lambda: self.set_active_tab("library"))

        # Divider
        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLOR_SPOTIFY_BORDER).pack(fill="x", padx=20, pady=12)

        # Action Buttons: Create Playlist & Liked Songs
        actions_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        actions_box.pack(fill="x", padx=12, pady=(0, 8))

        btn_create_pl = ctk.CTkButton(
            actions_box, text="➕  Create Playlist", anchor="w",
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=13, weight="bold"),
            height=38, command=self.on_create_playlist_dialog
        )
        btn_create_pl.pack(fill="x", pady=2)

        btn_liked_songs = ctk.CTkButton(
            actions_box, text="💜  Liked Songs", anchor="w",
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MAIN, font=ctk.CTkFont(size=13, weight="bold"),
            height=38, command=lambda: self.load_playlist_view("Favorites")
        )
        btn_liked_songs.pack(fill="x", pady=2)

        btn_import_song = ctk.CTkButton(
            actions_box, text="🎵  Add Local File", anchor="w",
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_GREEN, font=ctk.CTkFont(size=13, weight="bold"),
            height=38, command=self.on_add_local_song
        )
        btn_import_song.pack(fill="x", pady=2)

        # Admin Dashboard Button (Highlighted)
        self.btn_admin_panel = ctk.CTkButton(
            actions_box, text="👑  Admin Dashboard", anchor="w",
            fg_color="#143422", hover_color="#1B472E",
            text_color=COLOR_SPOTIFY_GREEN, font=ctk.CTkFont(size=13, weight="bold"),
            height=38, command=self.open_admin_dashboard
        )
        self.btn_admin_panel.pack(fill="x", pady=2)

        # Scrollable Playlists List
        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLOR_SPOTIFY_BORDER).pack(fill="x", padx=20, pady=8)

        self.playlist_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", height=200)
        self.playlist_scroll.pack(fill="both", expand=True, padx=8, pady=4)
        self.refresh_sidebar_playlists()



    def _create_sidebar_nav_item(self, parent, text, command):
        btn = ctk.CTkButton(
            parent, text=text, anchor="w",
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=14, weight="bold"),
            height=40, command=command
        )
        btn.pack(fill="x", pady=2)
        return btn

    def refresh_sidebar_playlists(self):
        for w in self.playlist_scroll.winfo_children():
            w.destroy()

        names = self.bridge.get_playlist_names()
        for name in names:
            if name in ("All Songs", "Favorites"):
                continue
            btn = ctk.CTkButton(
                self.playlist_scroll, text=name, anchor="w",
                fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
                text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=13),
                height=32, command=lambda n=name: self.load_playlist_view(n)
            )
            btn.pack(fill="x", pady=1)

    # -------------------------------------------------------------
    # 2. MAIN VIEWPORT (TOP BAR + HERO HEADER + SONG LIST)
    # -------------------------------------------------------------
    def _build_main_viewport(self):
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_SPOTIFY_BG, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Top Bar: Nav Arrows, Spotify Search Bar, Profile Pill
        self._build_top_bar()

        # Scrollable Content Area (Spotify Playlist & Track Table)
        self.content_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.content_scroll.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Hero Banner
        self._build_hero_banner()

        # Playlist Action Bar (Large Round Green Play Button, Like, Shuffle)
        self._build_playlist_action_bar()

        # Table Column Headers
        self._build_table_headers()

        # Table Rows Container
        self.songs_table_frame = ctk.CTkFrame(self.content_scroll, fg_color="transparent")
        self.songs_table_frame.pack(fill="x", padx=32, pady=(0, 20))

    def _build_top_bar(self):
        top_bar = ctk.CTkFrame(self.main_container, height=64, fg_color="#101010")
        top_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        top_bar.pack_propagate(False)

        # Left: Back / Forward Circular Navigation Buttons
        arrows_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        arrows_box.pack(side="left", padx=(24, 16))

        btn_back = ctk.CTkButton(
            arrows_box, text="<", width=34, height=34, corner_radius=17,
            fg_color="#0A0A0A", hover_color="#1F1F1F", text_color=COLOR_SPOTIFY_TEXT_MAIN,
            font=ctk.CTkFont(size=16, weight="bold"), command=self.on_prev_track
        )
        btn_back.pack(side="left", padx=3)

        btn_fwd = ctk.CTkButton(
            arrows_box, text=">", width=34, height=34, corner_radius=17,
            fg_color="#0A0A0A", hover_color="#1F1F1F", text_color=COLOR_SPOTIFY_TEXT_MAIN,
            font=ctk.CTkFont(size=16, weight="bold"), command=self.on_next_track
        )
        btn_fwd.pack(side="left", padx=3)

        # Center: Spotify Pill Search Bar
        self.search_entry = ctk.CTkEntry(
            top_bar, placeholder_text="What do you want to play? (Trie O(L))...",
            width=360, height=40, corner_radius=20,
            fg_color="#242424", border_width=0,
            text_color=COLOR_SPOTIFY_TEXT_MAIN, placeholder_text_color="#757575",
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.on_search_key)

        # Right: User Profile Pill
        self.btn_profile = ctk.CTkButton(
            top_bar, text="👑  Admin (admin)", width=145, height=36, corner_radius=18,
            fg_color="#0A0A0A", hover_color="#1F1F1F", text_color=COLOR_SPOTIFY_GREEN,
            font=ctk.CTkFont(size=13, weight="bold"), command=self.open_profile_menu
        )
        self.btn_profile.pack(side="right", padx=24)

    def _build_hero_banner(self):
        self.hero_box = ctk.CTkFrame(self.content_scroll, height=220, fg_color="#202020", corner_radius=0)
        self.hero_box.pack(fill="x", padx=0, pady=0)
        self.hero_box.pack_propagate(False)

        hero_inner = ctk.CTkFrame(self.hero_box, fg_color="transparent")
        hero_inner.pack(fill="both", expand=True, padx=32, pady=24)

        # Album Art Big Square Thumbnail (170x170)
        art_frame = ctk.CTkFrame(hero_inner, width=170, height=170, corner_radius=8, fg_color="#282828")
        art_frame.pack(side="left", padx=(0, 24))
        art_frame.pack_propagate(False)

        self.lbl_big_art = ctk.CTkLabel(
            art_frame, text="🎵", font=ctk.CTkFont(size=64), text_color=COLOR_SPOTIFY_GREEN
        )
        self.lbl_big_art.pack(expand=True)

        # Metadata Texts
        meta_frame = ctk.CTkFrame(hero_inner, fg_color="transparent")
        meta_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            meta_frame, text="PUBLIC PLAYLIST", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN
        ).pack(anchor="w", pady=(8, 2))

        self.lbl_playlist_title = ctk.CTkLabel(
            meta_frame, text="All Songs", font=ctk.CTkFont(size=44, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN
        )
        self.lbl_playlist_title.pack(anchor="w", pady=(0, 6))

        self.lbl_playlist_desc = ctk.CTkLabel(
            meta_frame, text="Your custom collection powered by high-performance C++ Doubly Linked List.",
            font=ctk.CTkFont(size=13), text_color=COLOR_SPOTIFY_TEXT_MUTED
        )
        self.lbl_playlist_desc.pack(anchor="w", pady=(0, 8))

        self.lbl_playlist_stats = ctk.CTkLabel(
            meta_frame, text="Spotify • 1 song, about 4 min 30 sec",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN
        )
        self.lbl_playlist_stats.pack(anchor="w")

    def _build_playlist_action_bar(self):
        action_bar = ctk.CTkFrame(self.content_scroll, height=76, fg_color="transparent")
        action_bar.pack(fill="x", padx=32, pady=(16, 8))
        action_bar.pack_propagate(False)

        # Big Spotify Green Circular Play Button (56x56)
        self.btn_hero_play = ctk.CTkButton(
            action_bar, text="", image=self.img_play_icon,
            width=56, height=56, corner_radius=28,
            fg_color="transparent", hover_color="#181818",
            command=self.toggle_play_pause
        )
        self.btn_hero_play.pack(side="left", padx=(0, 20))

        # Heart / Like Button
        self.btn_heart = ctk.CTkButton(
            action_bar, text="♡", width=40, height=40,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=26),
            command=self.on_like_current_song
        )
        self.btn_heart.pack(side="left", padx=8)

        # Options Button (•••)
        btn_dots = ctk.CTkButton(
            action_bar, text="•••", width=40, height=40,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=16),
            command=self.open_dsa_inspector
        )
        btn_dots.pack(side="left", padx=8)

        # Sort Dropdown right aligned (Spotify Style)
        ctk.CTkLabel(
            action_bar, text="Custom order", font=ctk.CTkFont(size=12),
            text_color=COLOR_SPOTIFY_TEXT_MUTED
        ).pack(side="right", padx=(8, 0))

        self.sort_menu = ctk.CTkOptionMenu(
            action_bar, values=["Title (A-Z)", "Artist (A-Z)", "Duration", "Plays"],
            fg_color="#242424", button_color="#2F2F2F", text_color=COLOR_SPOTIFY_TEXT_MAIN,
            width=130, height=32, command=self.on_sort_changed
        )
        self.sort_menu.pack(side="right")

    def _build_table_headers(self):
        header_bar = ctk.CTkFrame(self.content_scroll, height=36, fg_color="transparent")
        header_bar.pack(fill="x", padx=32, pady=(0, 8))

        cols = [
            ("#", 45, "center"),
            ("TITLE", 280, "w"),
            ("ALBUM", 180, "w"),
            ("GENRE", 120, "w"),
            ("🕒", 80, "center"),
            ("ACTIONS", 110, "center")
        ]

        for title, width, anchor in cols:
            lbl = ctk.CTkLabel(
                header_bar, text=title, width=width, anchor=anchor,
                font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MUTED
            )
            lbl.pack(side="left", padx=4)

        # Thin line under headers
        ctk.CTkFrame(self.content_scroll, height=1, fg_color=COLOR_SPOTIFY_BORDER).pack(fill="x", padx=32, pady=(0, 10))

    # -------------------------------------------------------------
    # 3. SPOTIFY BOTTOM PLAYER BAR (100% IDENTICAL TO SPOTIFY)
    # -------------------------------------------------------------
    def _build_bottom_player_bar(self):
        self.player_bar = ctk.CTkFrame(
            self, height=90, corner_radius=0, fg_color=COLOR_SPOTIFY_PLAYER,
            border_width=1, border_color=COLOR_SPOTIFY_BORDER
        )
        self.player_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.player_bar.grid_propagate(False)

        # 3 Columns: Left (Song Info), Center (Controls & Scrubber), Right (Volume & Utils)
        self.player_bar.grid_columnconfigure(0, weight=1)
        self.player_bar.grid_columnconfigure(1, weight=2)
        self.player_bar.grid_columnconfigure(2, weight=1)

        # LEFT: Currently Playing Track Info (Cover, Title, Artist, Heart)
        now_box = ctk.CTkFrame(self.player_bar, fg_color="transparent")
        now_box.grid(row=0, column=0, sticky="w", padx=20, pady=16)

        # Cover Thumbnail
        thumb_box = ctk.CTkFrame(now_box, width=56, height=56, corner_radius=4, fg_color="#282828")
        thumb_box.pack(side="left", padx=(0, 14))
        thumb_box.pack_propagate(False)

        ctk.CTkLabel(thumb_box, text="🎵", font=ctk.CTkFont(size=22), text_color=COLOR_SPOTIFY_GREEN).pack(expand=True)

        # Track metadata text
        track_text_box = ctk.CTkFrame(now_box, fg_color="transparent")
        track_text_box.pack(side="left")

        self.lbl_now_title = ctk.CTkLabel(
            track_text_box, text="No song playing", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN, anchor="w"
        )
        self.lbl_now_title.pack(anchor="w")

        self.lbl_now_artist = ctk.CTkLabel(
            track_text_box, text="Select track to play", font=ctk.CTkFont(size=12),
            text_color=COLOR_SPOTIFY_TEXT_MUTED, anchor="w"
        )
        self.lbl_now_artist.pack(anchor="w")

        # Heart Like Icon
        self.btn_player_heart = ctk.CTkButton(
            now_box, text="♡", width=32, height=32, fg_color="transparent",
            hover_color=COLOR_SPOTIFY_CARD_HOVER, text_color=COLOR_SPOTIFY_TEXT_MUTED,
            font=ctk.CTkFont(size=18), command=self.on_like_current_song
        )
        self.btn_player_heart.pack(side="left", padx=12)

        # CENTER: Controls & Scrubber Slider
        center_box = ctk.CTkFrame(self.player_bar, fg_color="transparent")
        center_box.grid(row=0, column=1, sticky="nsew", pady=10)

        # Row 1: Shuffle, Prev, Play, Next, Repeat
        ctrl_row = ctk.CTkFrame(center_box, fg_color="transparent")
        ctrl_row.pack()

        self.btn_shuffle = ctk.CTkButton(
            ctrl_row, text="🔀", width=34, height=34,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=14),
            command=self.toggle_shuffle
        )
        self.btn_shuffle.pack(side="left", padx=8)

        self.btn_prev = ctk.CTkButton(
            ctrl_row, text="⏮", width=34, height=34,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=18),
            command=self.on_prev_track
        )
        self.btn_prev.pack(side="left", padx=8)

        # Center Play Button: Clean white circle with black icon (Authentic Spotify)
        self.btn_play_main = ctk.CTkButton(
            ctrl_row, text="▶", width=38, height=38, corner_radius=19,
            fg_color=COLOR_SPOTIFY_TEXT_MAIN, hover_color="#E2E8F0",
            text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(size=16, weight="bold"),
            command=self.toggle_play_pause
        )
        self.btn_play_main.pack(side="left", padx=10)

        self.btn_next = ctk.CTkButton(
            ctrl_row, text="⏭", width=34, height=34,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=18),
            command=self.on_next_track
        )
        self.btn_next.pack(side="left", padx=8)

        self.btn_repeat = ctk.CTkButton(
            ctrl_row, text="🔁", width=34, height=34,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=14),
            command=self.toggle_repeat
        )
        self.btn_repeat.pack(side="left", padx=8)

        # Row 2: Progress Scrubber Timeline
        scrub_row = ctk.CTkFrame(center_box, fg_color="transparent")
        scrub_row.pack(fill="x", padx=20, pady=(2, 0))

        self.lbl_time_elapsed = ctk.CTkLabel(
            scrub_row, text="0:00", font=ctk.CTkFont(size=11),
            text_color=COLOR_SPOTIFY_TEXT_MUTED, width=38
        )
        self.lbl_time_elapsed.pack(side="left")

        # Spotify Scrubber Bar
        self.progress_slider = ctk.CTkSlider(
            scrub_row, from_=0, to=100, height=14,
            progress_color=COLOR_SPOTIFY_GREEN,
            fg_color=COLOR_SPOTIFY_SLIDER_BG,
            button_color=COLOR_SPOTIFY_TEXT_MAIN,
            button_hover_color=COLOR_SPOTIFY_TEXT_MAIN,
            button_length=12,
            command=self.on_slider_change
        )
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=8)
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)

        self.lbl_time_total = ctk.CTkLabel(
            scrub_row, text="0:00", font=ctk.CTkFont(size=11),
            text_color=COLOR_SPOTIFY_TEXT_MUTED, width=38
        )
        self.lbl_time_total.pack(side="right")

        # RIGHT: Volume Slider & Quick Utilities
        right_box = ctk.CTkFrame(self.player_bar, fg_color="transparent")
        right_box.grid(row=0, column=2, sticky="e", padx=24, pady=24)

        # Queue Button
        btn_queue = ctk.CTkButton(
            right_box, text="≡", width=32, height=30,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=16),
            command=self.open_queue_modal
        )
        btn_queue.pack(side="left", padx=(0, 6))

        # Volume Mute Icon
        self.btn_vol_icon = ctk.CTkButton(
            right_box, text="🔊", width=32, height=30,
            fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
            text_color=COLOR_SPOTIFY_TEXT_MUTED, font=ctk.CTkFont(size=14),
            command=self.toggle_mute
        )
        self.btn_vol_icon.pack(side="left", padx=(0, 6))

        # Volume Slider
        self.vol_slider = ctk.CTkSlider(
            right_box, from_=0, to=1, width=100, height=12,
            progress_color=COLOR_SPOTIFY_GREEN,
            fg_color=COLOR_SPOTIFY_SLIDER_BG,
            button_color=COLOR_SPOTIFY_TEXT_MAIN,
            button_hover_color=COLOR_SPOTIFY_TEXT_MAIN,
            button_length=10,
            command=self.on_volume_change
        )
        self.vol_slider.set(0.7)
        self.vol_slider.pack(side="left")

    # -------------------------------------------------------------
    # PLAYLIST RENDERING & SONG TABLE
    # -------------------------------------------------------------
    def load_playlist_view(self, playlist_name: str):
        self.bridge.set_active_playlist(playlist_name)
        songs = self.bridge.get_playlist_songs(playlist_name)

        # Update Hero Banner
        self.lbl_playlist_title.configure(text=playlist_name)
        total_dur = sum(s.duration for s in songs)
        mins = total_dur // 60
        self.lbl_playlist_stats.configure(text=f"Spotify • {len(songs)} song(s), ~{mins} min")

        self.render_songs_table(songs)

    def render_songs_table(self, songs: List[SongInfo]):
        for child in self.songs_table_frame.winfo_children():
            child.destroy()

        if not songs:
            ctk.CTkLabel(
                self.songs_table_frame, text="This playlist is empty.\nClick 'Add Local File' to import songs!",
                font=ctk.CTkFont(size=14), text_color=COLOR_SPOTIFY_TEXT_MUTED
            ).pack(pady=40)
            return

        for idx, s in enumerate(songs):
            row = ctk.CTkFrame(
                self.songs_table_frame, height=52, fg_color="transparent",
                corner_radius=6
            )
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            is_cur = (self.current_song and self.current_song.id == s.id)
            if is_cur:
                row.configure(fg_color="#2A2A2A")

            # 1. Index / Play button
            btn_play = ctk.CTkButton(
                row, text="▶" if not is_cur else "❚❚", width=45, height=36,
                fg_color="transparent", hover_color=COLOR_SPOTIFY_CARD_HOVER,
                text_color=COLOR_SPOTIFY_GREEN if is_cur else COLOR_SPOTIFY_TEXT_MUTED,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda song=s, i=idx: self.play_song_at_index(song, i)
            )
            btn_play.pack(side="left", padx=4)

            # 2. Title & Artist
            title_box = ctk.CTkFrame(row, width=280, fg_color="transparent")
            title_box.pack(side="left", padx=4)
            title_box.pack_propagate(False)

            lbl_t = ctk.CTkLabel(
                title_box, text=s.title, font=ctk.CTkFont(size=14, weight="bold" if is_cur else "normal"),
                text_color=COLOR_SPOTIFY_GREEN if is_cur else COLOR_SPOTIFY_TEXT_MAIN, anchor="w"
            )
            lbl_t.pack(anchor="w")

            lbl_a = ctk.CTkLabel(
                title_box, text=s.artist, font=ctk.CTkFont(size=12),
                text_color=COLOR_SPOTIFY_TEXT_MUTED, anchor="w"
            )
            lbl_a.pack(anchor="w")

            # 3. Album
            lbl_alb = ctk.CTkLabel(
                row, text=s.album or "Singles", width=180, anchor="w",
                font=ctk.CTkFont(size=13), text_color=COLOR_SPOTIFY_TEXT_MUTED
            )
            lbl_alb.pack(side="left", padx=4)

            # 4. Genre
            lbl_gen = ctk.CTkLabel(
                row, text=s.genre, width=120, anchor="w",
                font=ctk.CTkFont(size=13), text_color=COLOR_SPOTIFY_TEXT_MUTED
            )
            lbl_gen.pack(side="left", padx=4)

            # 5. Time
            lbl_time = ctk.CTkLabel(
                row, text=s.format_duration(), width=80, anchor="center",
                font=ctk.CTkFont(size=13), text_color=COLOR_SPOTIFY_TEXT_MUTED
            )
            lbl_time.pack(side="left", padx=4)

            # 6. Delete Action (Only for Admin)
            if self.auth.is_current_admin():
                btn_del = ctk.CTkButton(
                    row, text="✕", width=40, height=30,
                    fg_color="transparent", hover_color="#7F1D1D", text_color="#EF4444",
                    command=lambda i=idx: self.on_remove_song_at_index(i)
                )
                btn_del.pack(side="right", padx=10)

    # -------------------------------------------------------------
    # PLAYBACK ENGINE INTEGRATION
    # -------------------------------------------------------------
    def play_song(self, song: SongInfo):
        if not song: return
        self.current_song = song

        # Update Bottom Player Bar UI
        self.lbl_now_title.configure(text=song.title)
        self.lbl_now_artist.configure(text=f"{song.artist} • {song.genre}")
        self.lbl_time_total.configure(text=song.format_duration())
        self.progress_slider.configure(to=max(1, song.duration))
        self.progress_slider.set(0)
        self.lbl_time_elapsed.configure(text="0:00")
        self.btn_play_main.configure(text="❚❚")
        self.btn_hero_play.configure(image=self.img_pause_icon)

        # Resolve File Path
        audio_file = song.file_path
        if audio_file and not os.path.isabs(audio_file):
            cand = os.path.join(parent_dir, audio_file)
            if os.path.exists(cand):
                audio_file = cand

        self.player.play(audio_file, duration=song.duration)
        self.bridge.record_play(song.id)

        # Refresh Song Table row highlights
        self.render_songs_table(self.bridge.get_playlist_songs(self.bridge.get_active_playlist()))

    def play_song_at_index(self, song: SongInfo, index: int):
        self.bridge.set_current_index(index)
        self.play_song(song)

    def toggle_play_pause(self):
        if not self.current_song:
            songs = self.bridge.get_playlist_songs(self.bridge.get_active_playlist())
            if songs:
                self.play_song_at_index(songs[0], 0)
            return

        if self.player.is_paused:
            self.player.unpause()
            self.btn_play_main.configure(text="❚❚")
            self.btn_hero_play.configure(image=self.img_pause_icon)
        elif self.player.is_playing:
            self.player.pause()
            self.btn_play_main.configure(text="▶")
            self.btn_hero_play.configure(image=self.img_play_icon)
        else:
            self.play_song(self.current_song)

    def on_prev_track(self):
        prev_s = self.bridge.get_prev_song()
        if prev_s:
            self.play_song(prev_s)

    def on_next_track(self):
        next_s = self.bridge.get_next_song()
        if next_s:
            self.play_song(next_s)

    def on_song_finished(self):
        if self.is_repeat and self.current_song:
            self.play_song(self.current_song)
        else:
            self.on_next_track()

    def toggle_shuffle(self):
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            self.btn_shuffle.configure(text_color=COLOR_SPOTIFY_GREEN)
            cur_pl = self.bridge.get_active_playlist()
            self.bridge.shuffle_playlist(cur_pl)
            self.render_songs_table(self.bridge.get_playlist_songs(cur_pl))
        else:
            self.btn_shuffle.configure(text_color=COLOR_SPOTIFY_TEXT_MUTED)

    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        if self.is_repeat:
            self.btn_repeat.configure(text_color=COLOR_SPOTIFY_GREEN)
        else:
            self.btn_repeat.configure(text_color=COLOR_SPOTIFY_TEXT_MUTED)

    def on_slider_press(self, event=None):
        self.is_seeking = True

    def on_slider_release(self, event=None):
        try:
            val = float(self.progress_slider.get())
            self.player.seek(val)
        finally:
            self.is_seeking = False

    def on_slider_change(self, val):
        mins = int(val) // 60
        secs = int(val) % 60
        self.lbl_time_elapsed.configure(text=f"{mins}:{secs:02d}")
        if not self.is_seeking and self.player.is_playing:
            self.player.seek(float(val))

    def on_volume_change(self, val):
        self.player.set_volume(val)
        if val == 0:
            self.btn_vol_icon.configure(text="🔇")
        elif val < 0.5:
            self.btn_vol_icon.configure(text="🔉")
        else:
            self.btn_vol_icon.configure(text="🔊")

    def toggle_mute(self):
        if self.player.volume > 0:
            self.player.set_volume(0)
            self.vol_slider.set(0)
            self.btn_vol_icon.configure(text="🔇")
        else:
            self.player.set_volume(0.7)
            self.vol_slider.set(0.7)
            self.btn_vol_icon.configure(text="🔊")

    def on_like_current_song(self):
        if self.current_song:
            self.bridge.add_to_playlist("Favorites", self.current_song.id)
            self.btn_heart.configure(text="♥", text_color=COLOR_SPOTIFY_GREEN)
            self.btn_player_heart.configure(text="♥", text_color=COLOR_SPOTIFY_GREEN)
            self.on_save_data(silent=True)
            messagebox.showinfo("Spotify", f"Added '{self.current_song.title}' to your Liked Songs!")

    # -------------------------------------------------------------
    # SEARCH & SORTING & PLAYLIST MANAGEMENT
    # -------------------------------------------------------------
    def on_search_key(self, event=None):
        q = self.search_entry.get().strip()
        if not q:
            self.render_songs_table(self.bridge.get_playlist_songs(self.bridge.get_active_playlist()))
        else:
            # High speed C++ Trie search
            found = self.bridge.search(q)
            self.render_songs_table(found)

    def on_sort_changed(self, choice):
        # 0=Title, 1=Artist, 2=Duration, 3=PlayCount
        criteria_map = {
            "Title (A-Z)": 0,
            "Artist (A-Z)": 1,
            "Duration": 2,
            "Plays": 3
        }
        crit = criteria_map.get(choice, 0)
        cur_pl = self.bridge.get_active_playlist()
        self.bridge.sort_playlist(cur_pl, crit, ascending=(crit != 3))
        self.render_songs_table(self.bridge.get_playlist_songs(cur_pl))

    def on_remove_song_at_index(self, index: int):
        if not self.auth.is_current_admin():
            messagebox.showwarning("Admin Restricted", "Admin privileges required to delete tracks from the Master Library!\n\nPlease switch to an Admin account.")
            return
        cur_pl = self.bridge.get_active_playlist()
        self.bridge.remove_from_playlist(cur_pl, index)
        self.on_save_data(silent=True)
        self.render_songs_table(self.bridge.get_playlist_songs(cur_pl))

    def on_create_playlist_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter playlist name:", title="New Playlist")
        name = dialog.get_input()
        if name and name.strip():
            if self.bridge.create_playlist(name.strip()):
                self.refresh_sidebar_playlists()
                self.load_playlist_view(name.strip())
                self.on_save_data(silent=True)
            else:
                messagebox.showerror("Error", "Playlist already exists or name is invalid.")

    def on_add_local_song(self):
        if not self.auth.is_current_admin():
            messagebox.showwarning("Admin Restricted", "Admin privileges required to import new tracks into the Master Library!\n\nPlease switch to an Admin account.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Local Audio Track - Spotify")
        dialog.geometry("460x500")
        dialog.grab_set()
        dialog.configure(fg_color=COLOR_SPOTIFY_BG)

        ctk.CTkLabel(
            dialog, text="Import Local Audio Track",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN
        ).pack(pady=(20, 10))

        form = ctk.CTkFrame(dialog, fg_color="transparent")
        form.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(form, text="Audio File:", anchor="w", text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(fill="x")
        file_box = ctk.CTkFrame(form, fg_color="transparent")
        file_box.pack(fill="x", pady=(2, 8))

        entry_path = ctk.CTkEntry(file_box, placeholder_text="Select MP3 or WAV file...")
        entry_path.pack(side="left", fill="x", expand=True, padx=(0, 6))

        def browse():
            fp = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
            if fp:
                entry_path.delete(0, tk.END)
                entry_path.insert(0, fp)
                base = os.path.splitext(os.path.basename(fp))[0]
                entry_title.delete(0, tk.END)
                entry_title.insert(0, base.replace("_", " ").title())

        ctk.CTkButton(file_box, text="Browse", width=68, fg_color="#242424", hover_color="#333333", command=browse).pack(side="right")

        ctk.CTkLabel(form, text="Title:", anchor="w", text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(fill="x")
        entry_title = ctk.CTkEntry(form, placeholder_text="Song Title")
        entry_title.pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(form, text="Artist:", anchor="w", text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(fill="x")
        entry_artist = ctk.CTkEntry(form, placeholder_text="Artist Name")
        entry_artist.pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(form, text="Genre:", anchor="w", text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(fill="x")
        genre_opt = ctk.CTkOptionMenu(
            form, values=["Punjabi", "Pop", "Hip-Hop", "Rock", "Lo-Fi", "Electronic"],
            fg_color="#242424", button_color="#333333"
        )
        genre_opt.pack(fill="x", pady=(2, 14))

        def submit():
            t = entry_title.get().strip() or "Untitled"
            a = entry_artist.get().strip() or "Unknown Artist"
            g = genre_opt.get()
            fp = entry_path.get().strip()

            new_song = SongInfo(
                id=0, title=t, artist=a, album="Singles", genre=g,
                duration=210, bpm=120, play_count=0, file_path=fp
            )
            sid = self.bridge.add_song(new_song)
            cur_pl = self.bridge.get_active_playlist()
            if cur_pl != "All Songs":
                self.bridge.add_to_playlist(cur_pl, sid)

            self.on_save_data(silent=True)
            self.load_playlist_view(cur_pl)
            dialog.destroy()
            messagebox.showinfo("Spotify", f"Track '{t}' imported successfully!")

        ctk.CTkButton(
            dialog, text="Add Track to Library",
            fg_color=COLOR_SPOTIFY_GREEN, hover_color=COLOR_SPOTIFY_GREEN_HOVER,
            text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(weight="bold"),
            height=38, command=submit
        ).pack(pady=10)

    def on_save_data(self, silent: bool = False):
        save_path = os.path.join(parent_dir, "data", "library.json")
        self.bridge.save_file(save_path)
        if not silent:
            messagebox.showinfo("Spotify", "Library saved successfully to data/library.json!")

    def set_active_tab(self, tab: str):
        self.active_tab = tab
        if tab == "home" or tab == "library":
            self.load_playlist_view("All Songs")
        elif tab == "search":
            self.search_entry.focus()

    def open_queue_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Play Queue (FIFO)")
        modal.geometry("440x480")
        modal.grab_set()
        modal.configure(fg_color=COLOR_SPOTIFY_BG)

        ctk.CTkLabel(
            modal, text="Play Queue (FIFO)", font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN
        ).pack(pady=(16, 10))

        q_songs = self.bridge.get_queue()
        scroll = ctk.CTkScrollableFrame(modal, fg_color=COLOR_SPOTIFY_CARD)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        if not q_songs:
            ctk.CTkLabel(scroll, text="Queue is empty.", text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(pady=30)
        else:
            for i, s in enumerate(q_songs):
                ctk.CTkLabel(scroll, text=f"{i+1}. {s.title} - {s.artist}", text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=4)

    def open_dsa_inspector(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Spotify - C++ DSA Architecture Inspector")
        modal.geometry("700x560")
        modal.grab_set()
        modal.configure(fg_color=COLOR_SPOTIFY_BG)

        ctk.CTkLabel(
            modal, text="⚡ C++ DSA Engine Architecture",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_SPOTIFY_GREEN
        ).pack(pady=(18, 8))

        content_box = ctk.CTkTextbox(
            modal, fg_color=COLOR_SPOTIFY_CARD, font=ctk.CTkFont(family="Consolas", size=12), wrap="word"
        )
        content_box.pack(fill="both", expand=True, padx=24, pady=10)

        cur_pl = self.bridge.get_active_playlist()
        pl_songs = self.bridge.get_playlist_songs(cur_pl)

        report = f"""======================================================================
  SPOTIFY ARCHITECTURE & C++ DSA COMPLEXITY REPORT
======================================================================
Core Engine Status: {'NATIVE C++ SHARED LIBRARY (playlist_core.dll)' if self.bridge.is_native else 'PYTHON DSA FALLBACK'}
Active Playlist   : {cur_pl} ({len(pl_songs)} nodes)

1. DOUBLY LINKED LIST NODES (O(1) Bidirectional Traversal):
"""
        for i, s in enumerate(pl_songs):
            report += f"  [{i}] <-> (ID: {s.id}) '{s.title}' by {s.artist}\n"

        report += """
2. ACADEMIC DATA STRUCTURES ANALYSIS:
----------------------------------------------------------------------
Data Structure        Operation            Time Complexity   Space
----------------------------------------------------------------------
Doubly Linked List    Next / Prev Track    O(1)              O(N)
FIFO Play Queue       Enqueue / Dequeue    O(1)              O(K)
LIFO History Stack    Push / Pop           O(1)              O(M)
Prefix Tree (Trie)    Search Word/Prefix   O(L)              O(Alphabet * N)
Sorter (MergeSort)    Multi-Column Sort    O(N log N)        O(N)
Vector Recommendation Content Similarity   O(N log K)        O(K)
======================================================================
"""
        content_box.insert("1.0", report)
        content_box.configure(state="disabled")

        ctk.CTkButton(
            modal, text="Close Inspector", command=modal.destroy,
            fg_color=COLOR_SPOTIFY_GREEN, text_color=COLOR_SPOTIFY_BLACK,
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=12)

    # -------------------------------------------------------------
    # AUTHENTICATION & ADMIN DASHBOARD METHODS
    # -------------------------------------------------------------
    def update_auth_ui(self):
        user = self.auth.current_user
        if not user:
            self.btn_profile.configure(text="👤  Login", text_color=COLOR_SPOTIFY_TEXT_MUTED)
            if hasattr(self, 'btn_admin_panel'):
                self.btn_admin_panel.pack_forget()
        elif user.is_admin():
            self.btn_profile.configure(text=f"👑  Admin ({user.username})", text_color=COLOR_SPOTIFY_GREEN)
            if hasattr(self, 'btn_admin_panel'):
                self.btn_admin_panel.pack(fill="x", pady=2)
        else:
            self.btn_profile.configure(text=f"👤  {user.display_name}", text_color=COLOR_SPOTIFY_TEXT_MAIN)
            if hasattr(self, 'btn_admin_panel'):
                self.btn_admin_panel.pack_forget()

        # Update table to reflect delete button visibility based on admin role
        cur_pl = self.bridge.get_active_playlist()
        self.render_songs_table(self.bridge.get_playlist_songs(cur_pl))

    def open_profile_menu(self):
        u = self.auth.current_user
        if not u:
            self.open_login_modal()
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Account - Spotify")
        modal.geometry("400x410")
        modal.grab_set()
        modal.configure(fg_color=COLOR_SPOTIFY_BG)

        name = u.display_name if u else "Guest"
        uname = u.username if u else "None"
        email = u.email if u else "None"
        role_str = "👑 System Administrator" if (u and u.is_admin()) else "👤 Standard Listener"

        ctk.CTkLabel(
            modal, text="Account Settings", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_SPOTIFY_TEXT_MAIN
        ).pack(pady=(20, 8))

        card = ctk.CTkFrame(modal, fg_color=COLOR_SPOTIFY_CARD, corner_radius=10)
        card.pack(fill="x", padx=24, pady=8)

        ctk.CTkLabel(card, text=f"User: {name} (@{uname})", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(pady=(12, 2), padx=14, anchor="w")
        ctk.CTkLabel(card, text=f"📧 Email: {email}", font=ctk.CTkFont(size=12), text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(pady=(0, 2), padx=14, anchor="w")
        ctk.CTkLabel(card, text=f"Role: {role_str}", font=ctk.CTkFont(size=13), text_color=COLOR_SPOTIFY_GREEN if (u and u.is_admin()) else COLOR_SPOTIFY_TEXT_MUTED).pack(pady=(0, 12), padx=14, anchor="w")

        btn_box = ctk.CTkFrame(modal, fg_color="transparent")
        btn_box.pack(fill="x", padx=24, pady=8)

        if self.auth.is_current_admin():
            ctk.CTkButton(
                btn_box, text="👑  Open Admin Dashboard", fg_color="#143422", hover_color="#1B472E",
                text_color=COLOR_SPOTIFY_GREEN, font=ctk.CTkFont(weight="bold"), height=36,
                command=lambda: [modal.destroy(), self.open_admin_dashboard()]
            ).pack(fill="x", pady=3)

        ctk.CTkButton(
            btn_box, text="🔄  Switch User / Log In", fg_color=COLOR_SPOTIFY_GREEN, hover_color=COLOR_SPOTIFY_GREEN_HOVER,
            text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(weight="bold"), height=36,
            command=lambda: [modal.destroy(), self.open_login_modal(initial_tab="Log In")]
        ).pack(fill="x", pady=3)

        ctk.CTkButton(
            btn_box, text="✨  Create New Account (Sign Up)", fg_color="#242424", hover_color="#333333",
            text_color=COLOR_SPOTIFY_TEXT_MAIN, font=ctk.CTkFont(weight="bold"), height=34,
            command=lambda: [modal.destroy(), self.open_login_modal(initial_tab="Sign Up")]
        ).pack(fill="x", pady=3)

        ctk.CTkButton(
            btn_box, text="🚪  Logout (Guest Mode)", fg_color="transparent", hover_color="#282828",
            text_color="#EF4444", height=32,
            command=lambda: [self.auth.logout(), self.update_auth_ui(), modal.destroy(), messagebox.showinfo("Logged Out", "You are now in guest mode.")]
        ).pack(fill="x", pady=3)

    def open_login_modal(self, initial_tab: str = "Log In"):
        modal = ctk.CTkToplevel(self)
        modal.title("Spotify - Log In or Sign Up")
        modal.geometry("480x620")
        modal.grab_set()
        modal.configure(fg_color=COLOR_SPOTIFY_BG)

        # Header
        top_h = ctk.CTkFrame(modal, fg_color="transparent")
        top_h.pack(fill="x", padx=24, pady=(18, 6))
        ctk.CTkLabel(top_h, text="●))) Spotify", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_SPOTIFY_GREEN).pack()
        ctk.CTkLabel(top_h, text="Music for everyone • Millions of tracks", font=ctk.CTkFont(size=12), text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(pady=(2, 0))

        # Tabview for Log In and Sign Up
        tabview = ctk.CTkTabview(
            modal, fg_color=COLOR_SPOTIFY_CARD,
            segmented_button_selected_color=COLOR_SPOTIFY_GREEN,
            segmented_button_selected_hover_color=COLOR_SPOTIFY_GREEN_HOVER,
            segmented_button_unselected_color="#242424",
            segmented_button_unselected_hover_color="#303030"
        )
        tabview.pack(fill="both", expand=True, padx=24, pady=(4, 16))

        tab_login = tabview.add("Log In")
        tab_signup = tabview.add("Sign Up")
        tabview.set(initial_tab)

        # ---------------------------------------------------------
        # TAB 1: LOG IN
        # ---------------------------------------------------------
        quick_frame = ctk.CTkFrame(tab_login, fg_color="#121212", corner_radius=8)
        quick_frame.pack(fill="x", padx=16, pady=(10, 10))

        ctk.CTkLabel(quick_frame, text="Quick One-Click Demo Login:", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(anchor="w", padx=10, pady=(6, 2))
        btn_row = ctk.CTkFrame(quick_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 8))

        def fill_and_login(identifier, pwd):
            ent_u.delete(0, tk.END)
            ent_u.insert(0, identifier)
            ent_p.delete(0, tk.END)
            ent_p.insert(0, pwd)
            do_login()

        admin_u = next((u for u in self.auth.get_all_users() if u.is_admin()), None)
        norm_u = next((u for u in self.auth.get_all_users() if not u.is_admin()), None)

        admin_id = admin_u.email if admin_u else "adminswayam@gmail.com"
        admin_pw = admin_u.password if admin_u else "admin@123"
        admin_lbl = f"👑 Admin ({admin_u.username if admin_u else 'admin'})"

        user_id = norm_u.email if norm_u else "swayam@gmail.com"
        user_pw = norm_u.password if norm_u else "user123"
        user_lbl = f"👤 User ({norm_u.username if norm_u else 'user'})"

        ctk.CTkButton(
            btn_row, text=admin_lbl, width=190, height=30,
            fg_color="#143422", hover_color="#1B472E", text_color=COLOR_SPOTIFY_GREEN,
            font=ctk.CTkFont(size=11, weight="bold"), command=lambda: fill_and_login(admin_id, admin_pw)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_row, text=user_lbl, width=190, height=30,
            fg_color="#242424", hover_color="#333333", text_color=COLOR_SPOTIFY_TEXT_MAIN,
            font=ctk.CTkFont(size=11), command=lambda: fill_and_login(user_id, user_pw)
        ).pack(side="left")

        # Login Form
        login_f = ctk.CTkFrame(tab_login, fg_color="transparent")
        login_f.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(login_f, text="Email or Username:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_u = ctk.CTkEntry(login_f, placeholder_text="e.g. adminswayam@gmail.com or username", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_u.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(login_f, text="Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_p = ctk.CTkEntry(login_f, placeholder_text="Enter your password", show="•", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_p.pack(fill="x", pady=(0, 10))

        lbl_login_status = ctk.CTkLabel(login_f, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        lbl_login_status.pack(pady=(0, 6))

        def do_login():
            ident = ent_u.get().strip()
            pwd = ent_p.get().strip()
            res = self.auth.login(ident, pwd)
            if res:
                self.update_auth_ui()
                modal.destroy()
                messagebox.showinfo("Login Success", f"Welcome back, {res.display_name}!\nAccount: {res.email}\nRole: {res.role.upper()}")
            else:
                lbl_login_status.configure(text="Invalid email/username or password!")

        ctk.CTkButton(
            login_f, text="Log In", fg_color=COLOR_SPOTIFY_GREEN, hover_color=COLOR_SPOTIFY_GREEN_HOVER,
            text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=do_login
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            login_f, text="Don't have an account? Sign up free", fg_color="transparent",
            text_color=COLOR_SPOTIFY_GREEN, font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=COLOR_SPOTIFY_CARD, command=lambda: tabview.set("Sign Up")
        ).pack()

        # ---------------------------------------------------------
        # TAB 2: SIGN UP (USER APNA ACCOUNT KHUD BANAYE)
        # ---------------------------------------------------------
        signup_f = ctk.CTkScrollableFrame(tab_signup, fg_color="transparent", height=420)
        signup_f.pack(fill="both", expand=True, padx=8, pady=4)

        ctk.CTkLabel(signup_f, text="Create your free account", font=ctk.CTkFont(size=15, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 10))

        ctk.CTkLabel(signup_f, text="Your Name (Display Name):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_sign_name = ctk.CTkEntry(signup_f, placeholder_text="e.g. Swayam Sharma", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_sign_name.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(signup_f, text="Choose a Username:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_sign_u = ctk.CTkEntry(signup_f, placeholder_text="e.g. swayam01 (letters & numbers)", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_sign_u.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(signup_f, text="Your Email Address:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_sign_e = ctk.CTkEntry(signup_f, placeholder_text="e.g. swayam@gmail.com", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_sign_e.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(signup_f, text="Create a Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(2, 2))
        ent_sign_p = ctk.CTkEntry(signup_f, placeholder_text="Enter password (min 3 chars)", show="•", height=36, fg_color="#121212", border_color=COLOR_SPOTIFY_BORDER)
        ent_sign_p.pack(fill="x", pady=(0, 8))

        lbl_sign_status = ctk.CTkLabel(signup_f, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        lbl_sign_status.pack(pady=(0, 4))

        def do_signup():
            name = ent_sign_name.get().strip()
            un = ent_sign_u.get().strip()
            em = ent_sign_e.get().strip()
            pw = ent_sign_p.get().strip()

            if not name or not un or not em or not pw:
                lbl_sign_status.configure(text="Please fill in all the required fields!")
                return

            if "@" not in em or "." not in em:
                lbl_sign_status.configure(text="Please enter a valid email address!")
                return

            if len(pw) < 3:
                lbl_sign_status.configure(text="Password must be at least 3 characters!")
                return

            # Register account as 'user'
            if self.auth.add_user(username=un, email=em, password=pw, role="user", display_name=name):
                # Auto-login newly registered user
                self.auth.login(em, pw)
                self.update_auth_ui()
                modal.destroy()
                messagebox.showinfo("Welcome to Spotify!", f"🎉 Account created successfully!\n\nWelcome, {name}!\nYou are now signed in to Spotify.")
            else:
                lbl_sign_status.configure(text="Username or Email is already registered!")

        ctk.CTkButton(
            signup_f, text="Create Free Account", fg_color=COLOR_SPOTIFY_GREEN, hover_color=COLOR_SPOTIFY_GREEN_HOVER,
            text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=do_signup
        ).pack(fill="x", pady=(2, 8))

        ctk.CTkButton(
            signup_f, text="Already have an account? Log In", fg_color="transparent",
            text_color=COLOR_SPOTIFY_GREEN, font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=COLOR_SPOTIFY_CARD, command=lambda: tabview.set("Log In")
        ).pack(pady=(0, 10))

    def open_admin_dashboard(self):
        if not self.auth.is_current_admin():
            messagebox.showerror("Access Denied", "Administrator permissions required to access the Admin Dashboard!")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Spotify - User Accounts Management")
        modal.geometry("760x560")
        modal.grab_set()
        modal.configure(fg_color=COLOR_SPOTIFY_BG)

        # Header
        top_box = ctk.CTkFrame(modal, fg_color="transparent")
        top_box.pack(fill="x", padx=28, pady=(20, 10))

        ctk.CTkLabel(top_box, text="👥 User Accounts Management", font=ctk.CTkFont(size=22, weight="bold"), text_color=COLOR_SPOTIFY_GREEN).pack(side="left")

        u = self.auth.current_user
        sub_text = f"Logged in as: {u.display_name} (@{u.username})" if u else ""
        ctk.CTkLabel(top_box, text=sub_text, font=ctk.CTkFont(size=12), text_color=COLOR_SPOTIFY_TEXT_MUTED).pack(side="right", pady=(4, 0))

        # Main Card Container
        main_card = ctk.CTkFrame(modal, fg_color=COLOR_SPOTIFY_CARD, corner_radius=12)
        main_card.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        u_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        u_frame.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(u_frame, text="Registered Accounts:", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", pady=(0, 8))

        u_scroll = ctk.CTkScrollableFrame(u_frame, height=240, fg_color="#121212")
        u_scroll.pack(fill="both", expand=True, pady=(0, 14))

        def refresh_users_list():
            for w in u_scroll.winfo_children(): w.destroy()
            for user in self.auth.get_all_users():
                r = ctk.CTkFrame(u_scroll, height=44, fg_color=COLOR_SPOTIFY_CARD)
                r.pack(fill="x", pady=2)
                r.pack_propagate(False)
                role_badge = "👑 Admin" if user.is_admin() else "👤 User"
                user_label = f"{role_badge}  {user.username} ({user.display_name})  •  📧 {user.email}"
                ctk.CTkLabel(r, text=user_label, font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_GREEN if user.is_admin() else COLOR_SPOTIFY_TEXT_MAIN).pack(side="left", padx=12)
                
                # Cannot delete the current admin user if it's the only admin
                is_sole_admin = user.is_admin() and (sum(1 for acc in self.auth.get_all_users() if acc.is_admin()) <= 1)
                if not is_sole_admin:
                    ctk.CTkButton(
                        r, text="Delete", width=64, height=26, fg_color="#7F1D1D", hover_color="#991B1B",
                        font=ctk.CTkFont(size=11, weight="bold"),
                        command=lambda un=user.username: [self.auth.remove_user(un), refresh_users_list()]
                    ).pack(side="right", padx=10)

        refresh_users_list()

        # Add user form
        add_u_box = ctk.CTkFrame(u_frame, fg_color="#121212", corner_radius=8)
        add_u_box.pack(fill="x", pady=4)

        ctk.CTkLabel(add_u_box, text="Register New Account with Email & Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_SPOTIFY_TEXT_MAIN).pack(anchor="w", padx=12, pady=(8, 4))
        in_row = ctk.CTkFrame(add_u_box, fg_color="transparent")
        in_row.pack(fill="x", padx=12, pady=(0, 10))

        ent_new_u = ctk.CTkEntry(in_row, placeholder_text="Username", width=120)
        ent_new_u.pack(side="left", padx=3)
        ent_new_email = ctk.CTkEntry(in_row, placeholder_text="Email Address", width=170)
        ent_new_email.pack(side="left", padx=3)
        ent_new_p = ctk.CTkEntry(in_row, placeholder_text="Password", width=120)
        ent_new_p.pack(side="left", padx=3)
        role_sel = ctk.CTkOptionMenu(in_row, values=["user", "admin"], width=85)
        role_sel.pack(side="left", padx=3)

        def create_new_user_action():
            un = ent_new_u.get().strip()
            em = ent_new_email.get().strip()
            pw = ent_new_p.get().strip()
            rl = role_sel.get()
            if un and pw:
                if self.auth.add_user(un, em, pw, role=rl, display_name=un.capitalize()):
                    ent_new_u.delete(0, tk.END)
                    ent_new_email.delete(0, tk.END)
                    ent_new_p.delete(0, tk.END)
                    refresh_users_list()
                    messagebox.showinfo("User Added", f"Account '{un}' ({em}) created successfully!")
                else:
                    messagebox.showerror("Error", "Username or Email already exists!")

        ctk.CTkButton(in_row, text="Add User", fg_color=COLOR_SPOTIFY_GREEN, hover_color=COLOR_SPOTIFY_GREEN_HOVER, text_color=COLOR_SPOTIFY_BLACK, font=ctk.CTkFont(weight="bold"), width=90, command=create_new_user_action).pack(side="left", padx=6)

    # -------------------------------------------------------------
    # 100MS SMOOTH PLAYBACK UPDATE LOOP
    # -------------------------------------------------------------
    def _update_playback_loop(self):
        try:
            if self.player.is_playing and not self.player.is_paused and not self.is_seeking:
                elapsed = self.player.get_progress()
                mins = int(elapsed) // 60
                secs = int(elapsed) % 60
                self.lbl_time_elapsed.configure(text=f"{mins}:{secs:02d}")
                self.progress_slider.set(elapsed)

            self.player.check_events()
        except Exception:
            pass
        finally:
            self.after(100, self._update_playback_loop)

if __name__ == "__main__":
    app = SpotifyPlayerApp()
    app.mainloop()
