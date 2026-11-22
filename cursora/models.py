from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class NivelCurs(models.TextChoices):
    INCEPATOR = 'incepator', 'Începător'
    MEDIU = 'mediu', 'Mediu'
    AVANSAT = 'avansat', 'Avansat'


class Profesor(models.Model):
    nume = models.CharField(
        'nume', max_length=80,
        error_messages={'max_length': 'Numele poate avea cel mult 80 de caractere.'},
    )
    prenume = models.CharField(
        'prenume', max_length=80,
        error_messages={'max_length': 'Prenumele poate avea cel mult 80 de caractere.'},
    )
    email = models.EmailField(
        'email', unique=True,
        error_messages={'unique': 'Există deja un profesor cu această adresă de email.'},
    )
    telefon = models.CharField('telefon', max_length=25, null=True, blank=True)
    specializare = models.CharField(
        'specializare', max_length=120,
        help_text='Domeniul principal în care predă profesorul.',
    )
    prezentare = models.TextField(
        'prezentare', null=True, blank=True,
        help_text='Scurtă biografie afișată în pagina profesorului.',
    )
    website = models.URLField(
        'website', null=True, blank=True,
        help_text='Adresă web opțională către portofoliul profesorului.',
    )
    data_adaugarii = models.DateTimeField('data adăugării', auto_now_add=True)
    activ = models.BooleanField('activ', default=True)

    class Meta:
        verbose_name = 'profesor'
        verbose_name_plural = 'profesori'
        ordering = ['nume', 'prenume']
        constraints = [
            models.CheckConstraint(
                condition=Q(nume__regex=r'\S') & Q(prenume__regex=r'\S'),
                name='profesor_nume_nevid',
                violation_error_message='Numele și prenumele profesorului nu pot fi goale.',
            ),
        ]
        indexes = [models.Index(fields=['nume'], name='profesor_nume_idx')]

    def __str__(self):
        return f'{self.nume} {self.prenume}'


class Categorie(models.Model):
    nume = models.CharField(
        'nume', max_length=100, unique=True,
        error_messages={'unique': 'Există deja o categorie cu acest nume.'},
    )
    slug = models.SlugField(
        'slug', max_length=110, unique=True,
        error_messages={'unique': 'Acest identificator de categorie este deja folosit.'},
    )
    descriere = models.TextField(
        'descriere', null=True, blank=True,
        help_text='Explică ce tipuri de cursuri sunt incluse în categorie.',
    )
    culoare = models.CharField(
        'culoare', max_length=7, default='#4472C4',
        help_text='Culoare reprezentativă în format hexadecimal, de exemplu #4472C4.',
        error_messages={'max_length': 'Culoarea trebuie să aibă cel mult 7 caractere.'},
    )
    sigla = models.CharField(
        'siglă', max_length=255, null=True, blank=True,
        help_text='Cale către o imagine sau numele unei pictograme.',
    )
    ordine = models.PositiveSmallIntegerField('ordine de afișare', default=0)
    data_adaugarii = models.DateTimeField('data adăugării', auto_now_add=True)
    activa = models.BooleanField('activă', default=True)

    class Meta:
        verbose_name = 'categorie'
        verbose_name_plural = 'categorii'
        ordering = ['ordine', 'nume']
        constraints = [
            models.CheckConstraint(
                condition=Q(ordine__gte=0),
                name='categorie_ordine_nenegativa',
                violation_error_message='Ordinea de afișare trebuie să fie zero sau pozitivă.',
            ),
            models.CheckConstraint(
                condition=Q(culoare__regex=r'^#[0-9A-Fa-f]{6}$'),
                name='categorie_culoare_hex',
                violation_error_message='Culoarea trebuie să respecte formatul #RRGGBB.',
            ),
        ]
        indexes = [models.Index(fields=['ordine', 'nume'], name='categorie_ordine_nume_idx')]

    def __str__(self):
        return self.nume


class Competenta(models.Model):
    nume = models.CharField(
        'nume', max_length=100, unique=True,
        error_messages={'unique': 'Există deja o competență cu acest nume.'},
    )
    descriere = models.TextField(
        'descriere', null=True, blank=True,
        help_text='Descrie abilitatea concretă pe care o dezvoltă cursantul.',
    )
    domeniu = models.CharField('domeniu', max_length=100)

    class Meta:
        verbose_name = 'competență'
        verbose_name_plural = 'competențe'
        ordering = ['nume']
        constraints = [
            models.CheckConstraint(
                condition=Q(nume__regex=r'\S') & Q(domeniu__regex=r'\S'),
                name='competenta_nume_domeniu_nevide',
                violation_error_message='Numele și domeniul competenței sunt obligatorii.',
            ),
        ]
        indexes = [models.Index(fields=['domeniu'], name='competenta_domeniu_idx')]

    def __str__(self):
        return self.nume


