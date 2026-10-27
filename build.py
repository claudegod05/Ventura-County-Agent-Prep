#!/usr/bin/env python3
"""Build dist/index.html from the question bank, drafted answers, glossary and app template.

Usage: python3 build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BANK = ROOT / "content" / "question-bank.md"
ANSWERS = ROOT / "content" / "answers"
GLOSSARY = ROOT / "content" / "glossary.json"
TEMPLATE = ROOT / "src" / "app.html"
OUT = ROOT / "dist" / "index.html"

ANSWER_FIELDS = ("summary", "answer", "keyPoints", "sources", "lastVerified", "confidence", "verify", "drills")


def parse_bank():
    sections, questions = [], {}
    current = None
    for line in BANK.read_text().splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            current = {"n": int(m.group(1)), "title": m.group(2).strip(), "ids": []}
            sections.append(current)
            continue
        m = re.match(r"^(\d+)\. (.+)$", line)
        if m and current:
            qid = int(m.group(1))
            current["ids"].append(qid)
            questions[qid] = {"id": qid, "s": current["n"], "t": m.group(2).strip(), "a": None}
    return sections, questions


def load_answers(questions):
    problems = []
    for path in sorted(ANSWERS.glob("s*.json")):
        data = json.loads(path.read_text())
        for a in data.get("answers", []):
            qid = a.get("id")
            if qid not in questions:
                problems.append(f"{path.name}: unknown question id {qid}")
                continue
            drills = []
            for i, d in enumerate(a.get("drills") or []):
                ok = (
                    isinstance(d.get("q"), str)
                    and isinstance(d.get("choices"), list)
                    and len(d["choices"]) >= 2
                    and isinstance(d.get("answer"), int)
                    and 0 <= d["answer"] < len(d["choices"])
                )
                if ok:
                    drills.append({"q": d["q"], "c": d["choices"], "a": d["answer"], "x": d.get("explain", "")})
                else:
                    problems.append(f"Q{qid}: drill {i} malformed, skipped")
            entry = {k: a.get(k) for k in ANSWER_FIELDS}
            entry["drills"] = drills
            questions[qid]["a"] = entry
    return problems


def main():
    sections, questions = parse_bank()
    problems = load_answers(questions)
    glossary = json.loads(GLOSSARY.read_text()) if GLOSSARY.exists() else []
    content = {
        "sections": sections,
        "q": {str(k): v for k, v in questions.items()},
        "glossary": glossary,
    }
    payload = json.dumps(content, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.read_text().replace("__CONTENT__", payload)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)

    answered = sum(1 for q in questions.values() if q["a"])
    drills = sum(len(q["a"]["drills"]) for q in questions.values() if q["a"])
    missing = [q["id"] for q in questions.values() if not q["a"]]
    print(f"{len(sections)} sections, {len(questions)} questions, {answered} answered, {drills} drills, {len(glossary)} glossary terms")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
    if missing:
        print(f"missing answers: {missing}")
    for p in problems:
        print("warning:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
