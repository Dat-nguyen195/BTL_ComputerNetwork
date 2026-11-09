# Also select XeLaTeX when latexmk is launched from the repository root.
$pdf_mode = 5;
$do_cd = 1;
$out_dir = 'build';
$xelatex = 'xelatex -no-shell-escape -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$max_repeat = 5;
$success_cmd = 'python3 -c "import shutil, pathlib; p=pathlib.Path(\'%D\').resolve(); f=p.parents[2]/\'final/report.pdf\'; l=p.parents[2]/\'latex/report.pdf\'; shutil.copyfile(p, f); shutil.copyfile(p, l)"';
