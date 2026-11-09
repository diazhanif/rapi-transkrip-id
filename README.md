# rapi-transkrip-id

CLI kecil untuk membersihkan kata jeda yang umum dari transkrip Bahasa Indonesia, misalnya keluaran Whisper atau layanan speech-to-text lainnya. Program berjalan lokal dan mengeluarkan teks bersih ke stdout agar mudah diteruskan ke editor atau pipeline.

## Contoh

```sh
cat transkrip.txt | rapi-transkrip-id --stats
```

Input:

```text
Eee, saya em mau anu menjelaskan ini.
```

Output:

```text
saya mau menjelaskan ini.
```

Statistik penghapusan ditulis ke stderr agar hasil stdout tetap bisa dipipe ke file atau program lain.

## Pemakaian sebagai library

```python
from rapi_transkrip import clean_transcript

teks, hitungan = clean_transcript("Eee saya anu setuju.")
# teks == "saya setuju."
# hitungan == {"anu": 1, "eee": 1}
```

Instalasi (Python 3.9+):

```sh
python -m pip install .
```

Atau tanpa instalasi perintah:

```sh
cat transkrip.txt | python -m rapi_transkrip
```

## Batasan dan privasi

Secara default hanya token mandiri `eee` (dan variasi huruf `e` yang lebih panjang), `em`/`emm`, serta `anu` yang dihapus. Interjeksi seperti `eh` dan `hmm` sengaja dipertahankan karena bisa bermakna. Program tidak menebak tanda baca, mengubah susunan kalimat, atau memperbaiki tata bahasa; periksa hasil sebelum dipublikasikan karena kata jeda tertentu mungkin bermakna dalam konteks.

Tidak ada API, telemetri, atau dependensi runtime. Teks dibaca dari stdin dan tidak dikirim ke jaringan.

## Tes

```sh
python -m unittest discover -s tests -v
```

## Lisensi

MIT. Lihat [LICENSE](LICENSE).
