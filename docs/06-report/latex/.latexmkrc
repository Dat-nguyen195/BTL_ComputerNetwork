# UTF-8 Vietnamese requires XeLaTeX. Keep local build output out of the sources.
$pdf_mode = 5;
$xelatex = 'xelatex -no-shell-escape -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$out_dir = 'build';
$max_repeat = 5;
