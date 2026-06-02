from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from config.custom_permissions import OnlyLoggedSuperUser
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .forms import CommentForm, ContactForm
from .models import Category, News


class HomePageView(TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.select_related('category').order_by('-publish_time')[:8]
        context['local_news'] = News.published.select_related('category').filter(
            category__name='Uzbekistan'
        ).order_by('-publish_time')[:6]
        context['world_news'] = News.published.select_related('category').filter(
            category__name='Jahon'
        ).order_by('-publish_time')[:6]
        context['sport_news'] = News.published.select_related('category').filter(
            category__name='Sport'
        ).order_by('-publish_time')[:6]
        context['techno_news'] = News.published.select_related('category').filter(
            category__name='Fan_texnika'
        ).order_by('-publish_time')[:6]
        context['economy'] = News.published.select_related('category').filter(
            category__name='Iqtisodiyot'
        ).order_by('-publish_time')[:6]
        context['jamiyat'] = News.published.select_related('category').filter(
            category__name='Jamiyat'
        ).order_by('-publish_time')[:4]
        return context


class BaseCategoryView(ListView):
    model = News
    template_name = 'news/category_page.html'
    context_object_name = 'articles'
    category_name = ''
    page_title = ''
    page_description = ''

    def get_queryset(self):
        return News.published.select_related('category').filter(
            category__name=self.category_name
        ).order_by('-publish_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = context['articles']
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['category_name'] = self.category_name
        context['featured_article'] = articles[0] if articles else None
        context['secondary_articles'] = articles[1:5]
        context['more_articles'] = articles[5:]
        context['latest_headlines'] = News.published.select_related('category').exclude(
            category__name=self.category_name
        ).order_by('-publish_time')[:4]
        return context


class LocalNewsView(BaseCategoryView):
    category_name = 'Uzbekistan'
    page_title = "O'zbekiston yangiliklari"
    page_description = "Mamlakat ichidagi eng muhim voqealar, tezkor tafsilotlar va tahliliy materiallar."


class WorldNewsView(BaseCategoryView):
    category_name = 'Jahon'
    page_title = 'Jahon yangiliklari'
    page_description = "Dunyo bo'ylab eng dolzarb mavzularni qisqa, aniq va o'qishga qulay formatda kuzating."


class SubjectNewsView(BaseCategoryView):
    category_name = 'Fan_texnika'
    page_title = 'Fan va texnika'
    page_description = "Texnologiya, innovatsiya va ilm-fandagi yangi yo'nalishlarni soddalashtirilgan usulda o'qing."


class SportNewsView(BaseCategoryView):
    category_name = 'Sport'
    page_title = 'Sport yangiliklari'
    page_description = "Musobaqalar, transferlar va sport olamidagi muhim voqealarni zamonaviy formatda kuzating."


class IqtisodiyotNewsView(BaseCategoryView):
    category_name = 'Iqtisodiyot'
    page_title = 'Iqtisodiyot sharhi'
    page_description = "Bozor, biznes va moliyadagi o'zgarishlarni tartibli va tushunarli ko'rinishda toping."


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'news/contact.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'news/contact.html', {'form': ContactForm(), 'success': True})
        return render(request, 'news/contact.html', {'form': form})


class NewsUpdtaeView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news_edit.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('homepage')


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('homepage')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = (
        'title', 'title_uz', 'title_en', 'title_ru',
        'slug',
        'body', 'body_uz', 'body_en', 'body_ru',
        'image', 'category', 'status',
    )
    success_url = reverse_lazy('homepage')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users,
    }
    return render(request, 'pages/admin_page.html', context)


def news_detail(request, news):
    article = get_object_or_404(News, slug=news, status=News.Status.PUBLISHED)

    # Hitcount (ko'rishlar soni)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(article)
    hits = hit_count.hits
    hitcontext = context['hit_count'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = article.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = article
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context.update({
        'recomend_news': News.published.select_related('category').exclude(
            pk=article.pk
        ).order_by('-publish_time')[:5],
        'news': article,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments_count': comments_count,
    })
    return render(request, 'news/single.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'news/no_results.html', {'query': query})

    results = News.published.select_related('category').filter(
        Q(title__icontains=query) | Q(body__icontains=query)
    ).distinct()

    if not results.exists():
        return render(request, 'news/no_results.html', {'query': query})

    return render(request, 'news/search_results.html', {'all_news': results, 'query': query})
