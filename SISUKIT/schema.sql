DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS surat_sakit;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE surat_sakit(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npm INTEGER NOT NULL,
    nama_mahasiswa TEXT NOT NULL,
    tanggal_upload DATE NOT NULL,
    surat_sakit_mahasiswa TEXT NOT NULL,
    status_surat_sakit TEXT NOT NULL,
    nama_penyakit TEXT,
    tanggal_izin DATE,
    daftar_mata_kuliah_izin TEXT,
    daftar_dosen TEXT,
    disetujui_oleh TEXT,
    ditolak_oleh TEXT,
    tanggal_pengubahan_status DATE NOT NULL 
);