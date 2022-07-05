from ndl_ocr.util import Util

url = "https://clioimg.hi.u-tokyo.ac.jp/viewer/api/image/idata%2F850%2F8500%2F02%2F0101%2F0001.jpg" #@param {type:"string"}
# output_dir = "/content/drive/MyDrive/ndl_ocr/output/pdf_url" #@param {type:"string"}
output_dir = "aaa/content/drive/MyDrive/ndl_ocr/output/image_url" #@param {type:"string"}
process = "\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)" #@param ["\u3059\u3079\u3066: \u30CE\u30C9\u5143\u5206\u5272,\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u6587\u5B57\u8A8D\u8B58(OCR)"]
ruby = False #@param {type:"boolean"}

ins = Util.imgFromUrl(url, output_dir, process, ruby)

# Util.updateRuby(ruby)