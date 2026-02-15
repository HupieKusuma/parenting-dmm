import gspread
from google.oauth2.service_account import Credentials
import time


_CACHE = {}
_CACHE_TTL = 60  



# Google Sheets Client

def get_client():
    try:
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.readonly",
            ],
        )
        return gspread.authorize(creds)
    except Exception as e:
        print("Sheets init error:", e)
        return None

def _get_cache(key):
    data = _CACHE.get(key)
    if not data:
        return None

    value, timestamp = data
    if time.time() - timestamp > _CACHE_TTL:
        del _CACHE[key]
        return None

    return value


def _set_cache(key, value):
    _CACHE[key] = (value, time.time())



# to be used

# def get_child_stats(student_id: int):
#     try:
#         creds = Credentials.from_service_account_file(
#             "credentials.json",
#             scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
#         )
#         client = gspread.authorize(creds)
#         sheet = client.open("Child Performance").sheet1

#         for row in sheet.get_all_records():
#             if int(row["student_id"]) == int(student_id):
#                 return row

#     except Exception as e:
#         print("Child stats error:", e)

#     return {
#         "attendance": "N/A",
#         "assignments": "N/A",
#         "average": "N/A",
#     }



# Student Data

def get_student(student_id: int):
    client = get_client()
    if not client:
        return None

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("students").get_all_records()

    for r in rows:
        if int(r["student_id"]) == int(student_id):
            return r

    return None
def get_student_kelas_mustawa(student_id: int):
    client = get_client()
    if not client:
        return None

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("students").get_all_records()

    for r in rows:
        if int(r["student_id"]) == int(student_id):
            return {
                "kelas": r.get("class") or r.get("kelas"),
                "mustawa": r.get("mustawa"),
            }

    return None



# Nilai ujian (to be changed)

def get_exam_scores(student_id: int):
    client = get_client()
    if not client:
        return []

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("exam_scores").get_all_records()

    result = []

    for r in rows:
        sid = str(r.get("student_id", "")).strip()
        if not sid:
            continue  # skip empty rows

        if int(sid) == int(student_id):
            result.append(r)

    return result




# Hafalan

def get_hafalan(student_id: int, month: str):
    cache_key = f"hafalan:{student_id}:{month}"
    cached = _get_cache(cache_key)
    if cached:
        return cached

    client = get_client()
    if not client:
        return []

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("hafalan").get_all_records()

    result = [
        {
            "week": int(r["week"]),
            "surah": r["surah"],
            "ayat_from": int(r["ayat_from"]),
            "ayat_to": int(r["ayat_to"]),
            "status": r["status"],
        }
        for r in rows
        if int(r["student_id"]) == int(student_id)
        and r["month"] == month
    ]

    result = sorted(result, key=lambda x: x["week"])
    _set_cache(cache_key, result)
    return result

def get_highest_hafalan(hafalan_list):
    """
    Returns string like: 'Ali Imran 1–5'
    """
    if not hafalan_list:
        return "-"

   
    h = hafalan_list[-1]
    return f"{h['surah']} {h['ayat_from']}–{h['ayat_to']}"




# Dashboard

def get_parent_dashboard_data(student_id: int, month: str):
    cache_key = f"dashboard:{student_id}:{month}"

    cached = _get_cache(cache_key)
    if cached:
        return cached

    # Fetch fresh data
    student = get_student(student_id)
    scores = get_exam_scores(student_id)
    hafalan = get_hafalan(student_id, month)
    kelas_info = get_student_kelas_mustawa(student_id)
    result = {
        "student": student,
        "scores": scores,
        "hafalan": hafalan,
        "highest_hafalan": get_highest_hafalan(hafalan),
        "kelas": kelas_info["kelas"] if kelas_info else "-",
        "mustawa": kelas_info["mustawa"] if kelas_info else "-",
        
    }

    _set_cache(cache_key, result)
    return result



# login


def check_student_login(student_id: str, password: str):
    client = get_client()
    if not client:
        return None

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("students").get_all_records()

    for r in rows:
        if str(r["student_id"]) == str(student_id):
            # normalize name (optional but recommended)
            if r["name"].strip().lower() == password.strip().lower():
                return r  # login success

    return None


# Silabus Viewer


def get_syllabus_for_student(student_id: int):
    client = get_client()
    if not client:
        return []


    student = get_student(student_id)
    if not student:
        return []

    kelas = (student.get("class") or student.get("kelas") or "").strip()
    if not kelas:
        return []

    sh = client.open("Santri Academic Database")
    rows = sh.worksheet("silabus_jadwal").get_all_records()

    result = []

    for r in rows:
        row_kelas = str(r.get("kelas", "")).strip()
        if not row_kelas:
            continue  

        if row_kelas != kelas:
            continue

        result.append({
            "mapel": r.get("mapel", ""),
            "pengajar": r.get("pengajar", ""),
            "bab": r.get("bab", ""),
            "tanggal": r.get("tanggal_pelaksanaan", ""),
            "status": r.get("status_pelaksanaan", ""),
        })

  
    result.sort(key=lambda x: x["tanggal"] or "")
    return result
