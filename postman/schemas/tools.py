from pydantic import BaseModel, validator


def wrap_schema_class(name):
    def wrapper(class_input):
        class_input.__name__ = name
        if class_input.__config__:
            class_input.__config__.title = name

        return class_input

    return wrapper


# Pydantic model generation from tortoise-orm
# does not work well with Enum type
# https://github.com/tortoise/tortoise-orm/issues/576
# TODO: Update this code section whith tortoise-orm 0.18.2 release
def fix_enum_validation(EnumType, field_name):
    def wrapper(class_input):
        @validator(field_name, check_fields=False, allow_reuse=True)
        def validation_method(cls, v):
            accepted_values = [m.value for m in EnumType]
            if v and v not in accepted_values:
                raise ValueError(
                    "%s must be on of %r" % (field_name, accepted_values)
                )
            return v

        FixEnumValidation = type(
            "FixEnumValidation",
            (BaseModel,),
            {f"{field_name}_enum_validation": validation_method},
        )

        return type(class_input.__name__, (class_input, FixEnumValidation), {})

    return wrapper
