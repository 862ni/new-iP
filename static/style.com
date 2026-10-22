:root{--bg:#0a1220;--p:#121c2f;--ink:#e8eef9;--mute:#9aaac4;--line:#24334f;--acc:#6c8bff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,Tahoma,sans-serif;line-height:1.6}
main{max-width:640px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:30px;margin:8px 0;direction:ltr;text-align:right}h1 b{color:var(--acc)}
.sub,.hint,.st,.sz{color:var(--mute);font-size:14px;margin:4px 0}
.drop{display:block;border:2px dashed var(--line);background:var(--p);border-radius:18px;padding:34px 16px;text-align:center;cursor:pointer}
.drop input{display:none}.drop strong{display:block;font-size:19px}
.ctl,.card{background:var(--p);border:1px solid var(--line);border-radius:14px;padding:14px;margin-top:14px}
.row{margin-bottom:12px}.row label{display:flex;justify-content:space-between;font-weight:600}
input[type=range]{width:100%;accent-color:var(--acc)}
select{width:100%;font:inherit;padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
button{font:inherit;font-weight:600;border:0;border-radius:10px;padding:10px 16px;background:var(--acc);color:#0a1220;cursor:pointer}
button:disabled{opacity:.5}
a.dl{display:inline-block;background:var(--acc);color:#0a1220;font-weight:600;padding:10px 16px;border-radius:10px;text-decoration:none;margin-top:8px}
.nm{font-weight:600;direction:ltr;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.good{color:#4fd18b;font-weight:700}.err{color:#ff8a7a}
video{width:100%;max-height:260px;border-radius:10px;background:#000;margin-top:8px}
.gate{position:fixed;inset:0;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:24px;z-index:9}
.gate>div{background:var(--p);border:1px solid var(--line);border-radius:18px;padding:24px;width:100%;max-width:360px;text-align:center}
.gate input{font-size:22px;letter-spacing:6px;text-align:center;padding:12px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%;margin:12px 0;direction:ltr}
[hidden]{display:none!important}
