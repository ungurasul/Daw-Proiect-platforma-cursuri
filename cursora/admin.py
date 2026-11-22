from django.contrib import admin

from .models import Categorie, Competenta, Curs, Lectie, Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prenume', 'email', 'specializare', 'activ')
    list_display_links = ('nume', 'prenume')
    list_filter = ('activ', 'specializare')
    search_fields = ('nume', 'prenume', 'email', 'specializare')
    readonly_fields = ('data_adaugarii',)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'culoare', 'ordine', 'activa', 'data_adaugarii')
    list_display_links = ('nume',)
    list_filter = ('activa',)
    search_fields = ('nume', 'descriere')
    prepopulated_fields = {'slug': ('nume',)}
    readonly_fields = ('data_adaugarii',)


@admin.register(Competenta)
class CompetentaAdmin(admin.ModelAdmin):
    list_display = ('nume', 'domeniu', 'numar_cursuri')
    list_display_links = ('nume',)
    search_fields = ('nume', 'domeniu', 'descriere')

    @admin.display(description='Număr cursuri')
    def numar_cursuri(self, obj):
        return obj.cursuri.count()


@admin.register(Curs)
class CursAdmin(admin.ModelAdmin):
    list_display = ('titlu', 'profesor_nume', 'categorie', 'nivel', 'pret', 'activ')
    list_display_links = ('titlu',)
    list_filter = ('activ', 'nivel', 'categorie')
    search_fields = ('titlu', 'descriere', 'profesor__nume', 'profesor__prenume', 'categorie__nume')
    prepopulated_fields = {'slug': ('titlu',)}
    readonly_fields = ('data_publicarii',)
    filter_horizontal = ('competente',)

    @admin.display(description='Profesor', ordering='profesor__nume')
    def profesor_nume(self, obj):
        return obj.profesor


@admin.register(Lectie)
class LectieAdmin(admin.ModelAdmin):
    list_display = ('curs', 'ordine', 'titlu', 'durata_minute', 'gratuita')
    list_display_links = ('titlu',)
    list_filter = ('gratuita', 'curs__categorie')
    search_fields = ('titlu', 'curs__titlu')
    readonly_fields = ('data_adaugarii',)
