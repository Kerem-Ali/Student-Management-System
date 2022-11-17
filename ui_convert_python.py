from PyQt5 import uic

with open("OgrenciIslemleri.py","w",encoding="utf-8") as fout:
    uic.compileUi("ogrenci.ui",fout)
