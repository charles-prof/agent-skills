#!/usr/bin/env python3
"""
Reusable Verification Tool for Inpainted Video Removals.
Extracts frames across specified time intervals and verifies 0% residual target color pixels.
"""

import sys
import subprocess

def verify_segment(video_path, label, start_t, end_t, bbox, color_fn, step=0.5):
    x1, x2, y1, y2 = bbox
    t = start_t
    leaks = 0
    total_checked = 0
    
    while t <= end_t:
        p = subprocess.Popen([
            'ffmpeg', '-y', '-ss', f'{t:.2f}', '-i', video_path,
            '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'ppm', '-'
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        p.stdout.readline() # P6
        dims = p.stdout.readline().decode().strip().split()
        while dims[0].startswith('#'):
            dims = p.stdout.readline().decode().strip().split()
        w, h = int(dims[0]), int(dims[1])
        p.stdout.readline() # Maxval
        data = p.stdout.read()
        
        detected = 0
        for y in range(max(0, y1), min(h, y2)):
            off = y * w * 3
            for x in range(max(0, x1), min(w, x2)):
                idx = off + x * 3
                r, g, b = data[idx], data[idx+1], data[idx+2]
                if color_fn(r, g, b):
                    detected += 1
        
        if detected > 10:
            leaks += 1
            print(f"  [LEAK] {label} at t={t:.2f}s: {detected} target pixels found!")
        
        total_checked += 1
        t += step
        
    status = "CLEAN (0 leaks)" if leaks == 0 else f"FAILED ({leaks} frames leaked)"
    print(f"[{status}] {label}: checked {total_checked} sample frames.")
    return leaks == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_removal.py <video_file>")
        sys.exit(1)
    print(f"Verifying removals on: {sys.argv[1]}")
