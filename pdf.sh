# 7. テキスト化したいPDFをダウンロードする
curl https://dglb01.ninjal.ac.jp/ninjaldl/toyogakuge/001/PDF/tygz-001.pdf -o /content/tygz-001.pdf

# 8. PDFをjpeg画像に変換する
python test.py

# 9. OCRの実行
cd $PROJECT_DIR
python main.py infer /content/tygz-001 /content/tygz-001_output -s s -x