from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_scope_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main', False):
                main_scope_count += 1
        if main_scope_count == 0:
            raise ValidationError('Укажите основной раздел')
        elif main_scope_count != 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
