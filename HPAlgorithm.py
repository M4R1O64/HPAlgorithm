# ANSI 컬러 코드 정의
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[1;94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
SORT = "\033[1;32m"

def log(msg, level=0, color=RESET):
    indent = "  " * level
    print(f"{color}{indent}{msg}{RESET}")

# --- Permutation 확장 ---
def extend_permutation(pi):
    pi_ext = [0] + pi + [len(pi) + 1]
    log(f"[EXTEND]: {pi_ext}", 0, BLUE)
    return pi_ext

# --- Reversal ---
def reversal(pi_ext, i, j):
    if i > j:
        i, j = j, i
    if i == j:
        new_pi = pi_ext[:i] + [-pi_ext[i]] + pi_ext[i+1:]
    else:
        new_pi = pi_ext[:i] + [-x for x in reversed(pi_ext[i:j+1])] + pi_ext[j+1:]
    log(f"[REV] ({i}, {j}): {new_pi}", 1, CYAN)
    return new_pi

# --- Oriented Pairs ---
def find_oriented_pairs(pi_ext):
    pairs = []
    n = len(pi_ext)
    for i in range(n):
        for j in range(i+1, n):
            a, b = pi_ext[i], pi_ext[j]
            if (a * b < 0) and (abs(a) - abs(b) in (-1,1)):
                pairs.append((i, j))
    log(f"[ORIENTED PAIRS]: {pairs}", 1, GREEN)
    return pairs

def get_oriented_reversal_interval(pi_ext, pair):
    i, j = pair
    if i > j:
        i, j = j, i
    s = pi_ext[i] + pi_ext[j]
    if s == 1:
        a, b = i, j - 1
    elif s == -1:
        a, b = i + 1, j
    else:
        return None
    if b > len(pi_ext) - 2:
        b = len(pi_ext) - 2
    if a > b:
        return None
    log(f"[ORIENTED INTERVAL] {pair}: ({a}, {b})", 2, YELLOW)
    return (a, b)

def count_oriented_pairs(pi_ext):
    count = len(find_oriented_pairs(pi_ext))
    log(f"[COUNT]: {count}", 1, GREEN)
    return count

def algorithm_1_step(pi_ext):
    pairs = find_oriented_pairs(pi_ext)
    if not pairs:
        log("NO ORIENTED PAIRS FOUND", 1, YELLOW)
        return None, pi_ext
    best_score = -1
    best_pi = pi_ext
    best_interval = None
    for pair in pairs:
        interval = get_oriented_reversal_interval(pi_ext, pair)
        if interval is None:
            continue
        new_pi = reversal(pi_ext, interval[0], interval[1])
        score = count_oriented_pairs(new_pi)
        if score > best_score:
            best_score = score
            best_pi = new_pi
            best_interval = interval
    if best_interval is not None and best_pi != pi_ext:
        log(f"[AG1] SELECTED OPTIMAL SCORE: {best_score}", 1, RED)
        return best_interval, best_pi
    return None, pi_ext

# --- Framed Intervals & Hurdles ---
def find_framed_intervals_direct(pi_ext):
    intervals = []
    n = len(pi_ext)
    for i in range(1, n-1):
        for j in range(i, n-1):
            a = pi_ext[i]
            b = pi_ext[j]
            if a == b:
                continue
            if a > 0 and b > 0:
                lo, hi = min(a, b), max(a, b)
                required = set(range(lo, hi+1))
                sub = set(x for x in pi_ext[i:j+1] if x > 0)
                if sub == required:
                    intervals.append((i, j))
            elif a < 0 and b < 0:
                lo, hi = min(a, b), max(a, b)
                required = set(range(lo, hi+1))
                sub = set(x for x in pi_ext[i:j+1] if x < 0)
                if sub == required:
                    intervals.append((i, j))
    log(f"[FRAMED]: {intervals}", 1, GREEN)
    return intervals

def find_minimal_intervals(intervals):
    minimal = []
    for a, b in intervals:
        contains_inner = any(a <= c and d <= b and (c,d) != (a,b) for c,d in intervals)
        if not contains_inner:
            minimal.append((a,b))
    log(f"[MINNIMAL]: {minimal}", 1, GREEN)
    return minimal

def is_continuous(h1, h2, all_intervals):
    a1, b1 = h1
    a2, b2 = h2
    if b1 + 1 != a2:
        return False
    for (c,d) in all_intervals:
        if (c,d) != (a1,b1) and (c,d) != (a2,b2):
            if a1 <= c <= b1 and a2 <= d <= b2:
                return True
    return False

def cut_hurdle(pi_ext, hurdle):
    log(f"[CUTTING]: {hurdle}", 0, BOLD)
    start, end = hurdle
    hurdle_vals = pi_ext[start:end+1]
    min_val = min(abs(x) for x in hurdle_vals)
    target_val = min_val - 1
    try:
        target_idx = pi_ext.index(target_val)
    except ValueError:
        target_idx = start
    min_idx_in_hurdle = start + next(i for i,x in enumerate(hurdle_vals) if abs(x)==min_val)
    i, j = target_idx, min_idx_in_hurdle
    if i > j:
        i, j = j, i
    new_pi = reversal(pi_ext, i, j)
    log(f"[CUTTING INTERVAL]: ({i}, {j})", 1, RED)
    return (i,j), new_pi

def merge_hurdles(pi_ext, hurdles):
    if len(hurdles) < 2:
        return None, pi_ext
    hurdles_sorted = sorted(hurdles)
    n = len(hurdles_sorted)
    for i in range(n-1):
        a1,b1 = hurdles_sorted[i]
        for j in range(i+1,n):
            a2,b2 = hurdles_sorted[j]
            if is_continuous((a1,b1),(a2,b2),hurdles_sorted):
                continue
            interval = (a1,b2)
            if interval[1] > len(pi_ext)-2:
                continue
            new_pi = reversal(pi_ext, interval[0], interval[1])
            pair_count = count_oriented_pairs(new_pi)
            new_framed = find_framed_intervals_direct(new_pi)
            new_hurdles = find_minimal_intervals(new_framed)
            if pair_count > 0 or len(new_hurdles) < len(hurdles):
                log(f"[MERGED]: {interval}", 1, RED)
                return interval, new_pi
    return None, pi_ext

def reduce_hurdle_direct(pi_ext):
    framed = find_framed_intervals_direct(pi_ext)
    hurdles = find_minimal_intervals(framed)
    if not hurdles:
        log("[REDUCE] NO HURDLES", 1, YELLOW)
        return None, pi_ext
    n = len(hurdles)
    if n % 2 == 1:
        return cut_hurdle(pi_ext, hurdles[0])
    i = 0
    while i < n-1:
        start = i
        end = i
        while end+1<n and hurdles[end][1]+1 >= hurdles[end+1][0]:
            end += 1
        if end > start:
            interval = (hurdles[start][0], hurdles[end][1])
            new_pi = reversal(pi_ext, interval[0], interval[1])
            return interval, new_pi
        i = end+1
    interval = (hurdles[0][1], hurdles[-1][0])
    new_pi = reversal(pi_ext, interval[0], interval[1])
    return interval, new_pi

# --- Sign Fix ---
def fix_sign_only(pi_ext):
    for i in range(1,len(pi_ext)-1):
        v = pi_ext[i]
        if abs(v)==i and v<0:
            new_pi = reversal(pi_ext,i,i)
            log(f"[FIXED] {i}",0,YELLOW)
            return (i,i), new_pi
    return None, pi_ext

# --- Main HP Algorithm ---
def hp_algorithm(pi):
    log("======= HP START =======",0,BOLD)
    pi_ext = extend_permutation(pi)
    reversals = []
    seen = set()
    step = 1
    while True:
        log(f"\n[STEP {step}]: {pi_ext}",0,BLUE)
        if pi_ext == list(range(len(pi_ext))):
            log("+= SORTED =+",0,SORT)
            break
        key = tuple(pi_ext)
        if key in seen:
            log("LOOPED, TERMINATING",0,RED)
            break
        seen.add(key)

        # Algorithm 1
        interval, new_pi = algorithm_1_step(pi_ext)
        if interval is not None and new_pi != pi_ext:
            reversals.append(interval)
            pi_ext = new_pi
            step += 1
            continue

        # Hurdle reduction
        interval, new_pi = reduce_hurdle_direct(pi_ext)
        if interval is not None and new_pi != pi_ext:
            reversals.append(interval)
            pi_ext = new_pi
            step += 1
            continue

        # Fallback: fix sign only
        interval, new_pi = fix_sign_only(pi_ext)
        if interval is not None and new_pi != pi_ext:
            reversals.append(interval)
            pi_ext = new_pi
            step += 1
            continue

        log("NO FURTHER STEPS POSSIBLE",0,YELLOW)
        break
    log("======= HP ENDED =======",0,BOLD)
    return reversals

if __name__=="__main__":
    n = int(input())
    final = list(map(int,input().split()))
    reversals = hp_algorithm(final)
    print(len(reversals))
    for a,b in reversed(reversals):
        print(a,b)
