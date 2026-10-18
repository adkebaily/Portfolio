#!/bin/sh
# Compile les CV. Usage : sh cv/build.sh
#  - version « site » (sans téléphone ni adresse) -> public/CV_Kebaily.pdf et public/CV_Kebaily_EN.pdf
#  - version complète (si cv/private.tex existe)   -> cv/out/ (jamais publiée)
set -e
cd "$(dirname "$0")"
mkdir -p out
for src in CV CV_en; do
  pdflatex -interaction=nonstopmode -output-directory=out -jobname="${src}_site" "\def\cvpublic{1}\input{$src.tex}" >/dev/null
  if [ -f private.tex ]; then
    pdflatex -interaction=nonstopmode -output-directory=out -jobname="${src}_complet" "\input{$src.tex}" >/dev/null
  fi
done
cp out/CV_site.pdf ../public/CV_Kebaily.pdf
cp out/CV_en_site.pdf ../public/CV_Kebaily_EN.pdf
rm -f out/*.aux out/*.log out/*.out
echo "OK : versions site copiées dans public/ ; versions complètes dans cv/out/"
