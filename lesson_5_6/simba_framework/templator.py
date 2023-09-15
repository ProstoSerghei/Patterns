from os.path import join

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    file_path = join(folder, template_name)

    # Открываем шаблон по имени
    env = Environment()

    env.loader = FileSystemLoader(folder)

    template = env.get_template(template_name)

    # рендерим шаблон с параметрами
    return template.render(**kwargs)
