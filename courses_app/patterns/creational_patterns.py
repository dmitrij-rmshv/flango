import copy
import quopri
from re import S
from courses_app.patterns.behavioral_patterns import Subject, ConsoleWriter, FileWriter
from courses_app.patterns.architectural_system_pattern_unit_of_work import DomainObject


class User:

    def __init__(self, name):
        self.name = name


class Professor(User):
    pass


class Learner(User, DomainObject):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {'teacher': Professor, 'student': Learner}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class CourseProto:

    def clone(self):
        return copy.deepcopy(self)


class Course(CourseProto, Subject, DomainObject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Learner):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class VebinarCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category(DomainObject):
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
        self.learners = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        # return UserFactory.create(name, category)
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

    def get_learner(self, name) -> Learner:
        for item in self.learners:
            if item.name == name:
                return item

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

    # def __init__(self, name, writer=FileWriter('logfile.log')):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    # @staticmethod
    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
