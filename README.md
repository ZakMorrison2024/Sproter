# Sproter
LOOOOOOOOOOOOOOOOOOOL
Sprote Refactored - Skeletal Animation Editor
=============================================

A 2D skeletal animation editor built using Pygame. Create, animate, and export bone-based sprite animations with support for keyframes, image attachments, and timeline control.

Project Features
----------------
- Intuitive GUI with context and top bar menus.
- Add and connect bones with optional images.
- Keyframe timeline system with interpolation.
- Export frames as PNGs or animated GIFs.
- Save and load bone projects in JSON format.
- Drag and rotate bones in viewport.
- Modular codebase with settings, UI, and export logic separated.

Requirements
------------
- Python 3.8+
- `pygame`
- `Pillow`

Install requirements:
```
pip install pygame Pillow
```

Running the Project
-------------------
To start the animation editor:
```
python main.py
```

Assets
------
Place your sprite images in the `assets/` folder. Use the `Choose Image` button when adding bones to attach a visual sprite.

Usage Tips
----------
- Right-click anywhere to open the context menu.
- Use the top bar to access File and View operations.
- Use SHIFT + drag to rotate bones.
- Press `K` to add a keyframe for the selected bone at the current time.
- Press `SPACE` to play/pause animation playback.
- Press `M` to open/close the menu manually.
- Press `DELETE` to remove a selected bone (and its children).
- Use `S` to save and `L` to (placeholder) load.

Keyboard Shortcuts
------------------
- `K`: Add keyframe at current time
- `SPACE`: Toggle play mode
- `S`: Save project
- `L`: Load project (not implemented)
- `M`: Toggle menu
- `DELETE`: Delete selected bone

Exporting Animations
--------------------
From the context menu or top bar:
- Export PNG frames: Saves all frames to `/exported_frames`.
- Export GIF: Saves a looping GIF as `animation.gif`.

Future Development
------------------
- Complete the load project system.
- Add better UI layout and polish.
- Include onion skinning and ghost preview frames.
- Support FK/IK animation logic.

File Structure
--------------
- `main.py`: Main event loop and state manager
- `bones.py`: Bone logic and hierarchy
- `timeline.py`: Keyframe system and interpolation
- `export.py`: PNG/GIF exporting
- `saving.py`: Project save/load (JSON)
- `UI.py`: GUI drawing and event handling
- `settings.py`: Configurable constants
- `assets/`: Folder for images used as bone visuals

License
-------
MIT License (or specify if otherwise)

Author
------
Zak Morrison
