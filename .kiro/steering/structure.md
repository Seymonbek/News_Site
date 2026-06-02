# Project Structure

```
News_Site/
├── config/                  # Django project config
│   ├── settings.py          # Settings (uses python-decouple for .env)
│   ├── urls.py              # Root URL config (i18n_patterns)
│   ├── wsgi.py
│   ├── asgi.py
│   └── custom_permissions.py  # OnlyLoggedSuperUser mixin
│
├── app/                     # Main news app
│   ├── models.py            # News, Category, Comment, Contact, ContactData
│   ├── views.py             # All news views (CBV + FBV)
│   ├── urls.py              # News URL patterns
│   ├── admin.py             # Admin registrations
│   ├── forms.py             # ContactForm, CommentForm
│   ├── translation.py       # modeltranslation config
│   └── contect_prossesor.py # lasted_news context processor
│
├── accounts/                # User accounts app
│   ├── models.py            # Profile model
│   ├── views.py             # dashboard, user_register, EditUserView
│   ├── urls.py              # Auth URL patterns
│   ├── forms.py             # UserRegistrationForm, ProfileEditForm, UserEditForm
│   └── translation.py       # (empty)
│
├── templates/
│   ├── news/                # Main templates
│   │   ├── base.html        # Site shell: ticker, topbar, brand, nav, footer
│   │   ├── index.html       # Homepage
│   │   ├── single.html      # Article detail
│   │   ├── category_page.html  # Generic category (used by all 5 categories)
│   │   ├── contact.html
│   │   ├── search_results.html
│   │   ├── no_results.html
│   │   └── 404.html
│   ├── account/             # Registration/profile templates
│   │   ├── register.html
│   │   ├── register_done.html
│   │   └── profile_edit.html
│   ├── crud/                # Superuser CRUD templates
│   │   ├── news_create.html
│   │   ├── news_edit.html
│   │   └── news_delete.html
│   ├── pages/               # Misc pages
│   │   ├── user_profile.html
│   │   └── admin_page.html
│   └── registration/        # Django auth templates
│       ├── login.html
│       ├── logged_out.html
│       ├── password_*.html
│       └── password_reset_email.html
│
├── static/
│   ├── css/
│   │   ├── news.css         # PRIMARY: full custom news site CSS (bn-* classes)
│   │   ├── style.css        # Legacy Bootstrap 4 (kept for compatibility)
│   │   └── redesign.css     # Legacy redesign (kept for compatibility)
│   ├── js/
│   │   └── main.js          # Theme toggle, back-to-top, jQuery plugins
│   ├── img/                 # Static images
│   └── lib/                 # owlcarousel, easing
│
├── media/                   # User uploaded files
│   └── news/images/         # News article images
│
├── locale/                  # Translation files
│   ├── en/LC_MESSAGES/      # English translations
│   └── ru/LC_MESSAGES/      # Russian translations
│
├── .env                     # Secret config (NOT in git)
├── .env.example             # Template for .env
├── requirements.txt         # Python dependencies
├── manage.py
└── deploy.md                # Server deployment guide
```

## CSS Naming Convention
All new CSS uses `bn-` prefix (BizNews):
- `bn-container` — main container
- `bn-card-feature` — big featured article card
- `bn-card-v` — vertical stacked card
- `bn-card-h` — horizontal compact card
- `bn-layout` — 2-column content + sidebar layout
- `bn-widget` — sidebar widget
- `bn-btn` — buttons (bn-btn--primary, --secondary, --outline)
- `bn-form`, `bn-field` — form elements
- `bn-article` — article detail page

## URL Structure
All URLs are under `i18n_patterns` → prefixed with `/uz/`, `/ru/`, `/en/`

| Name | URL | View |
|---|---|---|
| homepage | `/uz/` | HomePageView |
| news_detail_page | `/uz/news/<slug>/` | news_detail |
| news_create | `/uz/news/create/` | NewsCreateView |
| news_update | `/uz/news/<slug>/edit/` | NewsUpdtaeView |
| news_delete | `/uz/news/<slug>/delete/` | NewsDeleteView |
| Uzbekistan | `/uz/Uzbekistan/` | LocalNewsView |
| Jahon | `/uz/Jahon/` | WorldNewsView |
| Sport | `/uz/Sport/` | SportNewsView |
| Fan_texnika | `/uz/Fan_texnika/` | SubjectNewsView |
| Iqtisodiyot | `/uz/Iqtisodiyot/` | IqtisodiyotNewsView |
| search_results | `/uz/searchresult/` | search_view |
| contact-us | `/uz/contact/` | ContactPageView |
