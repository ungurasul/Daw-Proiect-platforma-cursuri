from collections import Counter
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html


ZILE_RO = (
    'Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică'
)
LUNI_RO = (
    'Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
    'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'
)


def client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR', 'necunoscut')


class Accesare:
    accesari = []
    ultimul_id = 0

    def __init__(self, request):
        type(self).ultimul_id += 1
        self.id = type(self).ultimul_id
        self.ip_client = getattr(request, 'client_ip', client_ip(request))
        self.url = request.build_absolute_uri()
        self.cale = request.path
        self.parametri = {
            nume: valori[0] if len(valori) == 1 else valori
            for nume in request.GET
            for valori in [request.GET.getlist(nume)]
        }
        self.data = timezone.now()
        type(self).accesari.append(self)

    def lista_parametri(self):
        return [
            (nume, valoare if valoare != '' else None)
            for nume, valoare in self.parametri.items()
        ]

    def string_url(self):
        return self.url

    def pagina(self):
        return self.cale.rstrip('/') or '/'

    def calculeaza_data(self, format='%A, {day} %B %Y', mod=''):
        moment = timezone.localtime(self.data)
        if mod == 'zi':
            rezultat = f'{moment.day} {LUNI_RO[moment.month - 1]} {moment.year}'
            return format_html('<section><h2>Data și ora</h2><p>{}</p></section>', rezultat)
        if mod == 'timp':
            rezultat = moment.strftime('%H:%M:%S')
            return format_html('<section><h2>Data și ora</h2><p>{}</p></section>', rezultat)

        if format:
            format_localizat = format.replace('{day}', str(moment.day))
            rezultat = moment.strftime(format_localizat)
            rezultat = rezultat.replace(moment.strftime('%A'), ZILE_RO[moment.weekday()])
            rezultat = rezultat.replace(moment.strftime('%B'), LUNI_RO[moment.month - 1])
        return format_html('<section><h2>Data și ora</h2><p>{}, {}</p></section>', rezultat, moment.strftime('%H:%M:%S'))

    def __str__(self):
        return '\n'.join((
            f'id: {self.id}',
            f'ip_client: {self.ip_client}',
            f'string_url: {self.string_url()}',
            f'pagina: {self.pagina()}',
            f'calculeaza_data: {self.calculeaza_data()}',
            f'lista_parametri: {self.lista_parametri()}',
        ))


def index(request):
    return render(request, 'cursora/index.html')


def info(request):
    accesare = getattr(request, 'accesare', None)
    if accesare is None:
        accesare = Accesare(request)
    mod = request.GET.get('data', '')
    data_html = accesare.calculeaza_data(mod=mod)
    return render(request, 'cursora/info.html', {'data_html': data_html})


def despre(request):
    return render(request, 'cursora/despre.html')


def istoric(request):
    return render(request, 'cursora/istoric.html')


def in_lucru(request):
    titluri = {
        'produse': 'Cursuri',
        'contact': 'Contact',
        'cos_virtual': 'Coș virtual',
        'instructori': 'Instructori',
        'intrebari_frecvente': 'Întrebări frecvente',
    }
    nume = getattr(request.resolver_match, 'url_name', '')
    return render(request, 'cursora/in_lucru.html', {'titlu_pagina': titluri.get(nume, 'În lucru')})


def log(request):
    toate_accesarile = list(Accesare.accesari)
    afisate = toate_accesarile
    eroare = ''

    if 'ultimele' in request.GET:
        valoare = request.GET.get('ultimele', '')
        try:
            n = int(valoare)
            if n < 0:
                raise ValueError
        except ValueError:
            eroare = 'Parametrul ultimele trebuie să fie un număr întreg pozitiv sau zero.'
        else:
            if n > len(toate_accesarile):
                eroare = f'Exista doar {len(toate_accesarile)} accesari fata de {n} accesari cerute'
            afisate = toate_accesarile[-n:] if n else []

    if 'iduri' in request.GET:
        iduri = []
        for valoare in request.GET.getlist('iduri'):
            for fragment in valoare.split(','):
                try:
                    id_accesare = int(fragment.strip())
                except ValueError:
                    eroare = f'Id de accesare invalid: {fragment}'
                    continue
                if request.GET.get('dubluri', '').lower() == 'true' or id_accesare not in iduri:
                    iduri.append(id_accesare)
        index = {accesare.id: accesare for accesare in toate_accesarile}
        lipsa = [id_accesare for id_accesare in iduri if id_accesare not in index]
        if lipsa:
            eroare = f'Nu există accesări cu id-urile: {", ".join(map(str, lipsa))}'
        afisate = [index[i] for i in iduri if i in index]

    proprietati = ('id', 'ip_client', 'url', 'pagina', 'data', 'parametri')
    tabel = request.GET.get('tabel', '')
    coloane = list(proprietati) if tabel == 'tot' else [x.strip() for x in tabel.split(',') if x.strip()]
    coloane = [x for x in coloane if x in proprietati]
    randuri = []
    for accesare in afisate:
        valori = {
            'id': accesare.id,
            'ip_client': accesare.ip_client,
            'url': accesare.string_url(),
            'pagina': accesare.pagina(),
            'data': timezone.localtime(accesare.data).strftime('%d.%m.%Y %H:%M:%S'),
            'parametri': accesare.lista_parametri(),
        }
        randuri.append([valori[c] for c in coloane])

    accesari_cu_id = {x.id: x for x in toate_accesarile}
    iduri_pagina = []
    for valoare in request.GET.getlist('iduri'):
        for fragment in valoare.split(','):
            try:
                iduri_pagina.append(int(fragment.strip()))
            except ValueError:
                pass
    accesari_dupa_id = [accesari_cu_id[i] for i in iduri_pagina if i in accesari_cu_id]

    contoare = Counter(accesare.pagina() for accesare in toate_accesarile)
    pagini_minime = [pagina for pagina, n in contoare.items() if n == min(contoare.values())] if contoare else []
    pagini_maxime = [pagina for pagina, n in contoare.items() if n == max(contoare.values())] if contoare else []
    parametri = [(nume, request.GET.getlist(nume)) for nume in request.GET]

    return render(request, 'cursora/log.html', {
        'accesari': afisate,
        'nr_accesari': len(toate_accesarile),
        'accesari_nr': request.GET.get('accesari') == 'nr',
        'accesari_detalii': request.GET.get('accesari') == 'detalii',
        'coloane': coloane,
        'randuri': randuri,
        'eroare': eroare,
        'parametri': parametri,
        'nr_parametri': sum(len(valori) for _, valori in parametri),
        'pagini_minime': pagini_minime,
        'pagini_maxime': pagini_maxime,
        'iduri_link': accesari_dupa_id,
    })


def detalii_accesare(request, accesare_id):
    accesare_id = int(accesare_id)
    accesare = next((x for x in Accesare.accesari if x.id == accesare_id), None)
    if accesare is None:
        return HttpResponseNotFound('Nu există accesarea cerută în sesiunea curentă a serverului.')
    return render(request, 'cursora/detalii_accesare.html', {'accesare': accesare})
