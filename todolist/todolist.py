#Hilmi Özbay 170422050 
#Donem Sonu Projesi

from pathlib import Path
from tkcalendar import Calendar
import json
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox,messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HP\Desktop\todolist\Dokumanlar")#Dosya yolundan kaynaklanan hatalar oluşabilir.

#Kullanılan bileşenler:
#button_1 -------> Silme metodu
#button_2 -------> Önemli listesine ekleme
#button_3 -------> Tamamlandı
#button_4 -------> Tümünü sil
#button_5 -------> Ekle
#entry_1 --------> Tarih seçme
#entry_2 --------> iş girişi
#isListesi--------> İş Listesi listbox
#onemliIs --------> Önemli İş Listesi listbox
#image_1 ---------> Logo
#image_2 ---------> "To Do List" yazısı
#image_3----------> "Önemli" Yazısı

gorev_listesi = [] #Görevleri tutmak için liste
gorev_listesi_onemli = [] #Önemli görevleri tutmak için liste


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def silme_islemi():
    try:
        islistesi_secilen = isListesi.curselection() # İşlistesi listboxundaki seçilen elemanı, değişkene atama
        onemli_is_secilen = onemliIs.curselection() # Önemli iş listboxundaki seçilen elemanı, değişkene atama

        if not islistesi_secilen and not onemli_is_secilen:
            raise ValueError("Lütfen silinecek bir iş seçiniz!")

        if islistesi_secilen:
            index = islistesi_secilen[0] # Seçilen elemanın indeksini alma
            isListesi.delete(index)# Seçilen elemanı silme
            del gorev_listesi[index]# Seçilen elemanı gorev_listesi listesinden silme

        if onemli_is_secilen:
            index = onemli_is_secilen[0] # Seçilen elemanın indeksini alma
            onemliIs.delete(index)# Seçilen elemanı silme
            del gorev_listesi_onemli[index] # Seçilen elemanı gorev_listesi_onemli listesinden silme

    except ValueError:
        messagebox.showinfo("Uyarı","Bir eleman seçiniz!")


def ekleme_islemi():# İşlerin bulunduğu listbox'a eleman eklemek için kullanılan metot
    is_adi = entry_2.get()#Entry 2 den işi alma
    if is_adi:
        isListesi.insert("end", is_adi)# listboxun sonuna işi ekleme
        gorev_listesi.append(is_adi)
        entry_2.delete(0, "end")#ekle butonuna basılınca entry_2 sıfırlanıcak
    try:
        if is_adi=="":
            raise ValueError()#boş ise hata verecek
    except:
        messagebox.showinfo("Uyarı", "Lutfen bir iş giriniz! ")


def tamamlandi():
    try:
        secilen_is = isListesi.curselection()#İş listesi listboxunda seçilen elemanı tutar
        secilen_onemli = onemliIs.curselection()#Önemli İş listboxunda seçilen elemanı tutar
        if not secilen_is and not secilen_onemli:
            raise TypeError() 

        if secilen_is:
            item_text = isListesi.get(secilen_is) # seçilen eleman item_text ' e atanır 
            updated_text = f"{item_text}✓ " # item_text in yanina ✓ işareti konarak text guncellenir
            isListesi.delete(secilen_is)#silme_güncelleme
            isListesi.insert(secilen_is, updated_text)#silme güncelleme
            entry_2.delete(0, "end")

        if secilen_onemli:
            item_text2 = onemliIs.get(secilen_onemli)# seçilen eleman item_text2 ' ye atanır 
            updated_text2 = f"{item_text2}✓ " # item_text2'nin yanina ✓ işareti konarak text guncellenir
            onemliIs.delete(secilen_onemli) #silme-güncelleme
            onemliIs.insert(secilen_onemli, updated_text2)#silme-güncelleme
            entry_2.delete(0, "end")

    except Exception:
        messagebox.showinfo("Uyarı","Herhangi bir eleman seçiniz!" )


def tumunu_sil():
    try: 
        if isListesi.size() == 0 and onemliIs.size()==0: #İş listesi listbox'ı ile onemli iş listboxu boş ise hata verir
            raise TypeError()
    except TypeError:
        messagebox.showinfo("Uyarı", "Silinecek İş Bulunamadı!")
    else:
        isListesi.delete(0, "end")#iş listesindeki tüm elemanları silme
        onemliIs.delete(0,"end")#önemli iş listesindeki tüm elemanları silme
        gorev_listesi_onemli.clear()
        gorev_listesi.clear()

