import os, tempfile, subprocess
import shutil
from colorama import Fore
from PIL import Image, features, UnidentifiedImageError, ImageOps
from multiprocessing import Pool
from pathlib import Path


def save_with_avifenc(img, file_path, file_name):
    base = os.path.splitext(file_name)[0]
    out_file_name = f"{base}.avif"
    out_file_path = os.path.join(out_dir, out_file_name)
    done_file_path = os.path.join(done_dir, file_name)

    tmp = None
    cq = 30
    try:
        fd, tmp = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        img = ImageOps.exif_transpose(img)
        img.save(tmp, format="PNG")
        # cmd = ["avifenc", "--min", "0", "--max", "63", "-a", "end-usage=q", "-a", "cq-level=18", tmp, out_path]
        cmd = ["avifenc", "--min", "0", "--max", "63", "-a", "end-usage=q", "-a", f"cq-level={cq}", tmp, out_file_path]
        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        print("`avifenc` not found — install libavif-bin.")
    except Exception as e:
        print("[avifenc] failed:", e)
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
        shutil.move(file_path, done_file_path)
        print(Fore.GREEN, "✅ Saved AVIF with avifenc:", out_file_path, Fore.RESET)
    print(Fore.RED, "❌ Could not save as AVIF.", Fore.RESET)
    return False


def worker(src_path):
    file_path = str(src_path)
    file_name = os.path.basename(file_path)
    if os.path.isdir(file_path):
        return None

    if report_size(file_path) < 500:
        shutil.move(file_path, os.path.join(out_dir, file_name))
        return None

    try:
        img = Image.open(file_path)
        img = ImageOps.exif_transpose(img)
        save_with_avifenc(img, file_path, file_name)
    except UnidentifiedImageError:
        pass

    if file_path.endswith(source_extention):
        compress_video_av1(file_path, os.path.join(out_dir, file_name.replace(f'.{source_extention}', '.mkv')), crf=30, cpu_used=8)
        shutil.move(file_path, os.path.join(done_dir, file_name))
        return False

    return os.path.join(done_dir, file_name)


def compress_video_av1(input_path, output_path, crf=30, cpu_used=16):
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libaom-av1",
        "-pix_fmt", "yuv420p10le",  # fix black screen issue
        "-crf", str(crf),
        "-b:v", "0",  # required for CRF mode
        "-cpu-used", str(cpu_used),
        "-c:a", "libopus",
        "-b:a", "96k",
        output_path
    ]
    subprocess.run(cmd, check=True)


def report_size(file_path):
    return round(os.path.getsize(file_path) / 1024, 2)


if __name__ == "__main__":
    source_path = "C:\\Users\\Sharad Raval\\Downloads"
    # source_path = "/home/sharad-raval/Downloads"
    out_dir = os.path.join(source_path, "Output")
    done_dir = os.path.join(source_path, 'Done')

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(done_dir, exist_ok=True)

    source_extention = 'jpg'
    # source_extention = 'jpeg'
    # source_extention = 'png'
    images = list(Path(source_path).glob(f"*.{source_extention}"))
    with Pool(processes=8) as p:
        results = p.map(worker, images)
    print("Converted:", results)

    source_extention = 'mp4'
    # source_extention = 'mkv'
    videos = list(Path(source_path).glob(f"*.{source_extention}"))
    with Pool(processes=1) as p:
        results = p.map(worker, videos)
    print("Converted:", results)
