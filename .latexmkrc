# Also select XeLaTeX when latexmk is launched from the repository root.
$pdf_mode = 5;
$do_cd = 1;
$out_dir = 'build';
$xelatex = 'xelatex -no-shell-escape -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$max_repeat = 5;
