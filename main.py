import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from OgrenciIslemleri import *

uygulama=QApplication(sys.argv)
pencere=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(pencere)

pencere.show()


import sqlite3

baglanti=sqlite3.connect("ogrenciler.db")
islem=baglanti.cursor()
baglanti.commit()

table=islem.execute("create table if not exists ogrenci (ogrAd text, ogrSoyad text, ogrSinif int, ogrSube text, ogrNumara int, ogrCinsiyet text)")
baglanti.commit()

def ogrenciEkle():
    OgrenciAdi=ui.lneAd.text().title()
    OgrenciSoyadi=ui.lneSoyad.text().upper()
    OgrenciSinifi=ui.cmbSinif.currentText()
    
    if OgrenciSinifi=="8(Hazirlik)":
        OgrenciSinifi=8
    else:
        OgrenciSinifi=int(OgrenciSinifi)
    
    OgrenciSubesi=ui.cmbSube.currentText()
    OgrenciNumarasi=int(ui.lneNumara.text())
    OgrenciCinsiyet=""
    if ui.rbErkek.isChecked():
        OgrenciCinsiyet="erkek"
    elif ui.rbKiz.isChecked():
        OgrenciCinsiyet="kiz"

    try:
        ekle="insert into ogrenci (ogrAd, ogrSoyad, ogrSinif, ogrSube, ogrNumara, ogrCinsiyet) values (?,?,?,?,?,?)"
        islem.execute(ekle,(OgrenciAdi,OgrenciSoyadi,OgrenciSinifi,OgrenciSubesi,OgrenciNumarasi,OgrenciCinsiyet))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı",10000)
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı==="+str(error))

    kayit_listele()

def listele():
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tblListe.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
    
def kayit_listele():
    
    ui.tblListe.clear()
    ui.tblListe.setHorizontalHeaderLabels(("Adi","Soyadi","Sinifi","Subesi","Numarasi","Cinsiyeti"))
    ui.tblListe.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    siralama=ui.cmbLsira.currentText()
    if siralama=="Artan":
        siralama="ASC"
    else:
        siralama="DESC"
    
    cinsiyet=ui.cmbCinsiyet.currentText()
    match cinsiyet:
        case "Erkek/Kiz":
            cinsiyet=""
        case "Erkek":
            cinsiyet="where ogrCinsiyet='erkek'"
        case "Kiz":
            cinsiyet="where ogrCinsiyet='kiz'"

    

    match  ui.cmbLkategori.currentText():
        case "KayitSirasi":
            sorgu="select * from ogrenci"+cinsiyet
            islem.execute(sorgu)

            listele()
        case "Ad":
            sorgu="select * from ogrenci {} order by ogrAd,ogrSoyad {}".format(cinsiyet,siralama)
            islem.execute(sorgu)

            listele()
        
        case "Soyad":
            sorgu="select * from ogrenci {} order by ogrSoyad,ogrAd {}".format(cinsiyet,siralama)
            islem.execute(sorgu)

            listele()

        case "Sinif":
            sorgu="select * from ogrenci {} order by ogrSinif {}".format(cinsiyet,siralama)
            islem.execute(sorgu)

            listele()
        
        case "Numara":
            sorgu="select * from ogrenci {} order by ogrNumara {}".format(cinsiyet,siralama)
            islem.execute(sorgu)

            listele()

kayit_listele()



def kayit_sil():
    sil_mesaj=QMessageBox.question(pencere,"Silme Onayı","Silmek İstededğinizden Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj==QMessageBox.Yes:
        secilen_kayit=ui.tblListe.selectedItems()
        
        silinecek_kayit=secilen_kayit[0].text()

        sorgu="delete from ogrenci where ogrAd = ?"

        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı ==="+str(error))

    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")

def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere,"Güncelleme Onayı","Bu kaydı Güncellemek istediğinizden Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

    if guncelle_mesaj == QMessageBox.Yes:
        try:
            OgrenciAdi=ui.lneAd.text().title()
            OgrenciSoyadi=ui.lneSoyad.text().upper()
            OgrenciSinifi=ui.cmbSinif.currentText()
            
            if OgrenciSinifi=="Hazirlik":
                OgrenciSinifi=8

            
            OgrenciSubesi=ui.cmbSube.currentText()
            OgrenciNumarasi=ui.lneNumara.text()
            OgrenciCinsiyeti=""
            if ui.rbErkek.isChecked():
                OgrenciCinsiyeti="erkek"
            elif ui.rbKiz.isChecked():
                OgrenciCinsiyeti="kiz"

            if OgrenciAdi == "" and OgrenciSoyadi == "" and OgrenciSinifi == "" and OgrenciSubesi == "":
                islem.execute("update ogrenci set ogrCinsiyet = ? where ogrNumara = ?",(OgrenciCinsiyeti,OgrenciNumarasi))

            elif OgrenciAdi == "" and OgrenciSoyadi == "" and OgrenciSinifi == "" and OgrenciCinsiyeti == "":
                islem.execute("update ogrenci set ogrSube = ? where ogrNumara = ?",(OgrenciSubesi,OgrenciNumarasi)) 

            elif OgrenciAdi == "" and OgrenciSoyadi == "" and OgrenciSubesi == "" and OgrenciCinsiyeti == "":
                islem.execute("update ogrenci set ogrSinif = ? where ogrNumara = ?",(OgrenciSinifi,OgrenciNumarasi))
                
            elif OgrenciAdi == "" and OgrenciSinifi == "" and OgrenciSubesi == "" and OgrenciCinsiyeti == "":
                islem.execute("update ogrenci set ogrSoyad = ? where ogrNumara = ?",(OgrenciSoyadi,OgrenciNumarasi))
                
            elif OgrenciSoyadi == "" and OgrenciSinifi == "" and OgrenciSubesi == "" and OgrenciCinsiyeti == "":
                islem.execute("update ogrenci set ogrAd = ? where ogrNumara = ?",(OgrenciAdi,OgrenciNumarasi))

            else:
                islem.execute("update ogrenci set ogrAd = ?, ogrSoyad = ? , ogrSinif = ?, OgrSubes = ?, OgrCinsiyet = ?",(OgrenciAdi,OgrenciSoyadi,OgrenciSinifi,OgrenciSubesi,OgrenciCinsiyeti))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === "+str(error))
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")





ui.btnEkle.clicked.connect(ogrenciEkle)
ui.btnListele.clicked.connect(kayit_listele)
ui.btnGuncelle.clicked.connect(kayit_guncelle)

ui.btnSil.clicked.connect(kayit_sil)


sys.exit(uygulama.exec_())
