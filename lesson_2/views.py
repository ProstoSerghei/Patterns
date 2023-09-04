from simba_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('get', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'
