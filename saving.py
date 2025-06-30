import json
import os

def save_project(bones, filename="project_save.json"):
    """
    Save the current project state (bones and their timelines) to a JSON file.
    """
    data = []
    for bone in bones:
        bone_data = {
            "name": bone.name,
            "length": bone.length,
            "angle": bone.angle,
            "x": bone.x,
            "y": bone.y,
            "parent": bone.parent.name if bone.parent else None,
            "image_path": bone.image_path if hasattr(bone, "image_path") else None,
            "timeline": [
                {"time": k.time, "angle": k.angle} for k in bone.timeline.keyframes
            ]
        }
        data.append(bone_data)

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[SAVE] Project saved to {filename}")
    except Exception as e:
        print(f"[SAVE ERROR] Failed to save project: {e}")

def load_project(bones, filename="project_save.json", bone_class=None, timeline_class=None):
    """
    Load project data from JSON file and rebuild bones list.

    Args:
        bones: list to fill with loaded bones (usually empty).
        bone_class: class Bone, needed to instantiate.
        timeline_class: class Timeline, to instantiate timelines.

    Returns:
        List of bones loaded.
    """
    if bone_class is None or timeline_class is None:
        raise ValueError("bone_class and timeline_class must be provided")

    if not os.path.isfile(filename):
        print(f"[LOAD] No save file found at {filename}")
        return []

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[LOAD ERROR] Failed to load project: {e}")
        return []

    name_to_bone = {}
    loaded_bones = []

    # First pass: create bones without parents
    for bone_data in data:
        bone = bone_class(
            bone_data["name"],
            bone_data["length"],
            timeline_class(),
            angle=bone_data.get("angle", 0),
            parent=None,
            image=None,
            offset=(0, 0),
        )
        bone.x = bone_data.get("x", 0)
        bone.y = bone_data.get("y", 0)
        bone.image_path = bone_data.get("image_path", None)
        # TODO: Load image from path if you want here
        name_to_bone[bone.name] = bone
        loaded_bones.append(bone)

    # Second pass: assign parents and timelines
    for bone_data in data:
        bone = name_to_bone[bone_data["name"]]
        parent_name = bone_data.get("parent")
        if parent_name:
            bone.parent = name_to_bone.get(parent_name)
        timeline_data = bone_data.get("timeline", [])
        for k in timeline_data:
            bone.timeline.add_keyframe(k["time"], k["angle"])

    print(f"[LOAD] Loaded {len(loaded_bones)} bones from {filename}")
    return loaded_bones
