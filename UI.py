import pygame
import os

# UI Colors & Constants
BG_COLOR = (40, 40, 40)
BTN_COLOR = (100, 100, 255)
BTN_ACTIVE_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
INPUT_BG_COLOR = (30, 30, 30)
INPUT_ACTIVE_COLOR = (50, 50, 50)
INPUT_BORDER_COLOR = (255, 255, 255)

EXPORT_MENU_RECT = (180, 120, 460, 440)
TOPBAR_HEIGHT = 30
CONTEXT_MENU_WIDTH = 160
CONTEXT_MENU_OPTION_HEIGHT = 25
TOPBAR_MENU_WIDTH = 140
TOPBAR_DROPDOWN_HEIGHT = 25

# --------- Basic Draw Functions ---------

def draw_button(surface, rect, text, font, active=False):
    color = BTN_COLOR if not active else BTN_ACTIVE_COLOR
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, TEXT_COLOR, rect, 1)
    txt = font.render(text, True, TEXT_COLOR)
    txt_rect = txt.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    surface.blit(txt, txt_rect)


def draw_input_field(surface, label, value, pos, font, active=False):
    x, y = pos
    color = INPUT_ACTIVE_COLOR if active else INPUT_BG_COLOR
    pygame.draw.rect(surface, color, (x, y, 200, 30))
    pygame.draw.rect(surface, INPUT_BORDER_COLOR, (x, y, 200, 30), 2)
    txt = font.render(f"{label}: {value}", True, TEXT_COLOR)
    surface.blit(txt, (x + 5, y + 5))


# --------- Existing Menus ---------

def draw_main_menu(surface, font):
    pygame.draw.rect(surface, BG_COLOR, (250, 200, 300, 150))
    draw_button(surface, (300, 230, 200, 40), "+ Add Bone", font)
    draw_button(surface, (300, 290, 200, 40), "Close Menu", font)


def draw_add_bone_menu(surface, new_bone_data, selected_input_field, font):
    pygame.draw.rect(surface, BG_COLOR, (180, 120, 440, 360))
    pygame.draw.rect(surface, TEXT_COLOR, (180, 120, 440, 360), 2)
    draw_input_field(surface, "Name", new_bone_data["name"], (200, 140), font, selected_input_field == "name")

    parent_name = new_bone_data["parent"].name if new_bone_data["parent"] else "None"
    draw_button(surface, (200, 200, 200, 30), f"Parent: {parent_name}", font)

    img_text = os.path.basename(new_bone_data["image_path"]) if new_bone_data.get("image_path") else "None"
    draw_button(surface, (200, 250, 200, 30), f"Image: {img_text}", font)

    draw_input_field(surface, "Length", str(new_bone_data["length"]), (200, 300), font, selected_input_field == "length")

    draw_button(surface, (200, 350, 100, 30), "Add", font)
    draw_button(surface, (320, 350, 100, 30), "Back", font)


def draw_image_menu(surface, image_buttons, font, title="Select Image"):
    pygame.draw.rect(surface, (50, 50, 50), (180, 150, 440, 300))
    pygame.draw.rect(surface, (255, 255, 255), (180, 150, 440, 300), 3)
    txt = font.render(title, True, (255, 255, 255))
    surface.blit(txt, (200, 160))
    for thumb, _, (x, y), _ in image_buttons:
        surface.blit(thumb, (x, y))
    draw_button(surface, (200, 420, 100, 30), "Back", font)



def draw_sidebar(surface, bones, selected_bone, font, sidebar_width=200, screen_width=800, y_offset=0):
    x = screen_width - sidebar_width
    pygame.draw.rect(surface, (20, 20, 20), (x, y_offset, sidebar_width, surface.get_height() - y_offset))

    add_bone_rect = pygame.Rect(x + 10, y_offset + 10, sidebar_width - 20, 25)
    color = BTN_COLOR if selected_bone is None else BTN_ACTIVE_COLOR
    pygame.draw.rect(surface, color, add_bone_rect)
    pygame.draw.rect(surface, TEXT_COLOR, add_bone_rect, 1)
    txt = font.render("+ Add Bone", True, TEXT_COLOR)
    surface.blit(txt, (add_bone_rect.x + 5, add_bone_rect.y + 5))

    for i, bone in enumerate(bones):
        y = y_offset + 40 + i * 30
        rect = pygame.Rect(x + 10, y, sidebar_width - 20, 25)
        color = BTN_COLOR if bone == selected_bone else BTN_ACTIVE_COLOR
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, TEXT_COLOR, rect, 1)
        txt = font.render(bone.name, True, TEXT_COLOR)
        surface.blit(txt, (rect.x + 5, rect.y + 5))


