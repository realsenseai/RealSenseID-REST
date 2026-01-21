import importlib


# https://stackoverflow.com/a/13808375/4405028
def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


targets = [
    {
        "class": "AlgoFlow",
        "class_snake_name": "algo_flow",
        "target_model_name": "AlgoFlowEnum",
    },
    {
        "class": "CameraRotation",
        "class_snake_name": "camera_rotation",
        "target_model_name": "CameraRotationEnum",
    },
    {
        "class": "SecurityLevel",
        "class_snake_name": "security_level",
        "target_model_name": "SecurityLevelEnum",
    },
    {
        "class": "MatcherConfidenceLevel",
        "class_snake_name": "matcher_confidence_level",
        "target_model_name": "MatcherConfidenceLevelEnum",
    },
    {
        "class": "Status",
        "class_snake_name": "status",
        "target_model_name": "StatusEnum",
    },
    {
        "class": "AuthenticateStatus",
        "class_snake_name": "authenticate_status",
        "target_model_name": "AuthenticateStatusEnum",
    },
    {
        "class": "EnrollStatus",
        "class_snake_name": "enroll_status",
        "target_model_name": "EnrollStatusEnum",
    },
]

rsid_py = "rsid_py"


def generate_models(gen_file_path: str):
    print(f"Generating enum models to {gen_file_path}")
    # fmt: off
    template = (
        """# AUTOMATICALLY GENERATED FILE - DO NOT EDIT
# TO REGENERATE: poe gen
# OR: uv run poe gen
from enum import Enum

from .. import rsid_py


""")
    # fmt: on

    for target in targets:
        class_name = target["class"]
        model_name = target["target_model_name"]
        klass = class_for_name(f"{rsid_py}", class_name)
        print(f"Generating enum for: {klass}")
        template = template + f"class {model_name}(str, Enum):\n"

        indent = 4 * " "
        for member in list(klass.__members__):
            template = template + f"{indent}{member} = '{class_name}.{member}'\n"

        template = template + ("\n" f"{indent}def __str__(self):\n" f"{indent}{indent}return f'{{self.value}}'\n" "\n")

        # to_rsid_py
        template = template + (
            f"{indent}def to_rsid_py(self) -> {rsid_py}.{class_name}:\n" f"{indent}{indent}enum_map = {{}}" "\n"
        )
        for member in list(klass.__members__):
            template = (
                template + f"{indent}{indent}enum_map['{class_name}.{member}'] = {rsid_py}.{class_name}.{member}\n"
            )
        template = template + f"{indent}{indent}return enum_map[self.value]\n" "\n"

        # from_rsid_py
        template = template + (
            f"{indent}@classmethod\n"
            f"{indent}def from_rsid_py(cls, val: {rsid_py}.{class_name}) -> '{model_name}':\n"
            f"{indent}{indent}enum_map = {{}}"
            "\n"
        )
        for member in list(klass.__members__):
            template = template + f"{indent}{indent}enum_map[{rsid_py}.{class_name}.{member}] = {model_name}.{member}\n"
        template = template + f"{indent}{indent}return enum_map[val]\n" "\n"
        template = template + "\n"

    template = template + "\n"
    with open(gen_file_path, "w") as f:
        f.write(template)

    # print(template)
