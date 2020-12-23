import ast
import yaml
from string import Template


class CommonTemplate:
    def template(self, yamlName, tp: dict):
        """
        yaml 实现传递变量的方法
        substitute 执行模板替换，返回一个新字符串
        :param yamlName:
        :param tp:
        :return:
        """
        with open(yamlName) as f:
            data = Template(f.read()).substitute(**tp)
            return yaml.safe_load(data)
