# Cursora

Platformă Django pentru prezentarea și vânzarea cursurilor digitale.

## Conținut

- `config/`: configurarea proiectului Django.
- `cursora/`: pagini, modele, administrare și fișiere statice.
- `creare_user.sql`: comenzi pentru rolul și baza de date PostgreSQL.
- `configurare_baza.ps1`: pornirea instanței PostgreSQL locale folosite la dezvoltare.
- `docs/DiagramaER.drawio`: diagrama editabilă.
- `docs/DiagramaER.png`: exportul diagramei.
- `Lista_prezentare.md`: corespondența dintre cerințele laboratoarelor 1–3 și fișierele proiectului.

Documentația Word se predă separat, conform cerințelor cursului.

## Instalare locală

Sunt necesare Python și PostgreSQL. Fișierul `configurare_baza.ps1` este pregătit pentru clusterul PostgreSQL local folosit la dezvoltare. Pentru alt calculator, configurează PostgreSQL și variabilele `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` și `POSTGRES_PORT`.

În PowerShell, din folderul care conține `manage.py`:

```powershell
python -m pip install -r requirements.txt
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\configurare_baza.ps1
python manage.py migrate
python manage.py runserver
```

Scriptul local pornește PostgreSQL și creează o cheie `DJANGO_SECRET_KEY` în `.env`. Acest fișier este ignorat de Git.

Site: `http://127.0.0.1:8000/`  
Admin: `http://127.0.0.1:8000/admin/`

Creează un superuser cu `python manage.py createsuperuser` dacă baza de date nu are deja unul.