# VAULT Core

VAULT hỗ trợ hồ sơ doanh nghiệp, chia sẻ dữ liệu có kiểm soát và thẩm định công nghệ giữa doanh nghiệp Việt Nam và nhà đầu tư Nhật Bản.

**Hiện tại: hai phần MVP đã chạy được — Hồ sơ doanh nghiệp/Trust Profile và Phòng dữ liệu theo thương vụ.** Hồ sơ lưu trong PostgreSQL; tài liệu lưu cục bộ theo lựa chọn của bạn. Có tạo/sửa/danh sách/ba lớp xem trước, sáu nhóm thư mục, upload, xem trước và lịch sử phiên bản. Đây là bản thử nội bộ dùng dữ liệu giả lập, chưa có đăng nhập hoặc chia sẻ cho buyer.

## Chạy trên Windows

Mở PowerShell tại thư mục `vault-core` (thư mục chứa README này). Máy hiện tại đã có `.venv`, thư viện, `.env` và PostgreSQL Docker. Nếu đang chạy phiên bản backend cũ, nhấn Ctrl+C trong cửa sổ đó rồi chạy lại theo bước 2.

### 1. Chuẩn bị lần đầu hoặc cài lại thư viện

Môi trường đã kiểm tra: Windows, Python **3.12.14**, Node.js **22.17.0**, npm **10.9.2**. Dùng Node.js 22.12 trở lên; bộ dependency Python đã được xác minh với Python 3.12.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

Script tạo `.venv` nếu chưa có, cài dependency theo lockfile, cài frontend bằng `npm ci`, và chỉ sao chép `.env.example` sang `.env` khi file đích chưa tồn tại. Script ưu tiên Python trên PATH rồi thử Python trong cache Codex đã tìm thấy trên máy này. Nếu cần chọn Python ở vị trí khác, truyền đường dẫn thực của `python.exe` qua tham số `-PythonExecutable`.

Lệnh trên chỉ đặt execution policy cho tiến trình PowerShell chạy script; không đổi chính sách toàn máy. Không cần kích hoạt môi trường ảo hay chạy `Activate.ps1`. Script không cài PostgreSQL và không tự tải trình duyệt kiểm thử.

### 2. Chuẩn bị PostgreSQL và khởi động backend — cửa sổ thứ nhất

Chạy từ thư mục gốc `vault-core`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-database.ps1
.\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini upgrade head
$env:INTERNAL_PREVIEW_ENABLED = "true"
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Mở Docker Desktop trước khi chạy. Script dùng PostgreSQL 17.9 ở cổng riêng `127.0.0.1:55432`, tạo database `vault` và `vault_test`, rồi chờ database sẵn sàng. Mật khẩu ngẫu nhiên chỉ lưu trong các file bị Git bỏ qua: `.tmp/database.json`, `.tmp/database.env` và URL trong `.env`. Script chỉ điền `DATABASE_URL` nếu giá trị đang trống; không thay URL bạn đã cấu hình. Nếu bạn dùng database riêng, migration ở trên áp dụng cho URL đó.

Lệnh Alembic tạo/cập nhật cấu trúc bảng, không xóa hồ sơ. Chạy lại khi có migration mới. Docker dùng volume lưu dữ liệu qua lần khởi động lại; giữ các file cấu hình `.tmp/database.*` cùng volume để tránh mất mật khẩu truy cập. Không dùng lệnh xóa volume để khởi động lại.

`INTERNAL_PREVIEW_ENABLED=true` bật các trang thử nội bộ trong tiến trình này. Mặc định tắt; đây không phải cơ chế đăng nhập. Giữ backend và frontend ở địa chỉ `127.0.0.1`, chỉ nhập dữ liệu giả lập. Giữ cửa sổ này mở.

- API kiểm tra: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- Swagger/API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI chạy thực tế: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 3. Khởi động frontend — cửa sổ PowerShell thứ hai

Cũng chạy từ thư mục gốc:

```powershell
npm.cmd --prefix frontend run dev
```