class Curs(models.Model):
    profesor = models.ForeignKey(
        Profesor, on_delete=models.PROTECT, related_name='cursuri', verbose_name='profesor',
        help_text='Profesorul care a creat și susține cursul.',
    )
    categorie = models.ForeignKey(
        Categorie, on_delete=models.PROTECT, related_name='cursuri', verbose_name='categorie',
        help_text='Categoria folosită pentru organizarea și filtrarea cursurilor.',
    )
    titlu = models.CharField(
        'titlu', max_length=150,
        error_messages={'max_length': 'Titlul cursului poate avea cel mult 150 de caractere.'},
    )
    slug = models.SlugField(
        'slug', max_length=160, unique=True,
        error_messages={'unique': 'Acest identificator de curs este deja folosit.'},
    )
    descriere = models.TextField('descriere')
    sumar = models.CharField(
        'sumar', max_length=240, null=True, blank=True,
        help_text='Rezumatul scurt folosit în catalog.',
    )
    pret = models.DecimalField(
        'preț', max_digits=8, decimal_places=2, default=0,
        validators=[MinValueValidator(0, message='Prețul nu poate fi negativ.')],
        help_text='Prețul final în lei.',
        error_messages={'max_digits': 'Prețul nu poate depăși 8 cifre în total.'},
    )
    nivel = models.CharField(
        'nivel', max_length=20, choices=NivelCurs.choices, default=NivelCurs.INCEPATOR,
        help_text='Alege nivelul necesar pentru parcurgerea cursului.',
    )
    durata_ore = models.PositiveSmallIntegerField(
        'durată în ore', default=1,
        validators=[MinValueValidator(1, message='Durata trebuie să fie de cel puțin o oră.')],
    )
    limbi_disponibile = ArrayField(
        models.CharField(max_length=5),
        verbose_name='limbi disponibile', default=list, blank=True,
        help_text='Listă de coduri de limbă, de exemplu ["ro", "en"]. Acesta este atributul cu valori multiple.',
    )
    imagine = models.FileField(
        'imagine', upload_to='cursuri/', null=True, blank=True,
        help_text='Imaginea de copertă a cursului.',
    )
    data_publicarii = models.DateTimeField('data publicării', auto_now_add=True)
    activ = models.BooleanField('activ', default=True)
    competente = models.ManyToManyField(
        Competenta, related_name='cursuri', blank=True, verbose_name='competențe',
    )

    class Meta:
        verbose_name = 'curs'
        verbose_name_plural = 'cursuri'
        ordering = ['titlu']
        constraints = [
            models.CheckConstraint(
                condition=Q(pret__gte=0),
                name='curs_pret_nenegativ',
                violation_error_message='Prețul cursului trebuie să fie zero sau pozitiv.',
            ),
            models.CheckConstraint(
                condition=Q(durata_ore__gte=1),
                name='curs_durata_minima',
                violation_error_message='Durata cursului trebuie să fie de cel puțin o oră.',
            ),
            models.CheckConstraint(
                condition=Q(nivel__in=NivelCurs.values),
                name='curs_nivel_valid',
                violation_error_message='Nivelul cursului nu este valid.',
            ),
        ]
        indexes = [
            models.Index(fields=['nivel'], name='curs_nivel_idx'),
            models.Index(fields=['pret'], name='curs_pret_idx'),
            models.Index(fields=['activ'], name='curs_activ_idx'),
            models.Index(fields=['data_publicarii'], name='curs_publicare_idx'),
        ]

    def __str__(self):
        return self.titlu


class Lectie(models.Model):
    curs = models.ForeignKey(
        Curs, on_delete=models.CASCADE, related_name='lectii', verbose_name='curs',
        help_text='Lecția este dependentă de cursul căruia îi aparține.',
    )
    ordine = models.PositiveSmallIntegerField(
        'număr de ordine',
        validators=[MinValueValidator(1, message='Ordinea trebuie să fie cel puțin 1.')],
        help_text='Împreună cu cursul identifică lecția în cadrul cursului.',
    )
    titlu = models.CharField(
        'titlu', max_length=150,
        error_messages={'max_length': 'Titlul lecției poate avea cel mult 150 de caractere.'},
    )
    durata_minute = models.PositiveSmallIntegerField(
        'durată în minute',
        validators=[MinValueValidator(1, message='Durata trebuie să fie de cel puțin un minut.')],
    )
    gratuita = models.BooleanField('lecție gratuită', default=False)
    descriere = models.TextField('descriere', null=True, blank=True)
    video_url = models.URLField('adresă video', null=True, blank=True)
    data_adaugarii = models.DateTimeField('data adăugării', auto_now_add=True)

    class Meta:
        verbose_name = 'lecție'
        verbose_name_plural = 'lecții'
        ordering = ['curs', 'ordine']
        constraints = [
            models.UniqueConstraint(
                fields=['curs', 'ordine'], name='lectie_unica_in_curs',
                violation_error_message='Un curs nu poate avea două lecții cu aceeași ordine.',
            ),
            models.CheckConstraint(
                condition=Q(ordine__gte=1),
                name='lectie_ordine_pozitiva',
                violation_error_message='Ordinea lecției trebuie să fie cel puțin 1.',
            ),
            models.CheckConstraint(
                condition=Q(durata_minute__gte=1),
                name='lectie_durata_pozitiva',
                violation_error_message='Durata lecției trebuie să fie pozitivă.',
            ),
        ]

    def __str__(self):
        return f'{self.curs.titlu} - {self.ordine}. {self.titlu}'
