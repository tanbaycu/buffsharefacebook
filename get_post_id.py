import sys
import os
import re
import requests
from urllib.parse import urlparse, parse_qs, unquote

from pystyle import Colorate, Colors


def clear():
    os.system('cls') if sys.platform.startswith('win') else os.system('clear')


def banner():
    print(f'''
\033[1;93m
 ██████╗ ███████╗████████╗    ██╗██████╗ 
██╔════╝ ██╔════╝╚══██╔══╝    ██║██╔══██╗
██║  ███╗█████╗     ██║       ██║██║  ██║
██║   ██║██╔══╝     ██║       ██║██║  ██║
╚██████╔╝███████╗   ██║       ██║██████╔╝
 ╚═════╝ ╚══════╝   ╚═╝       ╚═╝╚═════╝ 
\033[1;97m
────────────────────────────────────────────
➤ Facebook Post ID Extractor [PRO]
➤ Version: 2.0
➤ Hỗ trợ: share/p, reel, video, group, photo, permalink...
────────────────────────────────────────────
''')
    print(Colorate.Horizontal(
        Colors.white_to_black,
        "- - - - - - - - - - - - - - - - - - - - - - - - -"
    ))


# ══════════════════════════════════════════════════════════════
# TẦNG 1 — PARSE TĨNH (không cần HTTP, siêu nhanh)
# ══════════════════════════════════════════════════════════════

def extract_from_url(url: str) -> str | None:
    """
    Trích xuất Post ID trực tiếp từ cấu trúc URL (không cần HTTP).
    Bao gồm query string, path segment, và các pattern đặc biệt.
    """
    url = url.strip()

    try:
        parsed = urlparse(url)
        qs     = parse_qs(parsed.query)
        path   = parsed.path
    except Exception:
        return None

    # ── Query string params ───────────────────────────────────
    for key in ('story_fbid', 'fbid', 'id'):
        if key in qs and qs[key][0].isdigit():
            val = qs[key][0]
            if len(val) >= 10:           # ID hợp lệ tối thiểu 10 chữ số
                return val

    # ?v=ID (video embed)
    if 'v' in qs and qs['v'][0].isdigit() and len(qs['v'][0]) >= 10:
        return qs['v'][0]

    # ── Path segment patterns ─────────────────────────────────
    patterns = [
        r'/posts/(?:[^/]+/)?(\d{10,})',
        r'/videos/(?:[^/]+/)?(\d{10,})',
        r'/photos/(?:[^/]+/)?(\d{10,})',
        r'/photo/(?:[^/]+/)?(\d{10,})',
        r'/reel/(?:[^/]+/)?(\d{10,})',
        r'/reels/(?:[^/]+/)?(\d{10,})',
        r'/groups/[^/]+/posts/(?:[^/]+/)?(\d{10,})',
        r'/groups/[^/]+/permalink/(?:[^/]+/)?(\d{10,})',
        r'/permalink/(?:[^/]+/)?(\d{10,})',
        r'/story\.php.*story_fbid=(\d{10,})',
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)

    # ── Fallback: bất kỳ chuỗi số dài nào ở cuối path ────────
    m = re.search(r'/(\d{13,19})(?:/|$|\?)', path)
    if m:
        return m.group(1)

    return None


# ══════════════════════════════════════════════════════════════
# TẦNG 2 — RESOLVE QUA HTTP (follow redirect + parse HTML)
# ══════════════════════════════════════════════════════════════

# Headers giả lập trình duyệt — dùng cho mọi HTTP request
_HEADERS_DESKTOP = {
    'user-agent': 'Mozilla/5.0'
}

_HEADERS_MOBILE = {
    'user-agent': 'Mozilla/5.0 (Mobile)'
}


