cd "/content/"

# 1. NDLOCRのリポジトリをcloneする(--recursiveを忘れずに！)
rm -rf ndlocr_cli
git clone --recursive https://github.com/ndl-lab/ndlocr_cli

# 2. 必要なパッケージをインストールする
PROJECT_DIR="/content/ndlocr_cli"

# colabでインストールに時間を要するものを除外
# sed -i -e 's/scipy/#scipy/g' $PROJECT_DIR/requirements.txt
# sed -i -e 's/scikit/#scikit/g' $PROJECT_DIR/requirements.txt

# pip install -r $PROJECT_DIR/requirements.txt
# pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
# pip install mmcv-full==1.4.0 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.8.0/index.html

pip install mmcv==2.0.0 -f https://download.openmmlab.com/mmcv/dist/cu118/torch2.0/index.html
pip install mmdet==3.0.0

cd $PROJECT_DIR/src/ndl_layout/mmdetection
python setup.py bdist_wheel
pip install dist/*.whl

# # 4. OCRに必要な学習済みモデルをダウンロードする
cd $PROJECT_DIR
wget https://lab.ndl.go.jp/dataset/ndlocr/text_recognition/mojilist_NDL.txt -P ./src/text_recognition/models
wget https://lab.ndl.go.jp/dataset/ndlocr/text_recognition/ndlenfixed64-mj0-synth1.pth -P ./src/text_recognition/models
# wget https://lab.ndl.go.jp/dataset/ndlocr/ndl_layout/ndl_layout_config.py -P ./src/ndl_layout/models
wget https://lab.ndl.go.jp/dataset/ndlocr/ndl_layout/epoch_140_all_eql_bt.pth -P ./src/ndl_layout/models
wget https://lab.ndl.go.jp/dataset/ndlocr/separate_pages_ssd/weights.hdf5 -P ./src/separate_pages_ssd/ssd_tools

# 4.5. 拡張機能【読み順の自動ソート】を追加する
rm ./cli/core/inference.py
wget https://raw.githubusercontent.com/blue0620/simple_reading_order/main/inference.py -P ./cli/core/
wget https://lab.ndl.go.jp/dataset/ndlocr/appendix/simple_reading_order_model.joblib -P .

# 6. PDFを画像に変換するためのパッケージのインストール
apt-get install poppler-utils
pip install pdf2image

# transparent
pip install python-bidi
pip install reportlab
