from flask import request

def runflow(dataDariForm):
    total = 0
    details = []

    for key, val in dataDariForm.items():
        # Coba ubah ke float, kalau gagal di-skip
        try:
            num = float(val)
            total += num
            details.append(f"{key}={num}")
        except (ValueError, TypeError):
            # bukan angka, diabaikan (atau kamu bisa simpan di dict lain)
            continue

    detail_str = ", ".join(details)
    return f'ini hasil dari model_dua --> {total} (detail: {detail_str})'
