class Keyframe:
    def __init__(self, time, angle):
        self.time = time
        self.angle = angle

class Timeline:
    def __init__(self):
        self.keyframes = []
    
    def add_keyframe(self, time, angle):
        self.keyframes.append(Keyframe(time, angle))
        self.keyframes.sort(key=lambda k: k.time)

    def get_angle_at(self, time, default=None):
        if not self.keyframes:
            return default if default is not None else 0
        if len(self.keyframes) == 1 or time <= self.keyframes[0].time:
            return self.keyframes[0].angle
        for i in range(len(self.keyframes) - 1):
            k1 = self.keyframes[i]
            k2 = self.keyframes[i + 1]
            if k1.time <= time <= k2.time:
                t = (time - k1.time) / (k2.time - k1.time)
                return k1.angle * (1 - t) + k2.angle * t
        return self.keyframes[-1].angle
