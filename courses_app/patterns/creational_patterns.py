import copy
import quopri


class User:
    pass


class Professor(User):
    pass


class Learner(User):
    pass


class UserFactory:
    types = {'teacher': Professor, 'student': Learner}

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class CourseProto:

    def clone(self):
        return copy.deepcopy(self)


class Course(CourseProto):
    def __init__(self, name, category) -> None:
        self.name = name
        self.category = category
        self.category.courses.append(self)


class VebinarCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:
    category_id = 0

    def __init__(self, name, category) -> None:
        self.id = Category.category_id
        Category.category_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    types = {'vebinar': VebinarCourse, 'record': RecordCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Engine:
    def __init__(self) -> None:
        self.professors = []
        self.learner = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)  # ?
            if item.id == id:
                return item
        raise Exception(f'Отсутствует категория id{id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):  # ?
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