def onemli_listesi():
    try:
        selected_index = isListesi.curselection() # İş listesi listboxunda seçilen eleman selected_index e atanır.
        if not selected_index:
            raise ValueError("Lütfen bir iş seçiniz!")

        item_text = isListesi.get(selected_index)
        onemliIs.insert("end", item_text)#önemli iş listboxuna eleman eklenir
        isListesi.delete(selected_index)#sonra iş listesi listboxundan silinir
        gorev_listesi_onemli.append(selected_index)#Önemli listesine eklenir

    except ValueError as e:
        messagebox.showinfo("Uyarı", str(e))

        
window = Tk()#Tk dan bir nesne oluşturma

window.geometry("873x494")
window.configure(bg = "#3A9CEB")


canvas = Canvas(# Canvas ile panel oluşturma
    window,
    bg = "#3A9CEB",
    height = 494,
    width = 873,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0) #canvası konumlandırma
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    59.0,
    44.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))#Başlık ekleme

image_2 = canvas.create_image(#başlık konumlandırma
    475.0,
    58.0,
    image=image_image_2
)

entry_1 = Calendar(#Takvim ekleme
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(#Takvim konumlandırma
    x=61.0,
    y=167.0,
    width=220.0,
    height=180.0
)


entry_2 = Entry(#Liste giriş
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font="Jua 12"
)

entry_2.place(#liste giriş entry konumlandırma
    x=309.0,
    y=115.0,
    width=409.0,
    height=27.0
)


isListesi = Listbox(# İş listesi
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font="Jua 13",
    activestyle='none'
)
isListesi.place(#iş listesi konumlandırma
    x=309.0,
    y=163.0,
    width=409.0,
    height=131.0
)


onemliIs = Listbox(#Önemli İşler
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,font="Jua 13",
    activestyle='none'

)
onemliIs.place( # Önemli işler listbox'ı konumlandırma
    x=309.0,
    y=326.0,
    width=409.0,
    height=131.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button( #Silme Butonu
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=silme_islemi,
    relief="flat"
)

button_1.place(#Silme butonu konumlandırma
    x=738.0,
    y=316.0,
    width=43.0,
    height=43.0
)

button_image_2 = PhotoImage( #Önemli işlere ekleme butonu resmi
    file=relative_to_assets("button_2.png"))

button_2 = Button( #Önemli işlere ekleme butonu
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=onemli_listesi ,
    relief="flat"
)
button_2.place(#Önemli işlere ekleme butonu konumlandırma
    x=738.0,
    y=253.0,
    width=43.0,
    height=43.0
)

button_image_3 = PhotoImage( #Tamamlandı butonu resmi
    file=relative_to_assets("button_3.png"))

button_3 = Button( #Tamamlandı butonu
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=tamamlandi,
    relief="flat"
)
button_3.place(#Tamamlandı butonu konumlandırma
    x=738.0,
    y=190.0,
    width=43.0,
    height=43.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(#Tümünü sil butonu
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=tumunu_sil,
    relief="flat"
)
button_4.place(#Tümünü sil butonu konumlandırma
    x=738.0,
    y=379.0,
    width=43.0,
    height=43.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    340.0,
    308.0,
    image=image_image_3
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))

button_5 = Button(#Listeye ekle butonu (İş listesine ekler)
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=ekleme_islemi,
    relief="flat"
)
button_5.place(# Ekleme butonu konumlandırma
    x=691.0,
    y=118.0,
    width=23.0,
    height=23.0
)

def veriyi_kaydet():# Veriyi bir dosyaya kaydetmek için
    data = {
        "isListesi": isListesi.get(0, "end"),
        "onemliIs": onemliIs.get(0, "end"),
    }
    with open(ASSETS_PATH / "veri.json", "w") as dosya:
        json.dump(data, dosya)

def veriyi_yukle():# Veriyi bir dosyadan yüklemek için 
    try:
        with open(ASSETS_PATH / "veri.json", "r") as dosya:
            data = json.load(dosya)
            isListesi.delete(0, "end")
            onemliIs.delete(0, "end")
            for task in data.get("isListesi", []):
                isListesi.insert("end", task)
            for important_task in data.get("onemliIs", []):
                onemliIs.insert("end", important_task)
    except FileNotFoundError:
        pass

def kapatma():#pencere kapatılınca çağırılan metot
    veriyi_kaydet()
    window.destroy()


veriyi_yukle()

window.protocol("WM_DELETE_WINDOW", kapatma)
window.resizable(False, False)

window.mainloop()
