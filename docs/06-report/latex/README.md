# Báo cáo LaTeX có logo Bách Khoa

Bộ nguồn đầy đủ, không phải file bọc một PDF có sẵn. Biên dịch bằng **XeLaTeX**, UTF-8; font DejaVu Serif/Sans/Mono hỗ trợ tiếng Việt. Bìa dùng đúng ảnh `01_logobachkhoatoi.png` do người dùng cung cấp, được sao chép nguyên byte vào [assets/logo-bach-khoa.png](assets/logo-bach-khoa.png). LaTeX chỉ cắt phần trong suốt khi dàn trang, không sửa hoặc vẽ lại logo.

## Các file

- [report.tex](report.tex): toàn bộ nội dung bảy Step, bảng biểu, tài liệu tham khảo và phụ lục kiểm thử; có thể sửa trực tiếp.
- [cover.tex](cover.tex): trang bìa, khung và vị trí logo.
- [metadata.tex](metadata.tex): tên trường, môn học, đề tài, nhóm, giảng viên, lớp, thành viên/MSSV và ngày.
- [header.tex](header.tex): font, màu, mục lục, header/footer và số trang.
- [assets/topology.pdf](assets/topology.pdf): sơ đồ vector từ SVG của dự án.

Thông tin giảng viên, lớp và danh sách họ tên/MSSV chưa có dữ liệu xác nhận nên để rỗng trong `metadata.tex`; các dòng này tự ẩn trên bìa. Điền dữ liệu thật vào các macro tương ứng trước khi nộp, không cần sửa bố cục. Ví dụ danh sách thành viên có thể dùng `tabular` trong `\ReportMembers`.

## Biên dịch bộ nguồn hiện có

Không cần Python, Pandoc hoặc GNS3 để biên dịch các file đã bàn giao. Cần XeLaTeX với các package fontspec/unicode-math, graphicx, geometry, longtable/booktabs, fancyhdr, microtype, xurl, TikZ, etoolbox, needspace và font DejaVu. Có thể cài trên Ubuntu bằng `texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-dejavu-core`.

Từ root repository:

```bash
mkdir -p output/pdf
cd docs/06-report/latex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=../../../output/pdf report.tex
```

PDF ở `output/pdf/report.pdf`. Nếu không dùng `latexmk`, chạy `xelatex -output-directory=../../../output/pdf report.tex` ba lần để cập nhật mục lục và số trang.

Trên Overleaf: tải lên gói `docs/06-report/final/report-latex.zip`, đặt **Main document = report.tex**, **Compiler = XeLaTeX**, rồi Recompile. Các đường dẫn hình đều tương đối, không phụ thuộc máy người tạo. Chỉ dẫn này là cách dùng bộ nguồn; lần QA đã biên dịch bằng XeLaTeX local, chưa chạy dịch vụ Overleaf.

## Cập nhật lại từ Markdown và JSON evidence

```bash
python3 scripts/build_report.py
```

Chạy lệnh này ở root bằng Python có `cairosvg`; cần Pandoc và XeLaTeX. Script sinh lại `report.tex`, `assets/topology.pdf`, Markdown ghép evidence, PDF chuẩn tại `docs/06-report/final/report.pdf`, bản PDF local tại `output/pdf/report.pdf` và ZIP LaTeX. Các file `metadata.tex`, `cover.tex`, `header.tex` không bị ghi đè.

**Chọn một nguồn sửa nội dung:** nếu muốn tiếp tục dùng script, sửa `docs/06-report/source/report.md` rồi build; script sẽ ghi đè mọi thay đổi trực tiếp trong `report.tex`. Nếu sửa LaTeX trực tiếp, chỉ dùng XeLaTeX/latexmk cho đến khi đã đồng bộ lại Markdown. Khi nộp bản tự biên dịch, chép PDF đã kiểm vào đường dẫn PDF chuẩn và cập nhật package/checksum của dự án.
