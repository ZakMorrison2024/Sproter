import pygame
import os
from PIL import Image

def export_animation_frames(
    bones,
    screen,
    *,
    total_frames=None,
    animation_length=None,  # in seconds
    fps=60,
    output_folder="exported_frames"
):
    """
    Export animation frames as PNG images.

    Args:
        bones: list of Bone instances.
        screen: pygame display Surface.
        total_frames: int, total frames to export. Overrides animation_length if set.
        animation_length: float, seconds of animation duration.
        fps: frames per second.
        output_folder: folder to save PNG frames.

    If total_frames is None, calculated from animation_length * fps.
    If animation_length is None, defaults to 5.0 seconds.
    """
    if animation_length is None and total_frames is None:
        animation_length = 5.0

    if total_frames is None:
        total_frames = int(animation_length * fps)
    elif total_frames <= 0:
        raise ValueError("total_frames must be positive")

    os.makedirs(output_folder, exist_ok=True)
    clock = pygame.time.Clock()

    for frame_idx in range(total_frames):
        current_time = frame_idx / fps

        screen.fill((30, 30, 30))

        for bone in bones:
            bone.angle = bone.timeline.get_angle_at(current_time, default=bone.angle)

        for bone in bones:
            if bone.parent is None:
                bone.update()
                bone.draw(screen, None)

        filename = os.path.join(output_folder, f"frame_{frame_idx:04d}.png")
        pygame.image.save(screen, filename)

        clock.tick(fps // 2)

    print(f"[EXPORT] Exported {total_frames} frames to '{output_folder}'")


def export_animation_gif(
    bones,
    screen,
    *,
    total_frames=None,
    animation_length=None,
    fps=60,
    output_gif="exported_animation.gif"
):
    """
    Export animation as an animated GIF.

    Args:
        bones: list of Bone instances.
        screen: pygame display Surface.
        total_frames: int, total frames to export.
        animation_length: float, seconds duration.
        fps: frames per second.
        output_gif: filename for the GIF.

    If total_frames is None, calculated from animation_length * fps.
    If animation_length is None, defaults to 5.0 seconds.
    """
    if animation_length is None and total_frames is None:
        animation_length = 5.0

    if total_frames is None:
        total_frames = int(animation_length * fps)
    elif total_frames <= 0:
        raise ValueError("total_frames must be positive")

    frames = []

    for frame_idx in range(total_frames):
        current_time = frame_idx / fps

        screen.fill((30, 30, 30))

        for bone in bones:
            bone.angle = bone.timeline.get_angle_at(current_time, default=bone.angle)

        for bone in bones:
            if bone.parent is None:
                bone.update()
                bone.draw(screen, None)

        raw_str = pygame.image.tostring(screen, "RGBA", False)
        pil_image = Image.frombytes("RGBA", screen.get_size(), raw_str)
        frames.append(pil_image)

    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0
    )

    print(f"[EXPORT] GIF saved as '{output_gif}'")
