import os
import sys

MAX_DIFF = 300


def check_png(dateipfad, png_byte_order='big'):
    print(f"Analysiere {dateipfad}")
    tatsaechliche_groesse_in_bytes = os.path.getsize(dateipfad)

    with open(dateipfad, 'rb') as byte_reader:
        if not (ist_png_datei(byte_reader)):
            return False

        erwartete_groesse_in_bytes = get_erwartete_groesse(byte_reader, png_byte_order)
        differenz = tatsaechliche_groesse_in_bytes - erwartete_groesse_in_bytes

        if differenz > MAX_DIFF:
            print(f"Die errechnete Größe beträgt etwa {erwartete_groesse_in_bytes / 1000}KB.")
            print(f"Die Datei ist tatsächlich {tatsaechliche_groesse_in_bytes / 1000}KB groß.")
            print(f"Die Differenz beträgt {differenz / 1000}KB.")
            print(f"Das sind {100 / erwartete_groesse_in_bytes * differenz}% mehr als errechnet.")
            return False

        return True


def ist_png_datei(byte_reader):
    erste_acht_byte = bytes_lesen(byte_reader, 8)
    erwartete_erste_acht_byte = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

    if erste_acht_byte == erwartete_erste_acht_byte:
        return True
    else:
        print(f"Die ersten acht Byte sind {erste_acht_byte}")
        print(f"Die ersten acht Byte sollten {erwartete_erste_acht_byte} sein")
        return False


def get_erwartete_groesse(byte_reader, png_byte_order):
    ihdr_werte = get_ihdr_werte(byte_reader, png_byte_order)
    bits = berechne_bits(ihdr_werte)
    bytes = bits / 8
    return bytes


def get_ihdr_werte(byte_reader, png_byte_order):
    erwartete_laenge = b'\x00\x00\x00\x0D'
    laenge = bytes_lesen(byte_reader, 4)

    erwarteter_ihdr_string = b"IHDR"
    ihdr_string = bytes_lesen(byte_reader, 4)

    if erwartete_laenge == laenge and erwarteter_ihdr_string == ihdr_string:
        breite = int.from_bytes(bytes_lesen(byte_reader, 4), byteorder=png_byte_order)
        hoehe = int.from_bytes(bytes_lesen(byte_reader, 4), byteorder=png_byte_order)
        bit_tiefe = int.from_bytes(bytes_lesen(byte_reader, 1), byteorder=png_byte_order)
        farb_kanaele = get_anzahl_farb_kananaele(int.from_bytes(bytes_lesen(byte_reader, 1), byteorder=png_byte_order))

        kompressions_methode = bytes_lesen(byte_reader, 1)
        filter_methode = bytes_lesen(byte_reader, 1)
        interlace_methode = bytes_lesen(byte_reader, 1)
        crc = bytes_lesen(byte_reader, 4)

        return breite, hoehe, bit_tiefe, farb_kanaele
    else:
        print("Fehler beim Lesen des Image Header (IHDR)")
        return None


def get_anzahl_farb_kananaele(farbtyp):
    switcher = {
        0: 1,
        2: 3,
        4: 2,
        6: 4
    }
    return switcher.get(farbtyp, 0)


def bytes_lesen(byte_reader, anzahl_bytes):
    result = b''
    for i in range(anzahl_bytes):
        naechstes_byte = byte_reader.read(1)
        result += naechstes_byte
    return result


def berechne_bits(ihdr_werte):
    breite, hoehe, bit_tiefe, farb_kanaele = ihdr_werte
    return breite * hoehe * bit_tiefe * farb_kanaele


if __name__ == '__main__':
    check_png(str(sys.argv[0]))
