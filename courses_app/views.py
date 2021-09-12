from flango_framework.template_engine import linkage
from courses_app.patterns.creational_patterns import Engine, Logger
from courses_app.patterns.structural_patterns import FlaskRoute, Debug
from courses_app.patterns.behavioral_patterns import ListView, CreateView, EmailNotifier, SmsNotifier, BaseSerializer
from courses_app.patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from courses_app.patterns.architectural_system_pattern_mappers import MapperRegistry

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@FlaskRoute(routes=routes, url='/')
class Index:
    @Debug('Index')
    def __call__(self, request):
        return '200 OK', linkage('index.html', objects_list=site.categories)
        # categories = MapperRegistry.get_current_mapper('category').all()
        # print(categories)
        # return '200 OK', linkage('index.html', objects_list=categories)


@FlaskRoute(routes=routes, url='/about/')
class About:
    @Debug('About')
    def __call__(self, request):
        return '200 OK', linkage('about.html')


@FlaskRoute(routes=routes, url='/blog/')
class Blog:
    @Debug('Blog')
    def __call__(self, request):
        return '200 OK', linkage('blog.html')


@FlaskRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug('Contacts')
    def __call__(self, request):
        return '200 OK', linkage('contacts.html', phone_1=request.get('phone_1', None), phone_2=request.get('phone_2', None))


@FlaskRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug('CoursesList')
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

    @Debug('CreateCourse')
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
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

                course.mark_new()
                UnitOfWork.get_current().commit()

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
    @Debug('CreateCategory')
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

            new_category.mark_new()
            UnitOfWork.get_current().commit()

            return '200 OK', linkage('index.html', objects_list=site.categories)
        else:
            # categories = site.categories
            categories = MapperRegistry.get_current_mapper('learner')
            # return '200 OK', linkage('create_category.html', categories=categories)
            return '200 OK', linkage('create_category.html', categories=categories.all())


@FlaskRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug('CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', linkage('category_list.html', objects_list=site.categories)


@FlaskRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug('CopyCourse')
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


@FlaskRoute(routes=routes, url='/learner-list/')
class StudentListView(ListView):
    # queryset = site.learners
    # queryset = MapperRegistry.get_current_mapper('learner').all()
    template_name = 'learner_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('learner')
        return mapper.all()


@FlaskRoute(routes=routes, url='/create-learner/')
class StudentCreateView(CreateView):
    template_name = 'create_learner.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.learners.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@FlaskRoute(routes=routes, url='/add-learner/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_learner.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.learners
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_learner(student_name)
        course.add_student(student)


@FlaskRoute(routes=routes, url='/api/')
class CourseApi:
    def __call__(self, request):
        # print(site.courses)
        return '200 OK', BaseSerializer(site.courses).save()
