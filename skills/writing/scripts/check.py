#!/usr/bin/env python3
"""한국어 문서 자가 점검.

사용법: check.py <파일> | check.py -   (표준 입력)

검사 항목
  1. 금지 표현: references/banned-phrases.md 표의 첫 열(백틱) 문자열
  2. 문장 리듬: 서술식 문단에서 길이가 비슷한 문장 3개 이상 연속, 80자 넘는 문장
  3. 구분: 값: 문장 뒤 같은 줄에 붙은 "구분: 값", 문장을 끝내며 콜론으로 붙인 목록
코드 블록과 인라인 코드는 검사하지 않는다. 걸린 항목이 있으면 종료 코드 1.
"""
import re
import sys
from pathlib import Path

BANNED_MD = Path(__file__).resolve().parent.parent / "references" / "banned-phrases.md"
LONG_SENTENCE = 80     # 이 글자 수를 넘으면 경고
SIMILAR_RATIO = 1.3    # 최장/최단 비율이 이 값 이하이면 "비슷한 길이"
SIMILAR_RUN = 3        # 비슷한 길이 문장이 이만큼 이어지면 경고
MIN_LEN = 8            # 이보다 짧은 조각은 문장으로 보지 않음


def load_banned():
    """banned-phrases.md 에서 (분류, 표현, 고치는 법) 목록을 읽는다."""
    items, section = [], ""
    for line in BANNED_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*$", line)
        if m:
            items.append((section, m.group(1), m.group(2)))
    return items


def prose_lines(text):
    """(줄 번호, 검사용 줄, 서술식 여부)를 돌려준다. 코드 블록은 건너뛴다."""
    in_code = False
    for no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        clean = re.sub(r"`[^`]*`", "", line)
        s = clean.strip()
        is_prose = bool(s) and not re.match(r"([-*+>|#]|\d+[.)]\s)", s)
        yield no, clean, is_prose


def check_phrases(lines, banned):
    found = []
    for no, line, _ in lines:
        for section, phrase, fix in banned:
            if phrase in line:
                found.append((no, section, phrase, fix))
    return found


LABEL_AFTER_SENTENCE = re.compile(r"(?<![\d.])[.)]\s+([^\s.:`]{1,12}):\s")
COLON_LIST = re.compile(r"(니다|한다|이다|있다|같다):\s")


def check_labels(lines):
    """문장 뒤에 붙은 '구분: 값'과 문장 끝 콜론 목록을 찾는다."""
    found = []
    for no, line, _ in lines:
        m = LABEL_AFTER_SENTENCE.search(line)
        if m and not m.group(1).startswith("http"):
            found.append((no, f"문장 뒤 '{m.group(1)}:'", "값이 URL·경로·명령이면 앞에서 줄을 바꾸고, 짧으면 문장으로 푼다"))
        m = COLON_LIST.search(line)
        if m:
            found.append((no, f"'{m.group(0).strip()}' 뒤 목록", "콜론 앞에서 문장을 끝내고 목록은 항목으로 내린다"))
    return found


def split_sentences(paragraph):
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p for p in parts if len(p) >= MIN_LEN]


def check_rhythm(lines):
    """서술식 문단(빈 줄·개조식으로 끊긴 연속 줄)마다 문장 길이를 본다."""
    paragraphs, cur, start = [], [], None
    for no, line, is_prose in lines:
        if is_prose:
            if not cur:
                start = no
            cur.append(line.strip())
        elif cur:
            paragraphs.append((start, " ".join(cur)))
            cur = []
    if cur:
        paragraphs.append((start, " ".join(cur)))

    runs, longs = [], []
    for start, para in paragraphs:
        sents = split_sentences(para)
        for s in sents:
            if len(s) > LONG_SENTENCE:
                longs.append((start, len(s), s))
        i = 0
        while i < len(sents):
            j = i + 1
            while j < len(sents):
                window = [len(s) for s in sents[i:j + 1]]
                if max(window) / min(window) > SIMILAR_RATIO:
                    break
                j += 1
            if j - i >= SIMILAR_RUN:
                runs.append((start, [len(s) for s in sents[i:j]], sents[i:j]))
                i = j
            else:
                i += 1
    return runs, longs


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8")
    if text.startswith("---"):  # YAML frontmatter 는 검사하지 않는다
        end = text.find("\n---", 3)
        if end != -1:
            text = "\n" * text[:end + 4].count("\n") + text[end + 4:]
    lines = list(prose_lines(text))

    phrases = check_phrases(lines, load_banned())
    runs, longs = check_rhythm(lines)
    labels = check_labels(lines)

    if phrases:
        print(f"[금지 표현] {len(phrases)}건")
        for no, section, phrase, fix in phrases:
            print(f"  {no}행  {section}  '{phrase}'  → {fix}")
    if runs:
        print(f"[리듬] 길이가 비슷한 문장 연속 {len(runs)}곳")
        for start, lens, sents in runs:
            print(f"  {start}행~  길이 {lens}  시작: {sents[0][:30]}…")
    if longs:
        print(f"[긴 문장] {LONG_SENTENCE}자 초과 {len(longs)}개")
        for start, n, s in longs:
            print(f"  {start}행~  {n}자  {s[:30]}…")

    if labels:
        print(f"[구분: 값] {len(labels)}건")
        for no, what, fix in labels:
            print(f"  {no}행  {what}  → {fix}")

    if not (phrases or runs or longs or labels):
        print("걸린 항목 없음")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
