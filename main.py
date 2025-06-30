import pygame
import os
import math

from bones import Bone
from timeline import Timeline
import saving
import export
import settings
import UI

# --- Constants ---
SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
FPS = settings.FPS
TIMELINE_Y = settings.TIMELINE_Y
MAX_TIME = settings.MAX_TIME
ASSETS_FOLDER = settings.ASSETS_FOLDER
SIDEBAR_WIDTH = settings.SIDEBAR_WIDTH

os.makedirs(ASSETS_FOLDER, exist_ok=True)

# --- State ---
menu_open = False
menu_state = "main"
new_bone_data = {"name": "", "length": "60", "parent": None, "image": None, "image_path": None}
selected_input_field = None
selected_image_path = ""

bones = []
selected_bone = None
play_mode = False
current_time = 0
scrubbing_timeline = False
dragging_bone = None
mouse_prev_pos = None

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprote Refactored")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

image_buttons = UI.load_image_buttons(ASSETS_FOLDER)

# Export menu state
export_settings = {
    "animation_length": "5.0",
    "fps": str(FPS),
    "total_frames": "",
    "output_folder": ASSETS_FOLDER,
    "output_gif": "animation.gif",
}
export_selected_input = None

# Initialize UI components
context_menu = UI.ContextMenu([
    ("Add Bone", "add_bone"),
    ("Export PNG Frames", "export_png"),
    ("Export GIF", "export_gif"),
    ("Save Project", "save"),
    ("Load Project", "load"),
    ("Close Menu", "close_menu"),
])

top_bar = UI.TopBar()

def add_bone():
    global new_bone_data
    try:
        length = int(new_bone_data["length"])
    except ValueError:
        length = 60
    bone = Bone(
        new_bone_data["name"],
        length,
        Timeline(),
        angle=0,
        parent=new_bone_data["parent"],
        image=new_bone_data["image"],
        offset=(0, 0),
    )
    bone.x = SCREEN_WIDTH // 2
    bone.y = SCREEN_HEIGHT // 2
    bones.append(bone)
    new_bone_data.update({"name": "", "length": "60", "parent": None, "image": None, "image_path": None})

def update_bone_angles(current_time):
    for bone in bones:
        bone.angle = bone.timeline.get_angle_at(current_time, default=bone.angle)

