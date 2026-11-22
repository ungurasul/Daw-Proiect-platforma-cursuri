# Lista de prezentare

## Laboratorul 1

| Cerință | Unde se găsește |
|---|---|
| Tema și descrierea platformei | `cursora/views.py`, funcția `index`; `cursora/templates/cursora/index.html` |
| Pagina `/info`, titlu și data/ora în română | `cursora/urls.py`, `cursora/views.py`, `cursora/templates/cursora/info.html` |
| Clasa `Accesare`, ID, IP, URL, parametri și dată | `cursora/views.py`, clasa `Accesare` |
| IP prin middleware și jurnalizarea cererii | `cursora/middleware.py`, `config/settings.py` |
| Parametrii `data=zi` și `data=timp` | `cursora/views.py`, funcția `info` |

## Laboratorul 2

### Task 1: jurnalul accesărilor

| Cerință | Unde se găsește |
|---|---|
| Lista accesărilor și parametrul `ultimele` | `cursora/views.py`, funcția `log`; `cursora/templates/cursora/log.html` |
| `accesari=nr` și `accesari=detalii` | `cursora/views.py`, funcția `log`; `log.html` |
| `iduri`, valori repetate și `dubluri=true` | `cursora/views.py`, funcția `log` |
| Parametrii primiți și tabelul `tabel=tot` sau cu coloane alese | `cursora/views.py`, funcția `log`; `log.html` |
| Paginile cel mai puțin și cel mai mult accesate | `cursora/views.py`, funcția `log`; `log.html` |
| Detaliile unei accesări și ruta `re_path` | `cursora/urls.py`, `cursora/views.py`, `detalii_accesare.html` |

### Task 2: pagini și șabloane

| Cerință | Unde se găsește |
|---|---|
| Pagina principală cu cinci secțiuni și imagine | `cursora/templates/cursora/index.html`; imaginile în `cursora/static/cursora/images/` |
| Pagina Despre cu două secțiuni și imagine | `cursora/templates/cursora/despre.html` |
| Șablon comun cu header, main și footer | `cursora/templates/cursora/baza.html` |
| Meniu derulant, linkuri Django și ancore | `baza.html`, `cursora/static/cursora/css/nav.css` |
| Pagini în lucru | `cursora/urls.py`, funcția `in_lucru`, `in_lucru.html` |
| IP și datele firmei în footer | `cursora/middleware.py`, `cursora/context_processors.py`, `config/settings.py`, `baza.html` |

### Task 3: diagrama bazei de date

| Cerință | Unde se găsește |
|---|---|
| Diagrama editabilă și exportată | `docs/DiagramaER.drawio`, `docs/DiagramaER.png` |
| Descrierea entităților și relațiilor | Documentația Word predată separat, secțiunile „Entități” și „Relații între entități” |
| Lista câmpurilor din implementare | Secțiunea „Schema pentru diagrama ER” de mai jos; `cursora/models.py` |

## Laboratorul 3

### Task 1: modele și restricții

| Cerință | Unde se găsește |
|---|---|
| Cele cinci modele și relațiile | `cursora/models.py`: `Profesor`, `Categorie`, `Competenta`, `Curs`, `Lectie` |
| Câmpuri nullable, unice, EmailField, URLField, SlugField și ordonare | Câmpurile modelelor și clasele `Meta` din `cursora/models.py` |
| Choices și valori implicite | `NivelCurs` și câmpurile modelelor din `cursora/models.py` |
| `help_text`, date de adăugare și mesaje de eroare | Câmpurile modelelor din `cursora/models.py` |
| Constrângeri `Q`, indexuri, vector și fișier | Clasele `Meta`, `limbi_disponibile` și `imagine` din `cursora/models.py` |
| Migrarea inițială | `cursora/migrations/0001_initial.py` |

Verificare în cod: 10 câmpuri nullable, 10 câmpuri cu unicitate incluzând cheile primare, 1 câmp cu choices, 10 valori implicite, 16 câmpuri cu `help_text`, 4 câmpuri `DateTimeField` cu `auto_now_add`, 11 câmpuri cu mesaje personalizate în `error_messages`, 9 constrângeri `Q`, 7 indexuri și 1 `FileField`.

### Task 2: PostgreSQL și Django Admin

| Cerință | Unde se găsește |
|---|---|
| Rolul și baza PostgreSQL | `creare_user.sql`, `configurare_baza.ps1`, `config/settings.py` |
| Migrarea bazei | `cursora/migrations/0001_initial.py`; comanda `python manage.py migrate` |
| Superuser și autentificare | `/admin/`; contul este local, nu este salvat în repository |
| Modele înregistrate și listări Admin | `cursora/admin.py` |
| Date introduse prin Admin | PostgreSQL: 5 profesori, 5 categorii, 5 competențe, 10 cursuri și 5 lecții |

### Task 3: GitHub

Repository: https://github.com/ungurasul/Daw-Proiect-platforma-cursuri
Se folosește un commit distinct pentru fiecare etapă ulterioară. Adaugă linkul repository-ului în tabelul de activitate.

## Schema pentru diagrama ER

### PROFESOR

`id` (PK), `nume`, `prenume`, `email`, `telefon`, `specializare`, `prezentare`, `website`, `data_adaugarii`, `activ`.

### CATEGORIE

`id` (PK), `nume`, `slug`, `descriere`, `culoare`, `sigla`, `ordine`, `data_adaugarii`, `activa`.

### CURS

`id` (PK), `profesor_id` (FK), `categorie_id` (FK), `titlu`, `slug`, `descriere`, `sumar`, `pret`, `nivel`, `durata_ore`, `limbi_disponibile` (vector), `imagine`, `data_publicarii`, `activ`.

### LECTIE

`id` (PK Django), `curs_id` (FK), `ordine` (unica în curs), `titlu`, `durata_minute`, `gratuita`, `descriere`, `video_url`, `data_adaugarii`. Lecția depinde de curs și se șterge odată cu acesta. Perechea (`curs_id`, `ordine`) o identifică în curs.

### COMPETENȚĂ

`id` (PK), `nume`, `descriere`, `domeniu`.

În proiect sunt folosite atribute text, numere întregi și zecimale, niveluri prestabilite, valori logice, date și ore, un vector și un fișier.

### Relații

- PROFESOR 1:N CURS.
- CATEGORIE 1:N CURS.
- CURS 1:N LECȚIE.
- CURS M:N COMPETENȚĂ. Django creează tabelul intermediar pentru această relație.

## Datele firmei

Valorile din footer se modifică în dicționarul `DATE_FIRMA` din `config/settings.py`. Afișarea este în `cursora/templates/cursora/baza.html`, prin `cursora/context_processors.py`.

## Înainte de predare

- Încarcă documentația ca Google Doc, activează accesul prin link și adaugă linkul în tabelul de activitate, conform laboratorului 1.
- Diagrama editabilă și exportul PNG sunt în folderul `docs/`. Imaginea este inclusă în documentația Word predată separat.
- Adaugă linkul repository-ului în tabelul de activitate, conform laboratorului 1.
