# UTF-8 Vietnamese requires XeLaTeX. Keep local build output out of the sources.
$pdf_mode = 5;
$xelatex = 'xelatex -no-shell-escape -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$out_dir = 'build';
$max_repeat = 5;
$success_cmd = 'python3 -c "import shutil, pathlib; p=pathlib.Path(\'%D\').resolve(); f=p.parents[2]/\'final/report.pdf\'; l=p.parents[2]/\'latex/report.pdf\'; [shutil.copyfile(p, dest) for dest in (f,l)] if f.parent.is_dir() and l.parent.is_dir() else None"';
