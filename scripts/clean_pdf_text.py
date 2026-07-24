#!/usr/bin/env python3
"""
PDF → Markdown 清洗脚本 (gonzalez-partido v2)
处理: 页眉移除、断词修复、段落重建、标题识别
"""

import re, sys

# ── 章节标题映射 ──
# 格式: (标题原文, 中文标题)
# 多行标题用 `|` 表示换行(合并时替换为空格)
TITLE_ENTRIES = [
    ('AGRADECIMIENTOS', '## 致谢'),
    ('INTRODUCCIÓN', '## 引言：革命的政党及其组织'),
    ('I. LA FUNDACIÓN (1928-1933)', '## 第一章：建党（1928-1933）'),
    ('II. DE PARTIDO DE ÉLITES | AL PARTIDO DE MASAS (1933-1938)', '## 第二章：从精英政党到群众政党（1933-1938）'),
    ('III. EL PARTIDO DE LA UNIDAD NACIONAL (1938-1945)', '## 第三章：民族团结的政党（1938-1945）'),
    ('IV. EL CONFLICTO Y LAS INSTITUCIONES: LA REVOLUCIÓN CON OBJETIVOS (1946-1952)', '## 第四章：冲突与制度：有目标的革命（1946-1952）'),
    ('IV. EL CONFLICTO Y LAS INSTITUCIONES: | LA REVOLUCIÓN CON OBJETIVOS', '## 第四章：冲突与制度：有目标的革命（1946-1952）'),
    ('V. LA CONSOLIDACIÓN DEL SISTEMA | POLÍTICO MEXICANO: EL PERIODO | DE ADOLFO RUIZ CORTINES', '## 第五章：墨西哥政治体制的巩固：阿道弗·鲁伊斯·科尔蒂内斯时期'),
    ('VI. LA PRESIDENCIA DE ALFONSO CORONA | DEL ROSAL', '## 第六章：阿方索·科罗纳·德尔·罗萨尔的党主席任期'),
    ('VII. LA PRESIDENCIA | DE CARLOS A. MADRAZO', '## 第七章：卡洛斯·A·马德拉索的党主席任期'),
    ('VII. EL INTERINATO DE LAURO ORTEGA | Y LA PRESIDENCIA DE ALFONSO MARTÍNEZ | DOMÍNGUEZ', '## 第八章：劳罗·奥尔特加的过渡期与阿方索·马丁内斯·多明格斯的党主席任期'),
    ('VIII. EL INTERINATO DE LAURO ORTEGA Y LA PRESIDENCIA DE ALFONSO MARTÍNEZ DOMÍNGUEZ', '## 第八章'),
    ('IX. EL PRI DURANTE EL GOBIERNO | DE LUIS ECHEVERRÍA', '## 第九章：路易斯·埃切维里亚政府时期的革命制度党'),
    ('X. EN EL SEXENIO DE LA REFORMA POLÍTICA', '## 第十章：政治改革的六年任期'),
    ('XI. LA NUEVA CLASE POLÍTICA (1982-1988)', '## 第十一章：新政治阶级（1982-1988）'),
    ('XII. LA LEGITIMIDAD DE LA REVOLUCIÓN | Y LA SOCIEDAD CIVIL: LA PRESIDENCIA | DE LUIS DONALDO COLOSIO', '## 第十二章：革命的合法性与公民社会：路易斯·多纳尔多·科洛西奥的党主席任期'),
    ('XIII. REFUNDACIÓN FRUSTRADA, | LIBERALISMO SOCIAL Y VIOLENCIA POLÍTICA | (1992-1994)', '## 第十三章：受挫的重建、社会自由主义与政治暴力（1992-1994）'),
    ('XIV. LA DISTANCIA NECESARIA | Y LO INEVITABLE DE LA CERCANÍA | (1994-1999)', '## 第十四章：必要的距离与不可避免的接近（1994-1999）'),
    ('EPÍLOGO', '## 尾声'),
    ('ANEXOS', '## 附录（农民/工人/人民部门组织史）'),
    ('BIBLIOGRAFÍA', '## 参考文献'),
    ('ÍNDICE ONOMÁSTICO', '## 人名索引'),
]

# 短标题(运行页眉用, 无罗马数字前缀)
SHORT_TITLE_EXTRA = {}

