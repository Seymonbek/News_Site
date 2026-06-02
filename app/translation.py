from modeltranslation.translator import register, TranslationOptions
from .models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


# TUZATILDI: avval ikki class ham "NewsTranslationOptions" deb nomlangan edi
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