def draw_timeline(surface, bones, current_time, max_time, fps, frame_width, timeline_y, font, y_offset=0):
    timeline_y += y_offset
    pygame.draw.rect(surface, (20, 20, 20), (0, timeline_y, surface.get_width(), surface.get_height() - timeline_y))
    pygame.draw.line(surface, (100, 100, 100), (0, timeline_y), (surface.get_width(), timeline_y), 2)

    total_frames = int(max_time * fps)
    for f in range(total_frames):
        x = f * frame_width
        if x >= surface.get_width():
            break
        color = (60, 60, 60) if f % fps != 0 else (100, 100, 100)
        pygame.draw.line(surface, color, (x, timeline_y), (x, timeline_y + 10))

    for idx, bone in enumerate(bones):
        y_offset_bone = timeline_y + 20 + idx * 15
        for key in bone.timeline.keyframes:
            x = int(key.time * fps * frame_width)
            if x < surface.get_width():
                pygame.draw.circle(surface, (255, 0, 0), (x, y_offset_bone), 4)

    time_x = int(current_time * fps * frame_width)
    pygame.draw.line(surface, (0, 255, 255), (time_x, timeline_y), (time_x, surface.get_height()), 2)


def draw_play_button(surface, play_mode, font, screen_width=800, screen_height=600, y_offset=0):
    button_width, button_height = 100, 30
    x = (screen_width - button_width) // 2
    y = screen_height - button_height
    rect = pygame.Rect(x, y, button_width, button_height)
    color = (100, 255, 100) if play_mode else (100, 100, 255)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2)
    text = "Stop" if play_mode else "Play"
    txt_surface = font.render(text, True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(center=rect.center)
    surface.blit(txt_surface, txt_rect)
    return rect


# --- Export Menu Functions --- #

def draw_export_menu(surface, export_settings, selected_input_field, font):
    """
    Draw export menu UI.

    export_settings: dict with keys
        'animation_length' (str),
        'fps' (str),
        'total_frames' (str),
        'output_folder' (str),
        'output_gif' (str)

    selected_input_field: one of the keys or None

    """
    pygame.draw.rect(surface, BG_COLOR, EXPORT_MENU_RECT)
    pygame.draw.rect(surface, TEXT_COLOR, EXPORT_MENU_RECT, 2)

    x, y, w, h = EXPORT_MENU_RECT
    margin = 20

    draw_input_field(surface, "Animation Length (s)", export_settings.get("animation_length", ""), (x + margin, y + 40), font, selected_input_field == "animation_length")
    draw_input_field(surface, "FPS", export_settings.get("fps", ""), (x + margin, y + 90), font, selected_input_field == "fps")
    draw_input_field(surface, "Total Frames (override)", export_settings.get("total_frames", ""), (x + margin, y + 140), font, selected_input_field == "total_frames")
    draw_input_field(surface, "Output Folder", export_settings.get("output_folder", ""), (x + margin, y + 190), font, selected_input_field == "output_folder")
    draw_input_field(surface, "Output GIF Filename", export_settings.get("output_gif", ""), (x + margin, y + 240), font, selected_input_field == "output_gif")

    draw_button(surface, (x + margin, y + 300, 200, 40), "Export PNG Frames", font)
    draw_button(surface, (x + margin + 220, y + 300, 200, 40), "Export GIF", font)
    draw_button(surface, (x + margin, y + 350, 420, 40), "Back", font)


# ----------- New UI Classes: ContextMenu and TopBar -----------

class ContextMenu:
    def __init__(self, options):
        """
        options: list of (label:str, command:str)
        """
        self.options = options
        self.visible = False
        self.position = (0, 0)
        self.selected_index = None

    def show(self, pos):
        self.position = pos
        self.visible = True
        self.selected_index = None

    def hide(self):
        self.visible = False
        self.selected_index = None

    def handle_event(self, event):
        if not self.visible:
            return None

        mx, my = pygame.mouse.get_pos()
        x, y = self.position
        width = CONTEXT_MENU_WIDTH
        height = CONTEXT_MENU_OPTION_HEIGHT * len(self.options)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                # Check if clicked on any option
                for i, (label, cmd) in enumerate(self.options):
                    option_rect = pygame.Rect(x, y + i * CONTEXT_MENU_OPTION_HEIGHT, width, CONTEXT_MENU_OPTION_HEIGHT)
                    if option_rect.collidepoint(mx, my):
                        self.hide()
                        return cmd
                # Click outside menu hides it
                if not pygame.Rect(x, y, width, height).collidepoint(mx, my):
                    self.hide()
        elif event.type == pygame.MOUSEMOTION:
            self.selected_index = None
            for i in range(len(self.options)):
                option_rect = pygame.Rect(x, y + i * CONTEXT_MENU_OPTION_HEIGHT, width, CONTEXT_MENU_OPTION_HEIGHT)
                if option_rect.collidepoint(mx, my):
                    self.selected_index = i
                    break
        return None

    def draw(self, surface):
        if not self.visible:
            return
        x, y = self.position
        width = CONTEXT_MENU_WIDTH
        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect(x, y + i * CONTEXT_MENU_OPTION_HEIGHT, width, CONTEXT_MENU_OPTION_HEIGHT)
            color = BG_COLOR if i != self.selected_index else (80, 80, 80)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, TEXT_COLOR, rect, 1)
            txt_surf = pygame.font.SysFont(None, 20).render(label, True, TEXT_COLOR)
            surface.blit(txt_surf, (x + 5, y + i * CONTEXT_MENU_OPTION_HEIGHT + 5))


