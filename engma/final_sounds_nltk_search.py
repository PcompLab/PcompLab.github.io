"""
NLTK Word Stem Search by Final Sound
=====================================
Searches the NLTK English word corpus for words ending in /m/, /k/, and /ng/,
filtering out suffixed, compounded, and prefixed forms to retain stems.

Results:
  /m/        : 8,790 -> 1,919 (after suffix filter) -> 1,515 (after prefix filter)
  /k/ total  : 14,125 -> 2,028 (after suffix filter) -> 1,634 (after prefix filter)
    -k       : 2,613 -> 1,752 -> 1,406
    -c       : 11,272 -> 156 -> 138
    -que     : 240 -> 120 -> 90
  /ng/       : 5,913 -> 350 (after suffix filter) -> 299 (after prefix filter)

Note: a small number of words that happen to start with a prefix string
but are not actually prefixed (e.g. realm, antique, triphthong) will be
incorrectly removed. This is an accepted trade-off for simplicity.
"""

import nltk
nltk.download('words', quiet=True)
from nltk.corpus import words

english_words = words.words()
print(f'Total words in NLTK corpus: {len(english_words):,}')


# ===========================================================
# SHARED FILTER FUNCTIONS
# ===========================================================

def is_suffixed(word, suffixes):
    """Return True if word ends with any suffix, is not identical to it,
    and stripping it leaves at least 2 characters."""
    for sfx in suffixes:
        if word.endswith(sfx) and word != sfx and len(word) - len(sfx) >= 2:
            return True
    return False


# Sorted longest-first so 'counter' is checked before 'con', 'inter' before 'in', etc.
PREFIXES = sorted([
    'anti', 'ante', 'auto', 'arch',
    'be',
    'co', 'com', 'con', 'counter',
    'de', 'dis', 'demi',
    'em', 'en', 'ex', 'extra',
    'fore', 'hyper', 'hypo',
    'il', 'im', 'in', 'inter', 'intra', 'ir',
    'macro', 'mega', 'micro', 'mid', 'mini', 'mis', 'mono', 'multi',
    'non', 'out', 'over',
    'poly', 'post', 'pre', 'pro', 'pseudo',
    're', 'semi', 'sub', 'super',
    'trans', 'tri', 'un', 'under', 'uni', 'up',
    'with',
], key=len, reverse=True)

def has_prefix(word):
    """Return True if word starts with a known English prefix
    and the remainder is at least 3 characters."""
    for pfx in PREFIXES:
        if word.startswith(pfx) and len(word) - len(pfx) >= 3:
            return True
    return False


# ===========================================================
# FINAL /m/ -- spelled -m
# ===========================================================

ending_m = sorted(set(w.lower() for w in english_words if w.endswith('m')))

M_SUFFIXES = [
    # Derivational suffixes
    'ism', 'asm',
    'ium', 'eum', 'aeum', 'oeum',
    'arium', 'orium', 'erium', 'atorium', 'itorium',
    'phyllum', 'spermum', 'sporum', 'stomum',
    'dom', 'room', 'worm',
    # Compounding elements
    'bloom', 'storm', 'beam', 'stream', 'dream',
    'foam', 'gloom', 'loom',
    'arm', 'farm', 'harm', 'charm', 'warm',
    'form', 'term', 'derm', 'sperm',
    'stem', 'seam', 'gleam', 'team',
    'swim', 'swarm', 'gram', 'film',
]

after_suffix_m = [w for w in ending_m if not is_suffixed(w, M_SUFFIXES)]
stems_m = sorted(w for w in after_suffix_m if not has_prefix(w))

print()
print('=' * 55)
print('SUMMARY: words ending in -m')
print('=' * 55)
print(f'  Original total               : {len(ending_m):>6,}')
print(f'  After suffix/compound filter : {len(after_suffix_m):>6,}  ({len(ending_m) - len(after_suffix_m):>5,} removed)')
print(f'  After prefix filter          : {len(stems_m):>6,}  ({len(after_suffix_m) - len(stems_m):>5,} additional removed)')
print()
print('STEMS: words ending in -m')
print('-' * 30)
for w in stems_m:
    print(w)