Mở [http://127.0.0.1:5173](http://127.0.0.1:5173). Trang mặc định là **Hồ sơ doanh nghiệp**. Liên kết **Kết nối API** mở trang health check cũ tại `/#/health`.

Vite chuyển các yêu cầu `/api` sang backend cổng 8000. Nhấn **Ctrl+C** ở mỗi cửa sổ để dừng server. Hai server không tự mở trình duyệt. Test tự động dùng cổng khác, nên không cần dừng các server này để chạy test.

### Thử tính năng hồ sơ bằng tay

1. Chọn **Tạo hồ sơ**, nhập tên doanh nghiệp giả lập. Các mục còn thiếu có thể để trống; chỉ tên là bắt buộc để lưu nháp.
2. Nhập ngành, vùng, địa chỉ, nhân sự và tài chính. Doanh thu/EBITDA nhập theo VND, tối đa hai chữ số thập phân; EBITDA có thể âm. Ba năm gợi ý có thể sửa hoặc bỏ.
3. Mở **Nguồn & xác minh** dưới một dữ kiện. Khi chọn **Đã đối chiếu** hoặc **Bên thứ ba xác nhận**, phải nhập nguồn, ngày nguồn, người và ngày đối chiếu. Đây là ghi nhận thủ công, chưa xác thực người ký/đối chiếu. Dữ kiện mâu thuẫn/hết hạn giữ nhãn tự khai.
4. Chọn **Lưu hồ sơ**. Sau thông báo **Đã lưu hồ sơ**, tải lại trang để kiểm tra dữ liệu còn nguyên; chọn **Sửa hồ sơ** để cập nhật. Khi thay giá trị đã đối chiếu, nhãn tự trở về tự khai; lưu thay đổi trước khi đối chiếu lại.
5. Thử **Lớp 1 · Ẩn danh**: chỉ còn mã ngẫu nhiên, ngành/vùng và các dải số. Tên, địa chỉ, ghi chú và tiền chính xác không xuất hiện. **Lớp 2 · Định danh** có thông tin doanh nghiệp; **Lớp 3 · Hạn chế** có thông tin cổ đông/người quyết định/phạm vi sử dụng.
6. Mở cùng hồ sơ ở hai tab, sửa/lưu tab thứ nhất rồi thử lưu tab thứ hai: API báo xung đột, yêu cầu tải lại để tránh ghi đè. Dữ liệu thiếu không được tự thay bằng số 0.

Ba lớp hiện là **xem trước nội bộ**, chưa phải phân quyền. Hồ sơ chưa được phép chia sẻ bên ngoài chỉ nhờ chọn một tab. Trong lớp 3, liên kết **Mở phòng dữ liệu theo thương vụ** dẫn đến các phòng của doanh nghiệp.

### Thử phòng dữ liệu bằng tay

1. Chọn **Phòng dữ liệu → Thêm phòng dữ liệu**. Tìm/chọn doanh nghiệp, đặt tên thương vụ rồi bấm **Tạo phòng dữ liệu**.
2. Phòng có sáu nhóm: pháp lý/doanh nghiệp; tài chính/thuế; kinh doanh/vận hành; công nghệ/IP; nhân sự; Q&A. Chọn nhóm để lọc tài liệu.
3. Chọn **Thêm tài liệu**, nhập tên, chọn nhóm và file, rồi **Tải lên**. Mặc định tối đa 10 MiB/file; nhận PDF, PNG, JPG/JPEG, TXT UTF-8, DOCX và XLSX. File sai định dạng/quá lớn bị từ chối; form giữ nội dung để bạn sửa.
4. Mở tài liệu để xem trước. PDF có nút chuyển trang và phần văn bản; ảnh và TXT xem trực tiếp. DOCX/XLSX có liên kết tải xuống để mở bằng ứng dụng trên máy. PDF có mật khẩu hoặc trên 500 trang, ảnh trên 20 triệu điểm ảnh không được nhận ở MVP này.
5. Bấm **Thêm phiên bản**, chọn file mới và ghi chú. Sau khi lưu, chọn **Phiên bản 1** rồi **Phiên bản 2** để kiểm tra nội dung khác nhau. Tải lại trang: cả hai phiên bản vẫn còn; file cũ không bị ghi đè.
6. Bạn có thể tạo tài liệu giả lập để thử bằng lệnh sau; các file nằm trong `.tmp/fixtures/` và không được đưa vào Git:

```powershell
.\.venv\Scripts\python.exe -m backend.preview_fixtures
```

Dùng `sample-v1.png`, `sample-v2.png` và `sample.pdf` (hai trang). Không cần sửa các file mẫu cũ trong `sample_data/`.

File thực của bản thử nằm trong `.data/uploads/`, có tên do hệ thống tạo; PostgreSQL giữ tên gốc, nhóm, phiên bản, thời gian và SHA-256. Không tự sửa/xóa file trong thư mục này: ứng dụng sẽ báo lỗi khi nội dung mất hoặc không khớp. Khi sao lưu sau này cần giữ cả database và thư mục file. Chưa có antivirus, khôi phục sự cố tự động, MFA, watermark, NDA hay quyền buyer.

### 4. Kiểm tra nhanh bằng PowerShell

Khi backend đang chạy:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
```

Kết quả mặc định:

```json
{
  "status": "ok",
  "service": "VAULT Core",
  "version": "0.1.0",
  "scope": "liveness"
}
```

`liveness` chỉ có nghĩa API đang trả lời. Nó **không** xác nhận PostgreSQL, đăng nhập hay dịch vụ bên ngoài hoạt động.

## Biến môi trường

Chỉnh file `.env` ở thư mục gốc rồi khởi động lại cả hai server. [Mẫu .env.example](.env.example) không chứa thông tin bí mật; script setup không ghi đè file `.env` đã có.

| Biến | Công dụng |
| --- | --- |
| `PROJECT_NAME`, `VERSION` | Tên/phiên bản backend hiển thị trên trang |
| `API_V1_STR` | Tiền tố API, mặc định `/api/v1`; giữ mặc định cho bước này |
| `VITE_API_BASE_URL` | Đường dẫn API phía trình duyệt, mặc định `/api/v1` |
| `BACKEND_PROXY_TARGET` | Địa chỉ backend để Vite chuyển tiếp, mặc định `http://127.0.0.1:8000` |
| `DATABASE_URL` | URL PostgreSQL của backend; script database điền khi còn trống. Health check vẫn chạy khi không có DB |
| `INTERNAL_PREVIEW_ENABLED` | Mặc định false; bật true cho bản thử hồ sơ/phòng dữ liệu cục bộ |
| `UPLOAD_DIRECTORY` | Thư mục file backend, mặc định `.data/uploads`; đường dẫn tương đối tính từ gốc repo |
| `MAX_UPLOAD_BYTES` | Dung lượng tối đa mỗi file, mặc định 10485760 (10 MiB) |
| `ENVIRONMENT` | Nhãn môi trường, không phải công tắc bảo mật |

Backend đọc root `.env` bằng Pydantic Settings; biến môi trường của tiến trình có ưu tiên cao hơn file. Giá trị có tiền tố `VITE_` là **công khai trong trình duyệt**, không dùng để chứa mật khẩu/token. Các dòng secret/DRM/webhook cũ ở cuối mẫu chỉ được giữ để tham khảo tương thích với demo cũ, không được backend mới sử dụng.

## Kiểm tra tự động

Từ thư mục gốc:

```powershell
.\.venv\Scripts\python.exe -m backend.testing
.\.venv\Scripts\python.exe -m pytest tests backend/tests -q
.\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini check
.\.venv\Scripts\python.exe -m backend.export_openapi --check
npm.cmd --prefix frontend run api:check
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run format:check
```

PostgreSQL cần đang chạy. `backend.testing` áp dụng migration riêng cho `vault_test`. Test Python cũng chuẩn bị migration này, rồi rollback dữ liệu của từng test. Không dùng database thương vụ cho test. Có thể cung cấp `TEST_DATABASE_URL` trỏ tới database riêng có tên `vault_test`; mặc định đọc cấu hình cục bộ trong `.tmp/database.json`.

Kiểm tra bằng trình duyệt thật (cần cổng **18000/15173** trống):

```powershell
npm.cmd --prefix frontend run browser:install
npm.cmd --prefix frontend run test:e2e
```

Lệnh đầu tải Chromium vào `.tmp/playwright`, chỉ cần lần đầu hoặc khi nâng cấp Playwright. Lệnh sau tự chuẩn bị migration cho `vault_test`, tạo file giả lập, chạy backend/frontend riêng, kiểm tra health/hồ sơ/phòng dữ liệu rồi dừng server. Browser test ghi dữ liệu vào `vault_test` và file vào `.tmp/e2e-uploads`, không dùng `vault` hoặc `.data/uploads`. Ảnh desktop/mobile/PDF nằm trong `frontend/test-results/`.

Kết quả đã xác minh: **36 kiểm tra Python đạt**, **8 kiểm tra giao diện đạt**, **3 kiểm tra Chromium đạt**; migration ở head `0002`, build/lint và hợp đồng được kiểm tra. Chi tiết và giới hạn nằm trong STATE. Còn 14 cảnh báo deprecation từ demo/thư viện và cảnh báo màu của Playwright. Browser test chạy ngoài Codex sandbox và thoát bình thường; không cần mở PowerShell quản trị cho các lệnh dự án thông thường.

## API contract và cấu trúc

Backend là nguồn định nghĩa hợp đồng; frontend dùng types sinh tự động từ cùng OpenAPI:

```text
backend/app/schemas + backend/app/api
  → contracts/openapi.json
  → frontend/src/api/generated/schema.d.ts
```

Sau khi thay đổi API:

```powershell
.\.venv\Scripts\python.exe -m backend.export_openapi
npm.cmd --prefix frontend run api:generate
```

Không sửa trực tiếp file types được sinh tự động. Kiểm tra `--check` / `api:check` phát hiện file chưa được cập nhật.

| Đường dẫn | Vai trò |
| --- | --- |
| `backend/app/` | API hồ sơ/phòng dữ liệu, validation, projection, file store và SQLAlchemy |
| `backend/migrations/` | Revision 0001 cho companies và 0002 cho rooms/documents/document_versions |
| `backend/requirements.lock.txt` | Dependency đã xác minh trên Windows/Python 3.12, gồm cả thư viện kiểm tra demo cũ |
| `frontend/src/` | Trang React, CSS, API wrapper và types |
| `frontend/package-lock.json` | Phiên bản thư viện frontend cố định |
| `contracts/openapi.json` | Hợp đồng API chung được export |
| `scripts/setup.ps1` | Cài môi trường cục bộ trên Windows |
| `scripts/start-database.ps1`, `compose.yaml` | Chạy PostgreSQL cục bộ, giữ database và mật khẩu qua lần chạy lại |
| `app/`, `tests/`, `sample_data/` | Demo cũ được giữ nguyên; không được backend mới nạp |
| `VAULT_text/` | Hai tài liệu nguồn được giữ nguyên |

## Tài liệu dự án

| Tài liệu | Nội dung |
| --- | --- |
| [PROJECT](.planning/PROJECT.md) | Mục tiêu, phạm vi, nguồn và quyết định còn mở |
| [REQUIREMENTS](.planning/REQUIREMENTS.md) | Yêu cầu và tiêu chí nghiệm thu |
| [ROADMAP](.planning/ROADMAP.md) | Các giai đoạn và bước tiếp theo |
| [STATE](.planning/STATE.md) | Tiến độ thực tế, kết quả kiểm tra và giới hạn |
| [TECH_STACK](.planning/TECH_STACK.md) | Stack và lý do lựa chọn |
| [ARCHITECTURE](.planning/ARCHITECTURE.md) | Cấu trúc, trách nhiệm và API contract |
| [CONVENTIONS](.planning/CONVENTIONS.md) | Quy ước code, kiểm tra và Git |
| [AGENTS](AGENTS.md) | Hướng dẫn chung |
| [Backend](backend/AGENTS.md) / [Frontend](frontend/AGENTS.md) | Hướng dẫn riêng |
| [Project-planning skill](.agents/skills/project-planning/SKILL.md) | Quy trình duy trì kế hoạch |

Nguồn gốc: [hướng dẫn hành động Tech](VAULT_text/14_TECH_FOCUS_TRUST_DATAROOM_TECHDD_BUILD_BUY.md) và [hướng dẫn triển khai](VAULT_text/16_HUONG_DAN_TRIEN_KHAI_TECH_VAULT.md). Tên nguồn khác tên chung ban đầu; giả định A-01 vẫn được ghi trong PROJECT.

## Nếu chưa kết nối được

- Kiểm tra cửa sổ backend còn chạy, sau đó thử API trực tiếp ở cổng 8000.
- Nếu API trực tiếp hoạt động nhưng trang lỗi, kiểm tra `VITE_API_BASE_URL` / `BACKEND_PROXY_TARGET` và khởi động lại Vite.
- Nếu cổng đã được dùng, dừng tiến trình của bạn đang chiếm cổng hoặc cấu hình lại cổng và proxy đồng bộ; Vite không tự đổi sang cổng khác.
- Dùng `npm.cmd` như hướng dẫn để tránh lỗi PowerShell chặn `npm.ps1`.
- Nếu thiếu thư viện, chạy lại script setup. Health check không cần PostgreSQL; danh sách/lưu hồ sơ thì cần.
- Nếu hồ sơ báo chưa bật bản xem trước, đặt `INTERNAL_PREVIEW_ENABLED=true` như bước 2 rồi khởi động lại backend.
- Nếu báo không đọc/lưu được dữ liệu, mở Docker Desktop, chạy script database rồi Alembic `upgrade head`. Chỉ kiểm tra URL trong `.env` trên máy bạn, không chia sẻ mật khẩu trong log hoặc ảnh chụp.

Bước tiếp theo: thử hai luồng bằng dữ liệu giả lập theo hướng dẫn trên và ghi lại điểm cần chỉnh. Trước khi dùng tài liệu thật hoặc chia sẻ cho buyer, cần chốt đăng nhập, NDA, phê duyệt, phân quyền và phương án VDR vận hành. Chưa commit hoặc push.

## Deploy full-stack demo để link public test giống local

Mục tiêu của mode này: giữ frontend trên Vercel nhưng thêm backend public + PostgreSQL + persistent upload directory để đồng nghiệp test được các màn **Doanh nghiệp**, **Phòng dữ liệu**, upload/preview file và API health giống local ở mức MVP synthetic.

> Lưu ý: đây vẫn là hosted demo dùng dữ liệu giả lập, chưa phải production cho dữ liệu thật. Chưa có auth/RBAC/MFA/audit/watermark/antivirus production-grade.

### Phương án Railway được chọn

```text
Vercel frontend
  -> Railway FastAPI backend
  -> Railway PostgreSQL
  -> Railway Volume /data/vault-uploads
```

Repo có sẵn cấu hình Railway:

- `Dockerfile.railway`: build backend FastAPI từ `backend/requirements.txt`.
- `railway.json`: dùng Dockerfile, chạy Alembic ở pre-deploy, start Uvicorn bằng `$PORT`, healthcheck `/api/v1/health`.
- `.dockerignore`: loại node_modules, dist, .env, .tmp, .data khỏi Docker context.

Các bước trên Railway:

1. Tạo Railway project mới.
2. Add PostgreSQL service.
3. Add backend service từ repo hoặc deploy bằng CLI `railway up` tại thư mục `vault-core`.
4. Generate public domain cho backend service trong Settings → Networking.
5. Add volume cho backend, mount path `/data`.
6. Set variables cho backend service:

```text
PROJECT_NAME=VAULT Core
VERSION=0.1.0
API_V1_STR=/api/v1
ENVIRONMENT=hosted-demo
DATABASE_URL=${{Postgres.DATABASE_URL}}
INTERNAL_PREVIEW_ENABLED=true
UPLOAD_DIRECTORY=/data/vault-uploads
MAX_UPLOAD_BYTES=10485760
ALLOWED_ORIGINS=https://frontend-xi-eosin-36.vercel.app
ALLOWED_HOSTS=
DEMO_PASSWORD=<optional shared demo password>
```

Nếu service PostgreSQL trên Railway không tên là `Postgres`, đổi reference `DATABASE_URL=${{Postgres.DATABASE_URL}}` theo đúng tên service trên canvas, hoặc paste database URL trực tiếp. Backend tự nhận `postgres://...`, `postgresql://...` và đổi sang driver `postgresql+psycopg://...`. Backend cũng tự đọc `RAILWAY_PUBLIC_DOMAIN` để allow host Railway-provided domain; chỉ cần `ALLOWED_HOSTS` khi dùng custom domain hoặc domain ngoài Railway.

Sau khi backend Railway lên, mở:

```text
https://<railway-backend-domain>/api/v1/health
```

Kỳ vọng `status=ok`, `scope=liveness`.

### Cấu hình Vercel frontend gọi Railway backend

Trong Vercel project frontend, đặt environment variable production:

```text
VITE_API_BASE_URL=https://<railway-backend-domain>/api/v1
```

Redeploy production. Khi biến này tồn tại, Vercel sẽ không chặn các route Company/Room nữa và frontend sẽ gọi backend Railway public.

Smoke test:

```text
https://frontend-xi-eosin-36.vercel.app/#/health
https://frontend-xi-eosin-36.vercel.app/#/companies
https://frontend-xi-eosin-36.vercel.app/#/rooms
https://frontend-xi-eosin-36.vercel.app/#/investor-mvp
```

Tạo hồ sơ giả lập, tạo phòng dữ liệu, upload file PNG/PDF/TXT nhỏ, reload trang và kiểm tra dữ liệu/file còn nguyên. Nếu upload xong nhưng mất file sau restart, kiểm tra Railway volume mount path `/data` và `UPLOAD_DIRECTORY=/data/vault-uploads`.

### Phương án Render/Neon thay thế

```text
Vercel frontend
  -> Render FastAPI backend
  -> Neon Postgres
  -> Render persistent disk /var/data/vault-uploads
```

### 1. Tạo Neon Postgres

Tạo database Neon mới và lấy connection string. Có thể dùng dạng Neon mặc định:

```text
postgresql://USER:PASSWORD@HOST/DB?sslmode=require
```

Backend sẽ tự đổi sang driver `postgresql+psycopg://...`, không cần sửa tay trong secret nếu provider đưa `postgresql://`.

### 2. Tạo Render web service

Có thể dùng `render.yaml` ở repo root hoặc nhập thủ công trên UI.

Thiết lập chính:

```text
Runtime: Python
Build command: pip install -r backend/requirements.txt && python -m alembic -c backend/alembic.ini upgrade head
Start command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
Health check path: /api/v1/health
Persistent disk mount path: /var/data
```

Environment variables trên Render:

```text
PROJECT_NAME=VAULT Core
VERSION=0.1.0
API_V1_STR=/api/v1
ENVIRONMENT=hosted-demo
DATABASE_URL=<Neon connection string>
INTERNAL_PREVIEW_ENABLED=true
UPLOAD_DIRECTORY=/var/data/vault-uploads
MAX_UPLOAD_BYTES=10485760
ALLOWED_HOSTS=<render-backend-hostname, ví dụ vault-core-api.onrender.com>
ALLOWED_ORIGINS=https://frontend-xi-eosin-36.vercel.app
DEMO_PASSWORD=<optional shared demo password>
```

Nếu đặt `DEMO_PASSWORD`, mở frontend sẽ có mục **Demo password** để nhập password trên trình duyệt. Đây chỉ là demo gate nhẹ, không phải auth thật.

### 3. Cấu hình Vercel frontend gọi backend

Trong Vercel project frontend, đặt environment variable:

```text
VITE_API_BASE_URL=https://<render-backend-hostname>/api/v1
```

Sau đó redeploy production. Khi biến này tồn tại, Vercel sẽ không chặn các route Company/Room nữa và frontend sẽ gọi backend public.

### 4. Smoke test sau deploy

1. Mở backend health:

```text
https://<render-backend-hostname>/api/v1/health
```

Kỳ vọng `status=ok`, `scope=liveness`.

2. Mở frontend:

```text
https://frontend-xi-eosin-36.vercel.app/#/health
https://frontend-xi-eosin-36.vercel.app/#/companies
https://frontend-xi-eosin-36.vercel.app/#/rooms
https://frontend-xi-eosin-36.vercel.app/#/investor-mvp
```

3. Tạo hồ sơ giả lập, tạo phòng dữ liệu, upload file PNG/PDF/TXT nhỏ, reload trang và kiểm tra dữ liệu/file còn nguyên.

Nếu health chạy nhưng hồ sơ/phòng dữ liệu lỗi 403, kiểm tra lại `ALLOWED_HOSTS` và `ALLOWED_ORIGINS`. Nếu lỗi 503 database, kiểm tra `DATABASE_URL` và migration trong Render build log. Nếu upload xong nhưng mất file sau restart, kiểm tra persistent disk/mount path và `UPLOAD_DIRECTORY`.