def parse_id_from_html(html: str) -> str | None:
    """
    Trích xuất Post ID từ nội dung HTML của Facebook.
    Thử nhiều pattern theo thứ tự ưu tiên.
    """

    # ── Pattern ưu tiên cao — embedded JSON / meta ────────────

    # "top_level_post_id":"1234567890"
    m = re.search(r'"top_level_post_id"\s*:\s*"(\d{10,})"', html)
    if m:
        return m.group(1)

    # "post_id":"1234567890"
    m = re.search(r'"post_id"\s*:\s*"(\d{10,})"', html)
    if m:
        return m.group(1)

    # story_fbid=1234567890 (trong URL nhúng)
    m = re.search(r'story_fbid[=:]"?(\d{10,})', html)
    if m:
        return m.group(1)

    # "story_fbid":"1234567890"
    m = re.search(r'"story_fbid"\s*:\s*"(\d{10,})"', html)
    if m:
        return m.group(1)

    # <meta property="og:url" content="https://.../{id}">
    m = re.search(r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        og_url = unquote(m.group(1))
        result = extract_from_url(og_url)
        if result:
            return result

    # "fbid":"1234567890"
    m = re.search(r'"fbid"\s*:\s*"(\d{10,})"', html)
    if m:
        return m.group(1)

    # /posts/1234567890 trong HTML nhúng
    m = re.search(r'/posts/(\d{10,})', html)
    if m:
        return m.group(1)

    # ── Pattern thấp hơn — fallback số dài tổng quát ─────────
    # Tìm số ID xuất hiện cạnh các từ khóa liên quan
    for keyword in ('post_id', 'story_id', 'object_id', 'entity_id'):
        m = re.search(rf'"{keyword}"\s*:\s*"?(\d{{13,19}})"?', html)
        if m:
            return m.group(1)

    return None


def resolve_via_http(url: str, cookie: str = None) -> tuple[str | None, str]:
    """
    Resolve URL qua HTTP request, follow redirect, parse HTML.
    Trả về (post_id, method_used).
    """
    headers = dict(_HEADERS_DESKTOP)
    if cookie:
        headers['cookie'] = cookie

    try:
        resp     = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        final    = resp.url

        # Bước 1: Thử parse URL sau redirect
        result = extract_from_url(final)
        if result:
            return result, 'redirect_url'

        # Bước 2: Parse HTML desktop
        result = parse_id_from_html(resp.text)
        if result:
            return result, 'html_desktop'

    except Exception:
        pass

    # Bước 3: Thử lại với mbasic (mobile HTML đơn giản hơn, dễ parse hơn)
    try:
        mbasic_url = url
        for domain in ('www.facebook.com', 'm.facebook.com', 'web.facebook.com'):
            mbasic_url = mbasic_url.replace(domain, 'mbasic.facebook.com')

        mob_headers = dict(_HEADERS_MOBILE)
        if cookie:
            mob_headers['cookie'] = cookie

        resp   = requests.get(mbasic_url, headers=mob_headers, timeout=15, allow_redirects=True)
        result = extract_from_url(resp.url) or parse_id_from_html(resp.text)
        if result:
            return result, 'mbasic'

    except Exception:
        pass

    return None, 'failed'


# ══════════════════════════════════════════════════════════════
# ENTRY POINT — Kết hợp 2 tầng
# ══════════════════════════════════════════════════════════════

def get_post_id(url: str, cookie: str = None) -> tuple[str | None, str]:
    """
    Trích xuất Post ID theo thứ tự:
      1. Parse tĩnh từ URL (không cần mạng)
      2. HTTP resolve (follow redirect + parse HTML)
    Trả về (post_id, method_used).
    """
    # Tầng 1 — nhanh, không cần mạng
    result = extract_from_url(url)
    if result:
        return result, 'static_parse'

    # Tầng 2 — HTTP resolve
    return resolve_via_http(url, cookie)


# ══════════════════════════════════════════════════════════════
# UI — In kết quả
# ══════════════════════════════════════════════════════════════

METHOD_LABEL = {
    'static_parse' : '\033[38;5;245m[regex]\033[0m',
    'redirect_url' : '\033[1;34m[redirect]\033[0m',
    'html_desktop' : '\033[1;35m[html]\033[0m',
    'mbasic'       : '\033[1;36m[mbasic]\033[0m',
    'failed'       : '\033[1;31m[failed]\033[0m',
}


def print_result(idx: int | None, url: str, post_id: str | None, method: str) -> None:
    prefix = f'\033[1;33m[{idx}]\033[0m ' if idx is not None else ''
    label  = METHOD_LABEL.get(method, '')
    short  = url[:72] + '...' if len(url) > 72 else url

    if post_id:
        print(f'{prefix}\033[1;32m✔\033[0m {label} Post ID: \033[1;93m{post_id}\033[0m')
        print(f'   \033[38;5;245m{short}\033[0m')
    else:
        print(f'{prefix}\033[1;31m✘\033[0m {label} Không lấy được ID')
        print(f'   \033[38;5;245m{short}\033[0m')


# ══════════════════════════════════════════════════════════════
# MODES
# ══════════════════════════════════════════════════════════════

def mode_single(cookie: str = None) -> None:
    """Nhập URL tay từng cái"""
    print('\n\033[1;96m[MODE 1] URL thủ công — gõ "exit" để thoát\033[0m\n')
    idx = 1
    while True:
        url = input('\033[1;31m[\033[1;37m] \033[1;37m=> \033[38;5;51mURL: \033[1;35m').strip()
        if not url:
            continue
        if url.lower() in ('exit', 'quit', 'q'):
            break

        print(f'   \033[38;5;245mĐang xử lý...\033[0m', end='\r')
        post_id, method = get_post_id(url, cookie)
        print(' ' * 30, end='\r')   # Xóa dòng "Đang xử lý"
        print_result(idx, url, post_id, method)
        print()
        idx += 1


def mode_file(cookie: str = None) -> None:
    """Đọc danh sách URL từ file, xuất Post ID"""
    filepath = input('\033[1;31m[\033[1;37m] \033[1;37m=> \033[38;5;51mFile chứa URL: \033[1;35m').strip()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            urls = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f'\033[1;31m[!] Không tìm thấy: {filepath}\033[0m')
        return

    print(f'\n\033[1;33m[*] {len(urls)} URL — đang xử lý...\033[0m\n')
    print('\033[1;31m' + '─' * 64 + '\033[0m')

    results, fails = [], []
    for idx, url in enumerate(urls, 1):
        post_id, method = get_post_id(url, cookie)
        print_result(idx, url, post_id, method)
        print()
        if post_id:
            results.append(post_id)
        else:
            fails.append(url)

    print('\033[1;31m' + '─' * 64 + '\033[0m')
    print(f'\033[1;32m✔ Thành công: {len(results)}\033[0m  \033[1;31m✘ Thất bại: {len(fails)}\033[0m')

    if results:
        save = input('\n\033[38;5;51mLưu Post IDs ra file? (y/n): \033[0m').strip().lower()
        if save == 'y':
            out = 'post_ids.txt'
            with open(out, 'w', encoding='utf-8') as f:
                f.write('\n'.join(results))
            print(f'\033[1;32m✔ Đã lưu {len(results)} ID → \033[1;93m{out}\033[0m')


