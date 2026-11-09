# Nguồn LaTeX của báo cáo chính

Bản PDF chính thức để đọc, in và nộp là [final/report.pdf](../final/report.pdf). Toàn bộ nội dung báo cáo có thể chỉnh sửa trực tiếp trong thư mục này với file chính là [report.tex](report.tex). [packet-tracer-validation.pdf](../final/packet-tracer-validation.pdf) là phụ lục kiểm thử ngắn hai trang, không phải một bản báo cáo trùng.

## Biên dịch trên máy local

Dùng **XeLaTeX**, UTF-8. Lỗi `Unicode character ... not set up for use with LaTeX` là do chọn pdfLaTeX. File `report.tex` có chỉ dẫn engine và thông báo lỗi rõ ràng nếu chạy nhầm. `fonts.tex` chọn font có sẵn trên Windows/TeX Live; không cần cài Times New Roman trên Linux.

Trong thư mục `docs/06-report/latex`:

```bash
latexmk report.tex
```

`.latexmkrc` tự chọn XeLaTeX, cập nhật mục lục và đưa PDF/file phụ vào `build/`, đồng thời tự động đồng bộ sang `docs/06-report/final/report.pdf`. Nếu gọi từ root repository:

```bash
python3 scripts/build_report.py
```

Trong VS Code/LaTeX Workshop, mở root dự án rồi build `report.tex`: recipe mặc định của workspace là **XeLaTeX (Vietnamese report)**. File PDF tự động được cập nhật vào `docs/06-report/final/report.pdf` và `docs/06-report/latex/report.pdf`.

Nếu không có latexmk, chạy XeLaTeX ba lượt từ thư mục nguồn:

```bash
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error report.tex
```

Trên Ubuntu cần `texlive-xetex`, `texlive-latex-extra`, `texlive-fonts-recommended`; `fonts-dejavu-core` là font dự phòng. Không dùng pdfLaTeX cho báo cáo này.

## Overleaf và bộ nguồn độc lập

Upload toàn bộ [report-latex.zip](../final/report-latex.zip), chọn **Main document: report.tex**, **Compiler: XeLaTeX**, rồi Recompile. Bộ nguồn không cần Python, Pandoc, GNS3 hoặc đường dẫn tuyệt đối. Overleaf không tự đọc cấu hình LaTeX Workshop; cần đặt compiler một lần trong Menu.

- `report.tex`: toàn bộ nội dung, bảng và phụ lục A-F.
- `header.tex`, `fonts.tex`: kiểu trình bày, font và hỗ trợ trang ngang.
- `cover.tex`, `metadata.tex`: bìa/logo, L08, nhóm 2, danh sách thành viên và phân công BTL1/BTL2; GVHD ThS. Bùi Xuân Giang.
- `assets/`: logo gốc, sơ đồ logic, sơ đồ vật lý Main và Aux dạng PDF vector.
- `.latexmkrc`: cấu hình compiler và thư mục build.

## Biên soạn và cập nhật báo cáo

Nguồn nội dung chính là [report.tex](report.tex). Mọi chỉnh sửa được thực hiện trực tiếp trong file này (hoặc bìa trong `cover.tex`, thông tin nhóm/GVHD trong `metadata.tex`).

Từ root, chạy lệnh build chính thức:

```bash
python3 scripts/build_report.py
```

Script sẽ biên dịch trực tiếp từ `report.tex` bằng XeLaTeX, xuất ra [docs/06-report/final/report.pdf](../final/report.pdf) và đóng gói [report-latex.zip](../final/report-latex.zip).
