from ndl_ocr.util import Util

input_dir = "sample2" #@param {type:"string"}
# output_dir = "/content/drive/MyDrive/ndl_ocr/output/pdf_url" #@param {type:"string"}
output_dir = "aaa/content/drive/MyDrive/ndl_ocr/output/pdf_dir" #@param {type:"string"}
process = "\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)" #@param ["\u3059\u3079\u3066: \u30CE\u30C9\u5143\u5206\u5272,\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u6587\u5B57\u8A8D\u8B58(OCR)"]
ruby = False #@param {type:"boolean"}

Util.pdfFromLocalDir(input_dir, output_dir, process, ruby)