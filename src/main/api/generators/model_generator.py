import uuid
import rstr
import random
from typing import Any, get_type_hints, get_origin, Annotated, get_args
from src.main.api.generators.creation_rule import CreationRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        # генератор будет проходить по каждому полю и генерировать по правилам. если правила нет, то генерировать по умолчанию т.е str - это по умолчанию, аправило это правило
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {} #это словарь для хранения значений сгенерированных полей

        for filed_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type()

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule and rule.regex:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            elif rule and rule.value_range:
                value=RandomModelGenerator._generate_from_tuple(rule.value_range)
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[filed_name] = value
        print(f"Final data: {init_data}")
        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_from_tuple(value_range: tuple[float, float]) -> float:
        min_value, max_value = value_range
        return round(random.uniform(min_value, max_value), 1)

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None

