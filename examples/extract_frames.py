# extract_frames.py
import cv2, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--video", required=True, help="Path to input video")
parser.add_argument("--out", required=True, help="Output folder for frames")
parser.add_argument("--count", type=int, default=3, help="How many frames to extract (evenly spaced)")
args = parser.parse_args()

os.makedirs(args.out, exist_ok=True)
cap = cv2.VideoCapture(args.video)
if not cap.isOpened():
    raise SystemExit(f"Could not open video: {args.video}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
duration = frame_count / fps
times = [duration * (i+1)/(args.count+1) for i in range(args.count)]
frame_indices = [int(t * fps) for t in times]

for idx in frame_indices:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if not ret: continue
    out_path = os.path.join(args.out, f"frame_{idx}.png")
    cv2.imwrite(out_path, frame)
    print("wrote", out_path)

cap.release()
print("done.")
