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

**Công cụ tự động share bài viết Facebook đa tài khoản, xây dựng bằng Python.**  
*Không cần trình duyệt. Cookie-based. Chạy được ở mọi nơi.*

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Nền%20tảng-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)]()
[![License](https://img.shields.io/badge/Giấy%20phép-Cá%20nhân-orange?style=flat-square)]()
[![Version](https://img.shields.io/badge/Phiên%20bản-2.0-green?style=flat-square)]()
[![Status](https://img.shields.io/badge/Trạng%20thái-Hoạt%20động-brightgreen?style=flat-square)]()

---

**🌐 Ngôn ngữ / Language:**  
🇻🇳 **Tiếng Việt** (hiện tại) &nbsp;|&nbsp; [🇺🇸 English → README.md](./README.md)

</div>

---

## 📌 Giới thiệu

**Facebook Auto Share PRO** là công cụ tự động hóa dòng lệnh, sử dụng cookie phiên đăng nhập Facebook để share bài viết lên nhiều tài khoản — nhanh chóng, âm thầm, không cần mở trình duyệt.

Được tạo ra phục vụ nhu cầu tăng trưởng cá nhân và các chiến dịch mạng xã hội, công cụ này được thiết kế để:

- 🧩 **Linh hoạt** — đổi file cookie dễ dàng bất cứ lúc nào
- ⚡ **Nhanh** — share song song nhiều tài khoản qua threading
- 🔐 **Bảo mật cookie** — không cần mật khẩu, không qua bước đăng nhập
- 🖥️ **Terminal-native** — giao diện CLI gọn gàng với màu sắc

> ⚠️ **Tuyên bố miễn trừ trách nhiệm:** Công cụ này chỉ dành cho **mục đích giáo dục và cá nhân**. Mọi hành vi vi phạm Điều khoản sử dụng của Facebook là hoàn toàn thuộc trách nhiệm người dùng.

---

## ✨ Tính năng nổi bật

| Tính năng | Mô tả |
|---|---|
| 🍪 Xác thực qua Cookie | Không cần tài khoản/mật khẩu — dùng session token |
| 👥 Đa tài khoản | Nạp không giới hạn account từ một file `.txt` duy nhất |
| 🔁 Giới hạn share tùy chỉnh | Đặt số share chính xác trước khi tự động dừng |
| ⏱️ Delay điều chỉnh được | Tinh chỉnh thời gian chờ giữa các lần để tránh bị chặn |
| 🧵 Thực thi đa luồng (Thread) | Mỗi share chạy trên thread riêng để tối đa tốc độ |
| 📊 Trạng thái trực tiếp | Đếm share real-time ngay trên terminal |
| 🎨 CLI được làm đẹp | ASCII banner + màu sắc qua thư viện `pystyle` |
| 🔄 Chế độ lặp | Tool tiếp tục chạy cho đến khi bấm `Ctrl+C` |

---

## 🗂️ Cấu trúc dự án

```
buffsharefacebook/
│
├── main.py            # Script tự động hóa share bài chính
├── requirements.txt   # Các thư viện Python cần thiết
├── cookies.txt        # Cookie phiên đăng nhập của bạn (ĐỪNG COMMIT)
│
├── README.md          # Tài liệu tiếng Anh
└── README_vi.md       # Tài liệu tiếng Việt (file này)
```

---

## ⚙️ Yêu cầu hệ thống

Trước khi bắt đầu, hãy đảm bảo bạn có:

- **Python** `>= 3.7` — [Tải tại đây](https://www.python.org/downloads/)
- **pip** (đi kèm với Python)
- Kết nối Internet ổn định
- Ít nhất **một cookie phiên Facebook hợp lệ**

### Thư viện cần thiết

```
requests   — HTTP client để gọi API
pystyle    — Tiện ích màu sắc và định dạng Terminal
```

---

## 🛠️ Hướng dẫn cài đặt

### Bước 1 — Tải mã nguồn về máy

```bash
git clone https://github.com/tanbaycu/buffsharefacebook.git
cd buffsharefacebook
```

### Bước 2 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install requests pystyle
```

---

## 🍪 Cách lấy Cookie Facebook

File cookies là **trái tim** của công cụ này. Dưới đây là cách lấy cookie phiên hợp lệ:

### 💻 Trên máy tính (Tiện ích mở rộng trình duyệt)

1. Mở **Chrome** hoặc **Firefox**
2. Tìm và cài extension **"Get cookies.txt"** hoặc **"EditThisCookie"**
3. Đăng nhập vào tài khoản Facebook **phụ / clone** *(tuyệt đối không dùng tài khoản chính)*
4. Nhấn vào extension → **Export cookies** → Sao chép các trường `c_user`, `xs`, `datr`
5. Dán toàn bộ chuỗi cookie vào file `cookies.txt`

> 💡 Hoặc tìm **"Get Token Cookie"** trên thanh tìm kiếm trình duyệt và làm theo hướng dẫn.

### 📱 Trên điện thoại (Android)

1. Tải ứng dụng **MonokaiToolkit Pro** từ cửa hàng ứng dụng
2. Đăng nhập vào tài khoản Facebook **clone**
3. Tìm phần **Cookies** và sao chép chuỗi phiên

### 📄 Định dạng file cookies.txt

Mỗi dòng = cookie của một tài khoản:

```txt
c_user=100012xxx;xs=abc123;datr=xxxx;sb=yyyy;fr=zzz... (Tài khoản 1)
c_user=100098xxx;xs=def456;datr=aaaa;sb=bbbb;fr=ccc... (Tài khoản 2)
c_user=100076xxx;xs=ghi789;datr=cccc;sb=dddd;fr=eee... (Tài khoản 3)
```

> ⚠️ **Không để dòng trống** ở cuối file — sẽ tạo ra slot token rỗng gây lỗi.

---

## 🔍 Cách tìm Post ID

Tool tự động yêu cầu đầu vào là **Post ID** (dãy số định danh thật của bài viết).
Bởi vì các đường link Facebook hiện nay thường bị viết tắt ẩn giấu ID (ví dụ: `share/p/...` hoặc mã `pfbid...`), việc tìm ID thủ công là rất khó khăn.

**Sử dụng Công cụ Trích xuất Chính thức:**  
Truy cập **[Facebook Post ID Extractor](https://get-post-id.vercel.app/)** → Dán link bài viết vào → Nhận ngay dãy số ID chuẩn xác.

---

## ▶️ Hướng dẫn chạy Auto Share

```bash
python main.py
```

Tool sẽ hỏi bạn qua 4 bước thiết lập:

```
[+] => Nhập tên file cookies:              cookies.txt
[+] => Nhập ID bài viết cần share:         1234567890123456
[+] => Nhập delay giữa các lần share (giây): 5
[+] => Bao nhiêu share thì dừng:           50
```

---

## 🔬 Cơ chế hoạt động (Deep-Dive kỹ thuật)

Hiểu nguyên lý bên trong giúp bạn dùng hiệu quả hơn và tự debug khi có lỗi:

### 1. Trích xuất Token (`get_token`)

```python
# Tool gọi đến API Facebook Business Manager để lấy token ngắn hạn EAAG
# Token này được nhúng trong HTML thô của trang — không cần API key chính thức
requests.get('https://business.facebook.com/content_management', headers=header_)
token = response.text.split('EAAG')[1].split('","')[0]
```

Định dạng token trích xuất: `EAAG{chuỗi_token}` — là Graph API access token gắn với cookie phiên.

### 2. Thực thi Share (`share`)

```python
# Gửi request POST đến Graph API của Facebook dùng token đã trích xuất
requests.post(
    f'https://graph.facebook.com/me/feed'
    f'?link=https://m.facebook.com/{id_share}'
    f'&published=0'          ← share ẩn, không hiện lên tường
    f'&access_token={token}'
)
```

`published=0` nghĩa là bài share được gửi đi nhưng **không công khai trên tường** — chỉ tính vào lượt share nội bộ.

### 3. Mô hình Threading

Mỗi cặp cookie-token tạo ra một thread riêng:
```
Tài khoản 1 ──→ Thread 1 ──→ share()
Tài khoản 2 ──→ Thread 2 ──→ share()
Tài khoản N ──→ Thread N ──→ share()
```

Tất cả thread chạy gần như đồng thời, sau đó `time.sleep(delay)` được áp dụng sau mỗi chu kỳ.

---

## 🧩 Giải thích tham số chi tiết

| Tham số | Kiểu | Giá trị khuyến nghị | Ghi chú |
|---|---|---|---|
| `Tên file cookies` | string | `cookies.txt` | Đường dẫn tương đối từ `main.py` |
| `Post ID` | số nguyên | `1234567890` | Chỉ số ID, không phải URL |
| `Delay (giây)` | số thực | `3–10` | Thấp hơn = nhanh hơn nhưng rủi ro hơn |
| `Giới hạn share` | số nguyên | `20–100` | Tool dừng khi đạt ngưỡng này |

---

## 🔒 Quy tắc bảo mật quan trọng

```
✅ NÊN LÀM                              ❌ KHÔNG NÊN LÀM
─────────────────────────────────       ─────────────────────────────────────
Dùng tài khoản phụ / clone              Dùng Facebook tài khoản chính
Giữ bí mật file cookies.txt             Đẩy cookies.txt lên GitHub
Đặt delay 3–10 giây                     Để delay bằng 0 hoặc 1 giây
Theo dõi cảnh báo checkpoint            Bỏ qua thông báo đăng nhập
Làm mới cookie khi hết hạn              Dùng lại cookie đã expired
```

> 🔑 **Thời hạn Cookie:** Cookie phiên Facebook thường hết hạn sau khi **đăng xuất**, **đổi mật khẩu**, hoặc **không hoạt động lâu**. Hãy làm mới thường xuyên.

> 🛡️ **Thêm vào `.gitignore` để bảo vệ:**
> ```
> cookies.txt
> *.txt
> ```

---

## 🔧 Xử lý sự cố thường gặp

| Vấn đề | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `0 tài khoản live` | Tất cả cookie đã hết hạn hoặc sai format | Lấy lại cookie từ trình duyệt |
| Không có share nào | Post ID sai hoặc bài viết bị private | Kiểm tra ID qua traodoisub.com |
| Tool thoát ngay | File `cookies.txt` không tìm thấy | Kiểm tra tên file chính xác |
| Tài khoản bị checkpoint | Share quá nhanh, bị phát hiện tự động | Tăng delay lên 10–15 giây |
| Lỗi module không tìm thấy | Chưa cài thư viện | Chạy `pip install -r requirements.txt` |

---

## 📈 Mẹo tối đa hóa hiệu quả

- **Xoay vòng tài khoản:** Dùng 5–10+ tài khoản clone để tăng tổng số share
- **Delay thông minh:** Dùng `5–8` giây để giả lập hành vi người thật
- **Chỉ nhắm bài công khai:** Bài riêng tư không thể share qua phương pháp này
- **Theo dõi token:** Chạy lại tool để làm mới token nếu giữa chừng bị đứt
- **Chạy ngoài giờ cao điểm:** Rate limit của Facebook nhẹ hơn vào giờ thấp điểm

---

## 🤝 Hỗ trợ & Liên hệ

Tìm thấy lỗi? Có câu hỏi? Muốn hợp tác?

<div align="center">

[![Linktree](https://img.shields.io/badge/🔗%20Tất%20cả%20liên%20kết-Linktree-39e09b?style=for-the-badge&logo=linktree)](https://linktr.ee/tanbaycu)

</div>

---

## 📄 Giấy phép

Dự án này là mã nguồn mở và chỉ dành cho **mục đích cá nhân và học tập**.

- ❌ Không phân phối lại để kiếm lợi nhuận thương mại
- ❌ Không dùng cho spam, quấy rối, hoặc gian lận
- ✅ Thoải mái fork, học hỏi và chỉnh sửa cho mục đích cá nhân

---

<div align="center">

**Được tạo với ❤️ bởi [tanbaycu](https://linktr.ee/tanbaycu)**

*Nếu tool giúp ích cho bạn, hãy để lại ⭐ trên repo nhé!*

---

🇻🇳 Tiếng Việt (hiện tại) &nbsp;|&nbsp; [🇺🇸 English](./README.md)

</div>
