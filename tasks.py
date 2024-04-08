import sqlite3
from tkinter import Tk, Label, Button, Entry, Text
from datetime import datetime

def loo_tabel():
    conn.execute('''CREATE TABLE IF NOT EXISTS ulesanded (
                    id INTEGER PRIMARY KEY,
                    pealkiri TEXT NOT NULL,
                    kirjeldus TEXT,
                    tähtaeg DATE,
                    olek TEXT DEFAULT 'Ootel'
                )''')
    conn.commit()

def lisa_ülesanne():
    pealkiri = pealkiri_entry.get()
    kirjeldus = kirjeldus_entry.get("1.0", "end-1c")
    tähtaeg = tähtaeg_entry.get()
    conn.execute("INSERT INTO ulesanded (pealkiri, kirjeldus, tähtaeg) VALUES (?, ?, ?)", (pealkiri, kirjeldus, tähtaeg))
    conn.commit()
    result_text.insert("end", "Ülesanne lisatud edukalt.\n")

def vaata_ülesandeid():
    cursor = conn.execute("SELECT * FROM ulesanded")
    ülesanded = cursor.fetchall()
    result_text.delete("1.0", "end")
    if len(ülesanded) > 0:
        result_text.insert("end", "Kõik ülesanded:\n")
        for ülesanne in ülesanded:
            result_text.insert("end", f"ID: {ülesanne[0]}, Pealkiri: {ülesanne[1]}, Kirjeldus: {ülesanne[2]}, Tähtaeg: {ülesanne[3]}\n")
    else:
        result_text.insert("end", "Ülesandeid ei leitud.\n")

def kustuta_ülesanne():
    ülesande_id = int(kustutatava_id_entry.get())
    conn.execute("DELETE FROM ulesanded WHERE id = ?", (ülesande_id,))
    conn.commit()
    result_text.insert("end", f"Ülesanne ID {ülesande_id} kustutatud edukalt.\n")

def põhifunktsioon():
    loo_tabel()

    # Define GUI elements
    root = Tk()
    root.title("Ülesannete Haldur")

    global pealkiri_entry, kirjeldus_entry, tähtaeg_entry, kustutatava_id_entry, result_text

    pealkiri_label = Label(root, text="Pealkiri:")
    pealkiri_label.grid(row=0, column=0)
    pealkiri_entry = Entry(root)
    pealkiri_entry.grid(row=0, column=1)

    kirjeldus_label = Label(root, text="Kirjeldus:")
    kirjeldus_label.grid(row=1, column=0)
    kirjeldus_entry = Text(root, height=4, width=30)
    kirjeldus_entry.grid(row=1, column=1)

    tähtaeg_label = Label(root, text="Tähtaeg (YYYY-MM-DD):")
    tähtaeg_label.grid(row=2, column=0)
    tähtaeg_entry = Entry(root)
    tähtaeg_entry.grid(row=2, column=1)

    lisa_button = Button(root, text="Lisa Ülesanne", command=lisa_ülesanne)
    lisa_button.grid(row=3, column=0, columnspan=2)

    vaata_button = Button(root, text="Vaata Ülesandeid", command=vaata_ülesandeid)
    vaata_button.grid(row=4, column=0, columnspan=2)

    kustutatava_id_label = Label(root, text="Kustutatava ülesande ID:")
    kustutatava_id_label.grid(row=6, column=0)
    kustutatava_id_entry = Entry(root)
    kustutatava_id_entry.grid(row=6, column=1)

    kustuta_button = Button(root, text="Kustuta Ülesanne", command=kustuta_ülesanne)
    kustuta_button.grid(row=5, column=0, columnspan=2)

    result_text = Text(root, height=10, width=60)
    result_text.grid(row=7, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    conn = sqlite3.connect('ülesannete_haldur.db')
    põhifunktsioon()
    conn.close()
