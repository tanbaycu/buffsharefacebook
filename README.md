<div align="center">

<!-- ASCII Banner -->
```
███████╗██╗  ██╗ █████╗ ██████╗ ███████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝
███████╗███████║███████║██████╔╝█████╗  
╚════██║██╔══██║██╔══██║██╔══██╗██╔══╝  
███████║██║  ██║██║  ██║██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
```

# 🚀 Facebook Auto Share — PRO Edition

**A fast, multi-account Facebook post automation tool built with Python.**  
*No browser needed. Cookie-based. Runs anywhere.*

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)]()
[![License](https://img.shields.io/badge/License-Personal%20Use-orange?style=flat-square)]()
[![Version](https://img.shields.io/badge/Version-2.0-green?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

---

**🌐 Language / Ngôn ngữ:**  
🇺🇸 **English** (current) &nbsp;|&nbsp; [🇻🇳 Tiếng Việt → README_vi.md](./README_vi.md)

</div>

---

## 📌 What is This?

**Facebook Auto Share PRO** is a command-line automation tool that leverages Facebook session cookies to programmatically share any public post to multiple accounts — fast, silently, and without touching a browser.

Originally built for personal growth hacking and social media campaigns, this tool is designed to be:

- 🧩 **Modular** — swap cookie files freely
- ⚡ **Fast** — threaded per-account share requests
- 🔐 **Cookie-safe** — no password required, no login flow
- 🖥️ **Terminal-native** — clean CLI with color output

> ⚠️ **Disclaimer:** This tool is for **educational and personal use only**. Usage violating Facebook's Terms of Service is solely the user's responsibility.

---

## ✨ Feature Highlights

| Feature | Description |
|---|---|
| 🍪 Cookie-based auth | No username/password required — uses session tokens |
| 👥 Multi-account | Load unlimited accounts from a single `.txt` file |
| 🔁 Custom share count | Set exact number of shares before auto-stopping |
| ⏱️ Adjustable delay | Fine-tune delays between shares to avoid rate limits |
| 🧵 Threaded execution | Each share runs in its own thread for speed |
| 📊 Live status output | Real-time share count and status in terminal |
| 🎨 Stylized CLI | ASCII banner + colored output via `pystyle` |
| 🔄 Repeat mode | Tool loops until manually exited (`Ctrl+C`) |

---

## 🗂️ Project Structure

```
buffsharefacebook/
│
├── main.py            # Core auto share automation script
├── requirements.txt   # Python dependencies
├── cookies.txt        # Your session cookies (DO NOT COMMIT)
│
├── README.md          # English documentation (this file)
└── README_vi.md       # Vietnamese documentation
```

---

## ⚙️ System Requirements

Before getting started, make sure you have:

- **Python** `>= 3.7` — [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)
- Stable Internet connection
- At least **one valid Facebook session cookie**

### Required Libraries

```
requests   — HTTP client for API calls
pystyle    — Terminal color & styling utilities
```

---

## 🛠️ Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/tanbaycu/buffsharefacebook.git
cd buffsharefacebook
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests pystyle
```

---

## 🍪 Obtaining Facebook Cookies

Your cookies file is the **heart** of this tool. Here's how to get valid session cookies:

### 💻 On Desktop (Browser Extension)

1. Open **Chrome** or **Firefox**
2. Search for and install the **"Get cookies.txt"** or **"EditThisCookie"** extension
3. Log in to your **Facebook secondary/clone account** *(never use your main account)*
4. Click the extension → **Export cookies** → Copy the `c_user`, `xs`, `datr` fields
5. Paste the full cookie string into your `cookies.txt`

### 📱 On Mobile (Android)

1. Download **MonokaiToolkit Pro** from your app store
2. Log in with your **Facebook clone account**
3. Navigate to **Cookies** section and copy the session string

### 📄 cookies.txt Format

Each line = one account's cookie string:

```txt
c_user=100012xxx;xs=abc123;datr=xxxx;sb=yyyy;fr=zzz... (Account 1)
c_user=100098xxx;xs=def456;datr=aaaa;sb=bbbb;fr=ccc... (Account 2)
c_user=100076xxx;xs=ghi789;datr=cccc;sb=dddd;fr=eee... (Account 3)
```

> ⚠️ **No blank lines** at the end of the file — they'll cause empty token slots.

---

## 🔍 Finding the Post ID

The automation scripts require a **Post ID** (the numeric identifier of the Facebook post).
Modern Facebook URLs are highly obfuscated (e.g., `share/p/...` or `pfbid...`), making it difficult to find the ID manually.

**Use the Official Extractor:**  
Visit **[Facebook Post ID Extractor](https://get-post-id.vercel.app/)** → Paste your link → Get the raw numeric ID instantly.

---

## ▶️ Running the Auto Share Tool

```bash
python main.py
```

You'll be prompted through a 4-step interactive setup:

```
[+] => Enter cookies file name:       cookies.txt
[+] => Enter Post ID to Share:        1234567890123456
[+] => Enter Share Delay (seconds):   5
[+] => How many shares before stop:   50
```

---

## 🔬 How It Works (Technical Deep-Dive)

Understanding the internals helps you use the tool effectively and troubleshoot issues:

### 1. Token Extraction (`get_token`)

```python
# The tool hits Facebook's Business Manager API to extract a short-lived EAAG token
# This token is embedded in the page's raw HTML — no official API key needed
requests.get('https://business.facebook.com/content_management', headers=header_)
token = response.text.split('EAAG')[1].split('","')[0]
```

The extracted token format: `EAAG{token_string}` — a Graph API access token tied to the session cookie.

### 2. Share Execution (`share`)

```python
# Posts to Facebook's Graph API endpoint using the extracted token
requests.post(
    f'https://graph.facebook.com/me/feed'
    f'?link=https://m.facebook.com/{id_share}'
    f'&published=0'          ← shares as hidden post (no timeline spam)
    f'&access_token={token}'
)
```

`published=0` means the share is submitted but **not published to timeline** — just counted as a share internally.

### 3. Threading Model

Each cookie-token pair spawns its own thread:
```
Account 1 ──→ Thread 1 ──→ share()
Account 2 ──→ Thread 2 ──→ share()
Account N ──→ Thread N ──→ share()
```

All threads run near-simultaneously, then `time.sleep(delay)` is applied per cycle.

---

## 🧩 Parameter Reference

| Parameter | Type | Recommended Value | Notes |
|---|---|---|---|
| `cookies file` | string | `cookies.txt` | Path relative to `main.py` |
| `Post ID` | integer | `1234567890` | Numeric post/video ID only |
| `Delay (sec)` | float | `3–10` | Lower = faster but riskier |
| `Share limit` | integer | `20–100` | Tool stops when reached |

---

## 🔒 Security Best Practices

```
✅ DO                                  ❌ DON'T
──────────────────────────────────     ──────────────────────────────────
Use secondary/clone accounts           Use your main Facebook account
Keep cookies.txt private               Commit cookies.txt to GitHub
Set delays of 3–10 seconds             Set delay to 0 or 1 second
Monitor for checkpoint prompts         Ignore login alerts from Facebook
Refresh cookies if they expire         Reuse expired cookies
```

> 🔑 **Cookie Lifetime:** Facebook session cookies typically expire after **logout**, **password change**, or **long inactivity**. Refresh them regularly.

> 🛡️ **Add to `.gitignore`:**
> ```
> cookies.txt
> *.txt
> ```

---

## 🔧 Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `0 live accounts detected` | All cookies expired or malformed | Re-extract cookies from browser |
| No shares being counted | Post ID is wrong or post is private | Verify the ID via traodoisub.com |
| Tool exits immediately | `cookies.txt` file not found | Check the filename is exact |
| Checkpoint triggered | Shares too fast, account flagged | Increase delay to 10–15 seconds |
| Module not found error | Dependencies not installed | Run `pip install -r requirements.txt` |

---

## 📈 Tips to Maximize Effectiveness

- **Rotate accounts:** Use 5–10+ clone accounts for higher share counts
- **Stagger delays:** Use `5–8` seconds to blend in with human behavior  
- **Target public posts:** Private posts cannot be shared via this method
- **Monitor token validity:** Re-run to refresh tokens if mid-session breaks occur
- **Run off-peak hours:** Facebook's rate limits are softer during low-traffic periods

---

## 🤝 Support & Contact

Found a bug? Have questions? Want to collaborate?

<div align="center">

[![Linktree](https://img.shields.io/badge/🔗%20All%20My%20Links-Linktree-39e09b?style=for-the-badge&logo=linktree)](https://linktr.ee/tanbaycu)

</div>

---

## 📄 License

This project is open-source and intended for **personal and educational use only**.

- ❌ Do not redistribute for commercial purposes
- ❌ Do not use for spam, harassment, or fraud
- ✅ Feel free to fork, learn, and modify for personal use

---

<div align="center">

**Made with ❤️ by [tanbaycu](https://linktr.ee/tanbaycu)**

*If this helped you, drop a ⭐ on the repo!*

---

🇺🇸 English (current) &nbsp;|&nbsp; [🇻🇳 Tiếng Việt](./README_vi.md)

</div>
