

class PageNotFound404:
    def __call__(self, request):
        return 'Page not found (404)'


class Framework:

    """Основной класс фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # Получаем адрес запроса
        path: str = environ['PATH_INFO']

        # Добавляем слэш в конец адреса, если его нет
        if not path.endswith('/'):
            path = f'{path}/'

        # Находим нужный контроллер
        # Обработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        request = {}
        for front in self.fronts_lst:
            front(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