class TopBar:
    def __init__(self):
        # menus: dict[str, list[tuple[label, command]]]
        self.menus = {
            "File": [
                ("Add Bone", "add_bone"),
                ("Export PNG Frames", "export_png"),
                ("Export GIF", "export_gif"),
                ("Save Project", "save"),
                ("Load Project", "load"),
                ("Close Menu", "close_menu"),
            ],
            "View": [
                ("Toggle Play", "toggle_play"),
                ("Open Export Menu", "open_export"),
                ("Open Add Bone Menu", "open_add_bone"),
            ],
        }
        self.active_menu = None

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if my <= TOPBAR_HEIGHT:
                index = mx // TOPBAR_MENU_WIDTH
                menu_names = list(self.menus.keys())
                if index < len(menu_names):
                    clicked_menu = menu_names[index]
                    if self.active_menu == clicked_menu:
                        self.active_menu = None
                    else:
                        self.active_menu = clicked_menu
                    return None
            else:
                if self.active_menu is not None:
                    dropdown_rect = pygame.Rect(
                        list(self.menus.keys()).index(self.active_menu)*TOPBAR_MENU_WIDTH,
                        TOPBAR_HEIGHT,
                        TOPBAR_MENU_WIDTH,
                        TOPBAR_DROPDOWN_HEIGHT * len(self.menus[self.active_menu])
                    )
                    if not dropdown_rect.collidepoint(mx, my):
                        self.active_menu = None
                # Check dropdown clicks
                if self.active_menu:
                    rel_x = mx - list(self.menus.keys()).index(self.active_menu)*TOPBAR_MENU_WIDTH
                    rel_y = my - TOPBAR_HEIGHT
                    item_index = rel_y // TOPBAR_DROPDOWN_HEIGHT
                    items = self.menus[self.active_menu]
                    if 0 <= item_index < len(items):
                        self.active_menu = None
                        return items[item_index][1]
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, BG_COLOR, (0, 0, surface.get_width(), TOPBAR_HEIGHT))
        for i, menu_name in enumerate(self.menus.keys()):
            rect = pygame.Rect(i * TOPBAR_MENU_WIDTH, 0, TOPBAR_MENU_WIDTH, TOPBAR_HEIGHT)
            pygame.draw.rect(surface, BTN_ACTIVE_COLOR if self.active_menu == menu_name else BTN_COLOR, rect)
            txt_surf = pygame.font.SysFont(None, 20).render(menu_name, True, TEXT_COLOR)
            txt_rect = txt_surf.get_rect(center=rect.center)
            surface.blit(txt_surf, txt_rect)

        if self.active_menu:
            menu_index = list(self.menus.keys()).index(self.active_menu)
            x = menu_index * TOPBAR_MENU_WIDTH
            y = TOPBAR_HEIGHT
            items = self.menus[self.active_menu]
            for i, (label, _) in enumerate(items):
                rect = pygame.Rect(x, y + i * TOPBAR_DROPDOWN_HEIGHT, TOPBAR_MENU_WIDTH, TOPBAR_DROPDOWN_HEIGHT)
                pygame.draw.rect(surface, BTN_ACTIVE_COLOR, rect)
                txt_surf = pygame.font.SysFont(None, 18).render(label, True, TEXT_COLOR)
                surface.blit(txt_surf, (x + 5, y + i * TOPBAR_DROPDOWN_HEIGHT + 5))



