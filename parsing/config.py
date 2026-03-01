BASE_URL = "https://mnogomoloka.ru"

DELAY = 1.5

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

SITE_STRUCTURE = {
    "О компании": {
        "url": "/about/",
        "subsections": {
            "История": "/history/",
            "Миссия и ценности": "/mission/",
            "КСО": "/kso/",
            "Здоровый образ жизни": "/zog/",
            "Забота об окружающей среде": "/timpeallacht/",
            "Сотрудничество с Роскосмос": "/kosmos/"
        }
    },
    "Производство": {
        "url": "/production/",
        "subsections": {
            "Путь молока от фермы до потребителя": "/way/",
            "Технологии": "/technology/",
            "Качество и безопасность": "/quality/"
        }
    },
    "Бренды": {
        "url": "/brands/",
        "type": "brands",
        "subsections": {
            "Свежее Завтра": "/brands/svezhee/",
            "Большая Кружка": "/brands/bolshayakruzhka/",
            "Добрята": "/brands/dobryata/",
            "Сударыня": "/brands/sudarynia/",
            "Тёлушка": "/brands/telushka/"
        }
    },
    "Пресс-центр": {
        "url": "/press/",
        "subsections": {
            "Новости": "/news/",
            "Галерея": "/gallery/",
            "Видео": "/video/"
        }
    },
    "Партнерам": {
        "url": "/partners/",
        "subsections": {
            "Клиентам": "/clients/",
            "Поставщикам": "/providers/"
        }
    },
    "Контакты": {
        "url": "/contacts/",
        "subsections": {
            "Потребителям": "/consumers/",
            "Наши офисы": "/offices/",
            "Журналистам": "/journalists/",
            "Вопрос-ответ": "/questions/",
            "Работа у нас": "/jobs/"
        }
    }
}

OTHER_PAGES = {
    "Дистрибуция": "/distrib/",
    "Экология": "/ecology/",
    "Соглашение": "/agreement/"
}

SPECIAL_SECTIONS = {
    "news": "/news/",
    "video": "/video/"
}