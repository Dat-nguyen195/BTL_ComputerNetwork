# Nguồn LaTeX của báo cáo chính

Bản PDF chính thức để đọc, in và nộp là [final/report.pdf](../final/report.pdf). Bộ nguồn này biên dịch ra cùng nội dung. [packet-tracer-validation.pdf](../final/packet-tracer-validation.pdf) là phụ lục kiểm thử ngắn hai trang, không phải một bản báo cáo trùng.

## Biên dịch trên máy local

Dùng **XeLaTeX**, UTF-8. Lỗi `Unicode character ... not set up for use with LaTeX` là do chọn pdfLaTeX. File `report.tex` có chỉ dẫn engine và thông báo lỗi rõ ràng nếu chạy nhầm. `fonts.tex` chọn font có sẵn trên Windows/TeX Live; không cần cài Times New Roman trên Linux.

Trong thư mục `docs/06-report/latex`:

```bash
latexmk report.tex
```

`.latexmkrc` tự chọn XeLaTeX, cập nhật mục lục và đưa PDF/file phụ vào `build/`. Nếu gọi từ root repository:

```bash
latexmk -xelatex -cd docs/06-report/latex/report.tex
```

Trong VS Code/LaTeX Workshop, mở root dự án rồi build `report.tex`: recipe mặc định của workspace là **XeLaTeX (Vietnamese report)**. Nếu editor đã mở trước khi cập nhật, reload cửa sổ hoặc chọn recipe này. PDF xem trước nằm ở `latex/build/report.pdf`; bản nộp nằm ở `final/report.pdf`.

Nếu không có latexmk, chạy XeLaTeX ba lượt từ thư mục nguồn với output directory đã tạo:

```bash
mkdir -p build
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build report.tex
```

Trên Ubuntu cần `texlive-xetex`, `texlive-latex-extra`, `texlive-fonts-recommended`; `fonts-dejavu-core` là font dự phòng. Không dùng pdfLaTeX cho báo cáo này.

## Overleaf và bộ nguồn độc lập

Upload toàn bộ [report-latex.zip](../final/report-latex.zip), chọn **Main document: report.tex**, **Compiler: XeLaTeX**, rồi Recompile. Bộ nguồn không cần Python, Pandoc, GNS3 hoặc đường dẫn tuyệt đối. Overleaf không tự đọc cấu hình LaTeX Workshop; cần đặt compiler một lần trong Menu.

- `report.tex`: toàn bộ nội dung, bảng và phụ lục A-F.
- `header.tex`, `fonts.tex`: kiểu trình bày, font và hỗ trợ trang ngang.
- `cover.tex`, `metadata.tex`: bìa/logo, L08, nhóm 2, hai người thực hiện BTL2; dòng giảng viên tự ẩn khi chưa có thông tin.
- `assets/`: logo gốc, sơ đồ logic, sơ đồ vật lý Main và Aux dạng PDF vector.
- `.latexmkrc`: cấu hình compiler và thư mục build.

## Cập nhật báo cáo từ nguồn dự án

Nguồn nội dung là [report.md](../source/report.md) và [design-appendices.md](../source/design-appendices.md). `report-with-evidence.md` và `report.tex` được sinh lại; sửa trực tiếp các file này sẽ bị ghi đè khi build từ Markdown.

Từ root, dùng Python có CairoSVG, Pandoc và XeLaTeX:

```bash
python3 scripts/build_report.py
```

Nếu các SVG không thay đổi và đã có PDF vector được kiểm tra trong `assets`, có thể dùng `python -X utf8 scripts/build_report.py --reuse-diagrams` để tái sử dụng hình, không cần CairoSVG. Không dùng tùy chọn này sau khi sửa sơ đồ SVG. Bản ngày 09/11/2026 tổ chức nội dung thành bốn chương hoàn chỉnh; các bằng chứng runtime vẫn giữ ngày chạy và nền tảng gốc.

Script cập nhật Markdown ghép bằng chứng, LaTeX, hình vector, `output/pdf/report.pdf`, PDF chính thức và ZIP nguồn. Windows có thể dùng `python -X utf8 scripts/build_report.py --engine tectonic`. Sau thay đổi cần render/kiểm PDF, cập nhật QA/hash rồi đóng gói lại bằng `scripts/package_submission.py`. Bản PDF local do build editor chỉ để xem trước; không dùng file PDF cũ nằm cạnh `report.tex` để nộp.
