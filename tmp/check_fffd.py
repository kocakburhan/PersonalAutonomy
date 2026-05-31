import re
with open('docs/superpowers/plans/2026-05-27-personalautonomy-plan.md', 'rb') as f:
    data = f.read()
text = data.decode('utf-8', errors='replace')
total = text.count('\ufffd')
print(f"Total FFFD in file: {total}")

# Word context
wf = {}
for line in text.split('\n'):
    for m in re.finditer(r'\S*\ufffd\S*', line):
        w = m.group()
        wf[w] = wf.get(w, 0) + 1

with open('tmp/rem_fffd.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total FFFD in file: {total}\n\n")
    out.write(f"Unique corrupted words: {len(wf)}\n")
    out.write(f"Total word occurrences: {sum(wf.values())}\n\n")
    for w, c in sorted(wf.items(), key=lambda x: -x[1]):
        escaped = w.encode('unicode-escape').decode('ascii')
        out.write(f"{c:3d} | {escaped}\n")

# Standalone count
standalone = 0
for i, ch in enumerate(text):
    if ch == '\ufffd':
        prev = text[i-1] if i > 0 else '\n'
        nxt = text[i+1] if i < len(text)-1 else '\n'
        if not (prev.isalnum() or nxt.isalnum() or prev in "'\"" or nxt in "'\""):
            standalone += 1

print(f"Standalone (non-word) FFFD: {standalone}")
print(f"In-word FFFD: {total - standalone}")
