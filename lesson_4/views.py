from datetime import date

from simba_framework.templator import render
from patterns.creational_patterns import Engine, Logger


site = Engine()
logger = Logger(name='main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('get', None), objects_list=site.categories)


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('get', None))


class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', date=date.today())


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Страница не найдена'


class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Категории еще не добавлены'


class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'{name} (копия)'
                new_course = old_course.clone()
                new_course.name = new_name
                new_course.category = old_course.category
                new_course.category.courses.append(new_course)
                site.courses.append(new_course)

                return '200 OK', render('course_list.html',
                                        objects_list=new_course.category.courses,
                                        name=new_course.category.name, id=new_course.category.id)
            raise KeyError
        except KeyError:
            return '200 OK', 'No courses have been added yet'
