from datetime import datetime


def header_context(request):
    menu = [
        {"title": "Главная", "url_name": "home"},
        {"title": "О сайте", "url_name": "about"},
        # {"title": "Добавить статью", "url_name": "#"},
        # {"title": "Обратная связь", "url_name": "#"},
        # {"title": "Войти", "url_name": "#"},
    ]
    return {"menu": menu}


def this_year(request):
    return {"year": datetime.now().year}