def to_key(s):
    """清理字符串为纯大写无格式 key"""
    s = s.upper()
    for a, b in {'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U','Ñ':'N'}.items():
        s = s.replace(a, b)
    for ch in " .',:;!?()-":
        s = s.replace(ch, '')
    return s

# 构建所有可能的 title key 映射
TITLE_MAP = {}
for raw_title, chn in TITLE_ENTRIES:
    flat = raw_title.replace('|', ' ')
    TITLE_MAP[to_key(flat)] = chn
for raw_title, chn in SHORT_TITLE_EXTRA.items():
    TITLE_MAP[to_key(raw_title)] = chn


def match_title(stripped):
    key = to_key(stripped)
    return TITLE_MAP.get(key)


def clean_pdf_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines(keepends=True)

    # ── 第1步: 移除 form feed, 移除运行页眉和页码 ──
    # 策略: 每页以 \x0c 分隔, 页首的第一个非空行如果是运行页眉则移除
    cleaned = []
    removed_headers = 0
    removed_page_nums = 0
    seen_titles = set()

    at_page_start = True  # 第一行视为页首

    for line in lines:
        stripped = line.strip()
        is_ff = '\x0c' in line

        if is_ff:
            at_page_start = True
            content_after = line.replace('\x0c', '').strip()
            if content_after:
                stripped = content_after
            else:
                cleaned.append('\n')
                continue

        if not stripped:
            if at_page_start:
                continue  # 跳过页首空行
            cleaned.append('\n')
            at_page_start = False
            continue

        if at_page_start:
            # 页首第一行 → 检查
            mapped = match_title(stripped)
            if mapped and mapped not in seen_titles:
                seen_titles.add(mapped)
                cleaned.append(mapped + '\n')
                at_page_start = False
                continue

            # 检查运行页眉: 包含章节名 + 页码(或类似模式)
            # 模式1: "PAGE_NUM  +   CHAPTER" (偶页)
            m = re.match(r'^(\d{1,3})\s{2,}(.+)$', stripped)
            if m:
                s = m.group(2).strip()
                # 检查已知章节名(模糊)
                sk = to_key(s)
                for k, v in TITLE_MAP.items():
                    short_sk = sk
                    for c in '0123456789':
                        short_sk = short_sk.replace(c, '')
                    short_k = k
                    for c in '0123456789':
                        short_k = short_k.replace(c, '')
                    if len(short_sk) > 8 and (short_sk in short_k or short_k in short_sk):
                        removed_headers += 1
                        at_page_start = False
                        break
                else:
                    # 不是已知章节名 → 保留
                    cleaned.append(stripped + '\n')
                    at_page_start = False
                continue

            # 模式2: "CHAPTER  +  spaces  +  PAGE_NUM" (奇页)
            m = re.match(r'^(.+?)\s{4,}(\d{1,3}[\w)]*)$', stripped)
            if m:
                s = m.group(1).strip()
                sk = to_key(s)
                is_hdr = False
                for k, v in TITLE_MAP.items():
                    short_sk = sk
                    for c in '0123456789':
                        short_sk = short_sk.replace(c, '')
                    short_k = k
                    for c in '0123456789':
                        short_k = short_k.replace(c, '')
                    if len(short_sk) > 8 and (short_sk in short_k or short_k in short_sk):
                        is_hdr = True
                        break
                if is_hdr:
                    removed_headers += 1
                    at_page_start = False
                    continue

            # 模式3: 纯页码或类似物
            if re.match(r'^\d{1,3}$', stripped):
                removed_page_nums += 1
                at_page_start = False
                continue
            if re.match(r'^[ivxlcdmIVXLCDM]{1,6}$', stripped):
                removed_page_nums += 1
                at_page_start = False
                continue

            # 不是标题,不是页眉,不是页码 → 保留
            cleaned.append(stripped + '\n')
            at_page_start = False

        else:
            # 非页首 → 直接保留
            # 额外检查: 是否首次出现的完整标题(非页首但有章节标题,如超长标题的第二页)
            mapped = match_title(stripped)
            if mapped and mapped not in seen_titles:
                seen_titles.add(mapped)
                cleaned.append(mapped + '\n')
            else:
                cleaned.append(stripped + '\n')

    print(f'  页眉移除: {removed_headers}, 页码移除: {removed_page_nums}, 剩余: {len(cleaned)} 行')

    text = ''.join(cleaned)

    # ── 第2步: 合并多行章节标题 ──
    lines = text.splitlines(keepends=False)
    merged = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            merged.append(lines[i])
            i += 1
            continue

        # 尝试合并1-3行后匹配
        matched = False
        for n in range(1, 4):
            if i + n > len(lines):
                break
            parts = []
            ok = True
            for j in range(n):
                ns = lines[i + j].strip()
                if not ns or (j > 0 and (ns.startswith('#') or ns.startswith('---'))):
                    ok = False
                    break
                parts.append(ns)
            if not ok:
                break
            candidate = ' '.join(parts)
            mapped = match_title(candidate)
            if mapped and mapped not in seen_titles:
                seen_titles.add(mapped)
                merged.append(mapped + '\n')
                i += n
                matched = True
                break

        if not matched:
            merged.append(lines[i])
            i += 1

    text = '\n'.join(merged)

    # ── 第3步: 修复软连字符 + OCR ──
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    text = text.replace('\u00ad', '')
    for old, new in {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
                     'ﬀ': 'ff', 'Ĳ': 'IJ', 'ĳ': 'ij', 'œ': 'oe',
                     'Œ': 'OE'}.items():
        text = text.replace(old, new)
    text = text.replace('\u00a0', ' ')

    # 修复西班牙语 OCR 粘连
    text = re.sub(r'\bdelos\b', 'de los', text)
    text = re.sub(r'\bdelas\b', 'de las', text)
    text = re.sub(r'\bquel\b', 'que el', text)
    text = re.sub(r'(\d)([A-ZÁÉÍÓÚÑ])', r'\1 \2', text)
    text = re.sub(r'\bBS\b', '', text)

    # ── 第4步: 段落重建 ──
    lines = text.splitlines(keepends=False)
    rebuilt = []
    buffer = []

    def flush(buf, out):
        if not buf:
            return
        non_empty = [l.strip() for l in buf if l.strip()]
        if not non_empty:
            return
        para = ' '.join(non_empty)
        para = re.sub(r'  +', ' ', para)
        out.append(para + '\n\n')

    for line in lines:
        s = line.strip()
        if not s:
            flush(buffer, rebuilt)
            buffer = []
        elif s.startswith('#'):
            flush(buffer, rebuilt)
            rebuilt.append(s + '\n\n')
            buffer = []
        else:
            buffer.append(line)

    flush(buffer, rebuilt)
    text = ''.join(rebuilt)

    # ── 第5步: 清理孤立章节名残留 ──
    known_names = [
        'AGRADECIMIENTOS', 'INTRODUCCIÓN',
        'LA FUNDACIÓN \\(1928-1933\\)',
        'DE PARTIDO DE ÉLITES AL PARTIDO DE MASAS.*',
        'EL PARTIDO DE LA UNIDAD NACIONAL.*',
        'EL CONFLICTO Y LAS INSTITUCIONES.*',
        'LA CONSOLIDACIÓN DEL SISTEMA POLÍTICO MEXICANO.*',
        'LA PRESIDENCIA DE ALFONSO CORONA DEL ROSAL',
        'LA PRESIDENCIA DE CARLOS A\\. MADRAZO',
        'EL INTERINATO DE LAURO ORTEGA.*',
        'EL PRI DURANTE EL GOBIERNO DE LUIS ECHEVERRÍA',
        'EN EL SEXENIO DE LA REFORMA POLÍTICA',
        'LA NUEVA CLASE POLÍTICA.*',
        'LA LEGITIMIDAD DE LA REVOLUCIÓN.*',
        'REFUNDACIÓN FRUSTRADA.*',
        'LA DISTANCIA NECESARIA.*',
        'EPÍLOGO', 'ANEXOS', 'BIBLIOGRAFÍA', 'ÍNDICE ONOMÁSTICO',
    ]
    for name in known_names:
        text = re.sub(r'^' + name + r'\s*$', '', text, flags=re.MULTILINE)

    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # 清理行首多余空格
    text = re.sub(r'^ +', '', text, flags=re.MULTILINE)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    out_lines = text.splitlines()
    headings = [l for l in out_lines if l.strip().startswith('#')]
    print(f'清洗完成:')
    print(f'  总行数: {len(out_lines)}, 非空行: {len([l for l in out_lines if l.strip()])}')
    print(f'  标题: {len(headings)}')
    for h in headings:
        print(f'  {h}')


if __name__ == '__main__':
    clean_pdf_text('_原始.txt', '_原始_clean.md')
