from pathlib import Path
from pdf2image import convert_from_path
import os
pdf_path = Path("/content/tygz-001.pdf")
os.makedirs("/content/tygz-001/img",exist_ok=True)
img_path=Path("/content/tygz-001/img")

convert_from_path(pdf_path, output_folder=img_path,fmt='jpeg',output_file=pdf_path.stem,dpi=100)