def handle_menu_click(pos, menu_state, bones, new_bone_data, export_settings):
    x, y = pos
    selected_input = None
    command = None
    # Main menu buttons (example positions)
    if menu_state == "main":
        # + Add Bone button
        add_bone_rect = pygame.Rect(300, 230, 200, 40)
        close_menu_rect = pygame.Rect(300, 290, 200, 40)
        if add_bone_rect.collidepoint(x, y):
            return "add_bone", "name", None
        elif close_menu_rect.collidepoint(x, y):
            return None, None, "back"

    elif menu_state == "add_bone":
        base_x, base_y = 180, 120
        # Input fields
        name_rect = pygame.Rect(base_x + 20, base_y + 20, 200, 30)
        length_rect = pygame.Rect(base_x + 20, base_y + 180, 200, 30)
        # Parent button
        parent_btn_rect = pygame.Rect(base_x + 20, base_y + 80, 200, 30)
        # Image button
        image_btn_rect = pygame.Rect(base_x + 20, base_y + 130, 200, 30)
        # Add and Back buttons
        add_btn_rect = pygame.Rect(base_x + 20, base_y + 230, 100, 30)
        back_btn_rect = pygame.Rect(base_x + 140, base_y + 230, 100, 30)

        if name_rect.collidepoint(x, y):
            selected_input = "name"
        elif length_rect.collidepoint(x, y):
            selected_input = "length"
        elif parent_btn_rect.collidepoint(x, y):
            # For simplicity toggle parent None <-> first bone if exists
            if bones:
                new_bone_data["parent"] = bones[0] if new_bone_data["parent"] is None else None
            selected_input = None
        elif image_btn_rect.collidepoint(x, y):
            # Change to image selection menu
            return "choose_image", None, None
        elif add_btn_rect.collidepoint(x, y):
            command = "add"
        elif back_btn_rect.collidepoint(x, y):
            command = "back"

    elif menu_state == "choose_image":
        # You will have to add your own image buttons detection here
        # For now just simulate back button at bottom
        back_btn_rect = pygame.Rect(180 + 20, 150 + 250, 100, 30)
        if back_btn_rect.collidepoint(x, y):
            command = "back"

    
    return None, selected_input, command



def handle_text_input(event, selected_input_field, data_dict):
    if selected_input_field is None:
        return
    if event.type == pygame.KEYDOWN:
        key = event.key
        if key == pygame.K_BACKSPACE:
            # Remove last char
            if len(data_dict[selected_input_field]) > 0:
                data_dict[selected_input_field] = data_dict[selected_input_field][:-1]
        elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            # You can decide what to do on Enter — here we do nothing special
            pass
        else:
            # Only accept printable characters
            if event.unicode.isprintable():
                data_dict[selected_input_field] += event.unicode



def load_image_buttons(assets_folder):
    """
    Load images from assets_folder and create thumbnail buttons.
    Returns a list of tuples: (thumbnail_surface, image_path, (x, y), rect)
    """
    image_buttons = []
    x_start, y_start = 200, 180
    padding = 10
    thumb_size = (64, 64)
    x, y = x_start, y_start

    for filename in os.listdir(assets_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            full_path = os.path.join(assets_folder, filename)
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img_thumb = pygame.transform.smoothscale(img, thumb_size)
                rect = pygame.Rect(x, y, *thumb_size)
                image_buttons.append((img_thumb, full_path, (x, y), rect))
                x += thumb_size[0] + padding
                # wrap to next line if needed (e.g. 5 per row)
                if (x - x_start) // (thumb_size[0] + padding) >= 5:
                    x = x_start
                    y += thumb_size[1] + padding
            except Exception as e:
                print(f"Failed to load image {filename}: {e}")
    return image_buttons