running = True
while running:
    screen.fill((30, 30, 30))

    y_offset = UI.TOPBAR_HEIGHT

    # Draw UI components
    top_bar.draw(screen)
    UI.draw_sidebar(screen, bones, selected_bone, font, sidebar_width=SIDEBAR_WIDTH, screen_width=SCREEN_WIDTH, y_offset=0)
    UI.draw_timeline(screen, bones, current_time, MAX_TIME, FPS, settings.FRAME_WIDTH, TIMELINE_Y, font, y_offset=y_offset)
    play_button_rect = UI.draw_play_button(screen, play_mode, font, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, y_offset=y_offset)

    if context_menu.visible:
        context_menu.draw(screen)

    shift_held = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # UI component event handling
        cmd_top = top_bar.handle_event(event)
        cmd_ctx = context_menu.handle_event(event)

        # Prioritize context menu commands if visible
        command = cmd_ctx if context_menu.visible else cmd_top

        if command is not None:
            # Handle commands from top bar or context menu
            if command == "add_bone" or command == "open_add_bone":
                menu_open = True
                menu_state = "add_bone"
                selected_input_field = "name"
            elif command == "export_png" or command == "export_gif":
                # Call your export functions accordingly
                if command == "export_png":
                    export.export_animation_frames(bones, screen)
                else:
                    export.export_animation_gif(bones, screen)
  # Implement this if you haven't
            elif command == "save":
                saving.save_project(bones)
            elif command == "load":
                print("[LOAD] Load function not implemented yet")
            elif command == "close_menu":
                menu_open = False
                menu_state = "main"
            elif command == "toggle_play":
                play_mode = not play_mode
            elif command == "open_export":
                menu_open = True
                menu_state = "export"  # you need to add export menu drawing logic below
            # Hide context menu after a command
            context_menu.hide()

        if menu_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_menu_state, new_selected_input, cmd = UI.handle_menu_click(event.pos, menu_state, bones, new_bone_data, export_settings)
                        # Handle image button clicks in choose_image menu
                if menu_state == "choose_image":
                    for thumb, path, (x, y), rect in image_buttons:
                        if rect.collidepoint(event.pos):
                            new_bone_data["image_path"] = path
                            new_bone_data["image"] = pygame.image.load(path).convert_alpha()
                            menu_state = "add_bone"
                            break

                if new_menu_state is not None:
                    menu_state = new_menu_state
                if new_selected_input is not None:
                    if menu_state == "export":
                        export_selected_input = new_selected_input
                    else:
                        selected_input_field = new_selected_input
                if cmd == "add":
                    add_bone()
                elif cmd == "back":
                    if menu_state == "main":
                        menu_open = False
                    else:
                        menu_state = "main"

            if menu_state == "export":
                UI.handle_text_input(event, export_selected_input, export_settings)

            else:
                UI.handle_text_input(event, selected_input_field, new_bone_data)


        else:
            # Normal interaction
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right-click opens context menu
                    context_menu.show(event.pos)
                elif event.button == 1:  # Left-click
                    mx, my = event.pos
                    if play_button_rect.collidepoint(mx, my):
                        play_mode = not play_mode
                    else:
                        sidebar_x = SCREEN_WIDTH - SIDEBAR_WIDTH
                        add_bone_rect = pygame.Rect(sidebar_x + 10, y_offset + 10, SIDEBAR_WIDTH - 20, 25)
                        if add_bone_rect.collidepoint(mx, my):
                            menu_open = True
                            menu_state = "add_bone"
                            selected_input_field = "name"
                        elif mx > sidebar_x:
                            for i, bone in enumerate(bones):
                                rect = pygame.Rect(sidebar_x + 10, y_offset + 40 + i * 30, SIDEBAR_WIDTH - 20, 25)
                                if rect.collidepoint(mx, my):
                                    selected_bone = bone
                                    break
                        elif my >= TIMELINE_Y + y_offset:
                            scrubbing_timeline = True
                            current_time = min(max(0, mx / (settings.FRAME_WIDTH * FPS)), MAX_TIME)
                        else:
                            for bone in reversed(bones):
                                if bone.is_clicked((mx, my)):
                                    selected_bone = bone
                                    dragging_bone = bone if bone.parent is None else None
                                    break

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_bone = None
                scrubbing_timeline = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if scrubbing_timeline:
                    current_time = min(max(0, mx / (settings.FRAME_WIDTH * FPS)), MAX_TIME)
                elif shift_held and selected_bone:
                    if mouse_prev_pos is not None:
                        dx = mx - mouse_prev_pos[0]
                        dy = my - mouse_prev_pos[1]
                        selected_bone.angle += (dx - dy) * 1.5
                        selected_bone.angle %= 360
                    mouse_prev_pos = (mx, my)
                elif dragging_bone and my < TIMELINE_Y + y_offset and mx < SCREEN_WIDTH - SIDEBAR_WIDTH:
                    dragging_bone.x = mx
                    dragging_bone.y = my

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu_open = not menu_open
                elif event.key == pygame.K_k and selected_bone:
                    selected_bone.timeline.add_keyframe(current_time, selected_bone.angle)
                    print(f"[KEYFRAME] Added: {selected_bone.name} @ {round(current_time,2)} angle={round(selected_bone.angle,1)}")
                elif event.key == pygame.K_SPACE:
                    play_mode = not play_mode
                elif event.key == pygame.K_DELETE and selected_bone:
                    bones = [b for b in bones if b != selected_bone and b.parent != selected_bone]
                    selected_bone = None
                elif event.key == pygame.K_s:
                    saving.save_project(bones)
                elif event.key == pygame.K_l:
                    print("[LOAD] Load function not implemented yet")
                elif event.key == pygame.K_e:
                    export.export_animation_frames()
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    mouse_prev_pos = pygame.mouse.get_pos()

    if not shift_held:
        mouse_prev_pos = None

    if play_mode or scrubbing_timeline:
        update_bone_angles(current_time)

    for bone in bones:
        if bone.parent is None:
            bone.update()
            bone.draw(screen, selected_bone)

    # Draw menus on top if open
    if menu_open:
        if menu_state == "main":
            UI.draw_main_menu(screen, font)
        elif menu_state == "add_bone":
            UI.draw_add_bone_menu(screen, new_bone_data, selected_input_field, font)
        elif menu_state == "choose_image":
            UI.draw_image_menu(screen, image_buttons, font)
        elif menu_state == "export":
            UI.draw_export_menu(screen, export_settings, export_selected_input, font)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