def ask_cookie() -> str | None:
    """Hỏi có muốn dùng cookie không (để resolve link login-required)"""
    use = input('\033[38;5;51mDùng cookie để resolve? (y/n): \033[0m').strip().lower()
    if use != 'y':
        return None
    cookie_file = input('\033[38;5;51mTên file cookie: \033[0m').strip()
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            return f.read().splitlines()[0].strip()
    except Exception:
        print('\033[1;33m[!] Không đọc được cookie, tiếp tục không có cookie.\033[0m')
        return None


def main() -> None:
    clear()
    banner()

    print('\033[1;97m Chọn chế độ:\033[0m')
    print('  \033[1;96m[1]\033[0m Nhập URL thủ công')
    print('  \033[1;96m[2]\033[0m Batch từ file')
    print()

    choice = input('\033[1;31m[\033[1;37m] \033[1;37m=> \033[38;5;51mChọn (1/2): \033[1;35m').strip()
    print()

    cookie = ask_cookie()
    print()

    if choice == '1':
        mode_single(cookie)
    elif choice == '2':
        mode_file(cookie)
    else:
        print('\033[1;31m[!] Không hợp lệ.\033[0m')


# ── Entry point ─────────────────────────────────────────────
if __name__ == '__main__':
    while True:
        try:
            main()
            again = input('\n\033[38;5;245mChạy lại? (y/n): \033[0m').strip().lower()
            if again != 'y':
                break
        except KeyboardInterrupt:
            print('\n\033[38;5;245m[!] Thoát.\033[0m')
            sys.exit(0)

