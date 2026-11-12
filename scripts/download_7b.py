"""从 ModelScope 下载 qwen2.5-vl-7b GGUF（Q4_K_M）和视觉编码器 mmproj"""
import os, sys, time, requests

OUT = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "qwen2.5vl7b")
os.makedirs(OUT, exist_ok=True)

FILES = [
    (
        "https://www.modelscope.cn/models/unsloth/Qwen2.5-VL-7B-Instruct-GGUF/resolve/master/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf",
        os.path.join(OUT, "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"),
        "主模型",
    ),
    (
        "https://www.modelscope.cn/models/unsloth/Qwen2.5-VL-7B-Instruct-GGUF/resolve/master/mmproj-Qwen2.5-VL-7B-Instruct-F16.gguf",
        os.path.join(OUT, "mmproj-Qwen2.5-VL-7B-Instruct-F16.gguf"),
        "视觉编码器",
    ),
]

def download(url, dest, label, chunk=1024*1024):
    if os.path.exists(dest) and os.path.getsize(dest) > 100*1024*1024:
        print(f"[跳过] {label} 已存在: {dest}  {os.path.getsize(dest)/1024/1024:.1f} MB")
        return True

    headers = {"User-Agent": "Mozilla/5.0"}
    # 支持断点续传
    existing = os.path.getsize(dest) if os.path.exists(dest) else 0
    if existing > 0:
        headers["Range"] = f"bytes={existing}-"
        print(f"[续传] {label} 已有 {existing/1024/1024:.1f} MB")

    r = requests.get(url, headers=headers, stream=True, timeout=300, allow_redirects=True)
    if r.status_code not in (200, 206):
        print(f"[失败] {label} HTTP {r.status_code}")
        return False

    mode = "ab" if (r.status_code == 206 and existing > 0) else "wb"
    total = int(r.headers.get("Content-Length", 0)) + (existing if mode == "ab" else 0)
    start = time.time()
    done = existing

    with open(dest, mode) as f:
        for block in r.iter_content(chunk):
            if not block:
                continue
            f.write(block)
            done += len(block)
            elapsed = time.time() - start
            speed = done / elapsed if elapsed > 0 else 0
            pct = (done / total * 100) if total else 0
            print(f"  {label}: {done/1024/1024:.0f}/{total/1024/1024:.0f} MB  "
                  f"{speed/1024:.0f} KB/s  {pct:.1f}%  ", end="\r", flush=True)

    print(f"\n[完成] {label}  用时 {time.time()-start:.0f}s  大小 {done/1024/1024:.1f} MB")
    return True

ok = True
for url, dest, label in FILES:
    ok &= download(url, dest, label)
print(f"\n{'全部完成' if ok else '有文件失败'}，目录: {OUT}")