# ===========================================================
# FINAL /k/ -- spelled -k, -c, -que
# ===========================================================

ending_k   = sorted(set(w.lower() for w in english_words if w.endswith('k')))
ending_c   = sorted(set(w.lower() for w in english_words if w.endswith('c')))
ending_que = sorted(set(w.lower() for w in english_words if w.endswith('que')))

K_SUFFIXES = [
    'work', 'book', 'mark', 'back', 'jack', 'lock', 'stock',
    'stack', 'track', 'pack', 'sack', 'rack', 'tack',
    'walk', 'talk', 'hawk', 'cock', 'hook', 'stalk',
]
C_SUFFIXES   = ['iac', 'ac', 'ic']   # longest first
QUE_SUFFIXES = ['esque']

after_k   = [w for w in ending_k   if not is_suffixed(w, K_SUFFIXES)]
after_c   = [w for w in ending_c   if not is_suffixed(w, C_SUFFIXES)]
after_que = [w for w in ending_que if not is_suffixed(w, QUE_SUFFIXES)]

stems_k   = sorted(w for w in after_k   if not has_prefix(w))
stems_c   = sorted(w for w in after_c   if not has_prefix(w))
stems_que = sorted(w for w in after_que if not has_prefix(w))

orig_total  = len(ending_k)  + len(ending_c)  + len(ending_que)
after_sfx   = len(after_k)   + len(after_c)   + len(after_que)
final_total = len(stems_k)   + len(stems_c)   + len(stems_que)

print()
print('=' * 55)
print('COMBINED SUMMARY: all /k/ spellings (-k, -c, -que)')
print('=' * 55)
print(f'  Original total                    : {orig_total:>6,}')
print(f'  After suffix/compound filter      : {after_sfx:>6,}  ({orig_total - after_sfx:>5,} removed)')
print(f'  After prefix filter (stems only)  : {final_total:>6,}  ({after_sfx - final_total:>5,} additional removed)')
print()
print(f'  {"Spelling":<8}  {"Original":>8}  {"After suffix":>12}  {"Stems only":>10}')
print(f'  {"-k":<8}  {len(ending_k):>8,}  {len(after_k):>12,}  {len(stems_k):>10,}')
print(f'  {"-c":<8}  {len(ending_c):>8,}  {len(after_c):>12,}  {len(stems_c):>10,}')
print(f'  {"-que":<8}  {len(ending_que):>8,}  {len(after_que):>12,}  {len(stems_que):>10,}')
print()
print('STEMS: words spelled -k')
print('-' * 30)
for w in stems_k:
    print(w)
print()
print('STEMS: words spelled -c')
print('-' * 30)
for w in stems_c:
    print(w)
print()
print('STEMS: words spelled -que')
print('-' * 30)
for w in stems_que:
    print(w)


# ===========================================================
# FINAL /ng/ -- spelled -ng
# ===========================================================

ending_ng = sorted(set(w.lower() for w in english_words if w.endswith('ng')))

NG_SUFFIXES = [
    'ing',   # running, singing, walking -- gerunds and present participles
    'ling',  # duckling, yearling -- diminutive/agentive suffix
    'long',  # lifelong, daylong -- 'long' itself is kept
    'song',  # birdsong, singsong -- 'song' itself is kept
    'hang',  # overhang -- 'hang' itself is kept
]

after_suffix_ng = [w for w in ending_ng if not is_suffixed(w, NG_SUFFIXES)]
stems_ng = sorted(w for w in after_suffix_ng if not has_prefix(w))

print()
print('=' * 55)
print('SUMMARY: words ending in -ng')
print('=' * 55)
print(f'  Original total               : {len(ending_ng):>6,}')
print(f'  After suffix/compound filter : {len(after_suffix_ng):>6,}  ({len(ending_ng) - len(after_suffix_ng):>5,} removed)')
print(f'  After prefix filter          : {len(stems_ng):>6,}  ({len(after_suffix_ng) - len(stems_ng):>5,} additional removed)')
print()
print('STEMS: words ending in -ng')
print('-' * 30)
for w in stems_ng:
    print(w)
