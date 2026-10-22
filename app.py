import os, uuid, time, shutil, subprocess, threading
from flask import Flask, request, jsonify, send_file, send_from_directory, abort

CODE = "150140"
BASE = "/tmp/jobs"
os.makedirs(BASE, exist_ok=True)
app = Flask(__name__, static_folder="static", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 600 * 1024 * 1024
jobs = {}


def ok():
    return (request.headers.get("X-Code") or request.args.get("c")) == CODE


def cleanup():
    now = time.time()
    for jid in list(jobs):
        if now - jobs[jid]["t"] > 3600:
            shutil.rmtree(os.path.join(BASE, jid), ignore_errors=True)
            jobs.pop(jid, None)


def run(jid, args, dur):
    j = jobs[jid]
    p = subprocess.Popen(args, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True)
    for line in p.stdout:
        if line.startswith("out_time_ms=") and dur:
            try:
                v = int(line.split("=")[1]) / 1e6 / dur * 100
                j["pct"] = max(0, min(99, int(v)))
            except ValueError:
                pass
    p.wait()
    out = os.path.join(BASE, jid, "out.mp4")
    if p.returncode == 0 and os.path.exists(out):
        j["state"] = "done"
        j["pct"] = 100
        j["size"] = os.path.getsize(out)
    else:
        j["state"] = "error"


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/check", methods=["POST"])
def check():
    return jsonify(ok=ok())


@app.route("/upload", methods=["POST"])
def upload():
    if not ok():
        abort(403)
    cleanup()
    f = request.files.get("file")
    if not f:
        abort(400)
    jid = uuid.uuid4().hex[:12]
    d = os.path.join(BASE, jid)
    os.makedirs(d)
    src = os.path.join(d, "in")
    f.save(src)
    q = max(10, min(100, int(request.form.get("q", 80))))
    mh = int(request.form.get("mh", 0))
    pre = "veryfast" if request.form.get("pr") == "veryfast" else "ultrafast"
    crf = round(36 - (q - 10) / 90 * 18)
    try:
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", src], text=True).strip())
    except Exception:
        dur = 0
    a = ["ffmpeg", "-y", "-i", src, "-c:v", "libx264", "-preset", pre,
         "-crf", str(crf), "-pix_fmt", "yuv420p", "-threads", "1"]
    if mh:
        a += ["-vf", "scale=-2:'min(%d,ih)'" % mh]
    a += ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
          "-progress", "pipe:1", "-nostats", os.path.join(d, "out.mp4")]
    jobs[jid] = {"state": "run", "pct": 0, "size": 0, "t": time.time()}
    threading.Thread(target=run, args=(jid, a, dur), daemon=True).start()
    return jsonify(id=jid)


@app.route("/status/<jid>")
def status(jid):
    if not ok():
        abort(403)
    j = jobs.get(jid)
    if not j:
        return jsonify(state="gone")
    return jsonify(state=j["state"], pct=j["pct"], size=j["size"])


@app.route("/result/<jid>")
def result(jid):
    if not ok():
        abort(403)
    j = jobs.get(jid)
    if not j or j["state"] != "done":
        abort(404)
    return send_file(os.path.join(BASE, jid, "out.mp4"),
                     as_attachment=True, download_name="video-ipv.mp4")
