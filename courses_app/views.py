from flango_framework.template_engine import linkage
from courses_app.patterns.creational_patterns import Engine, Logger
from courses_app.patterns.structural_patterns import FlaskRoute

site = Engine()
logger = Logger('main')

routes = {}


@FlaskRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', linkage('index.html', objects_list=site.categories)


@FlaskRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', linkage('about.html')


@FlaskRoute(routes=routes, url='/blog/')
class Blog:
    def __call__(self, request):
        return '200 OK', linkage('blog.html')


@FlaskRoute(routes=routes, url='/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', linkage('contacts.html', phone_1=request.get('phone_1', None), phone_2=request.get('phone_2', None))


@FlaskRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', linkage('course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Пока нет курсов'


@FlaskRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)
            logger.log(f'Создание курса {name}')

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', linkage('course_list.html', objects_list=category.courses,
                                     name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', linkage('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@FlaskRoute(routes=routes, url='/create-category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)
            logger.log(f'Создание категории {name}')

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', linkage('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', linkage('create_category.html', categories=categories)


@FlaskRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', linkage('category_list.html', objects_list=site.categories)


@FlaskRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', linkage('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
