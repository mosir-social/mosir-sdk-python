from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Literal

from graphql import FragmentDefinitionNode, OperationDefinitionNode, parse, print_ast
from graphql.language.visitor import Visitor, visit

ROOT = Path(__file__).resolve().parent.parent
OPERATIONS_PATH = ROOT / "public.operations.graphql"
OPERATIONS_MODULE_PATH = ROOT / "src" / "mosir_sdk" / "_operations.py"


@dataclass(frozen=True)
class OperationInfo:
    operation_name: str
    method_name: str
    operation_type: Literal["query", "mutation", "subscription"]
    document: str
    variable_map: dict[str, str]


def main() -> None:
    document = parse(OPERATIONS_PATH.read_text())
    fragments = {
        definition.name.value: definition
        for definition in document.definitions
        if isinstance(definition, FragmentDefinitionNode)
    }
    operations = [
        build_operation_info(definition, fragments)
        for definition in document.definitions
        if isinstance(definition, OperationDefinitionNode) and definition.name is not None
    ]
    write_operations_module(operations)


def build_operation_info(
    operation: OperationDefinitionNode,
    fragments: dict[str, FragmentDefinitionNode],
) -> OperationInfo:
    if operation.name is None:
        raise ValueError("Named operations are required for wrapper generation.")

    operation_name = operation.name.value
    method_name = camel_to_snake(operation_name)
    operation_type = operation.operation.value
    needed_fragments = collect_fragments(operation, fragments)
    rendered_parts = [print_ast(operation), *[print_ast(fragment) for fragment in needed_fragments]]
    document = "\n\n".join(rendered_parts)

    variable_map: dict[str, str] = {}
    for variable_definition in operation.variable_definitions or []:
        variable_name = variable_definition.variable.name.value
        variable_map[variable_name] = variable_name
        variable_map[camel_to_snake(variable_name)] = variable_name

    return OperationInfo(
        operation_name=operation_name,
        method_name=method_name,
        operation_type=operation_type,
        document=document,
        variable_map=variable_map,
    )


def collect_fragments(
    operation: OperationDefinitionNode,
    fragments: dict[str, FragmentDefinitionNode],
) -> list[FragmentDefinitionNode]:
    ordered: list[FragmentDefinitionNode] = []
    seen: set[str] = set()

    def add_from_node(node: OperationDefinitionNode | FragmentDefinitionNode) -> None:
        fragment_names: list[str] = []

        class FragmentSpreadVisitor(Visitor):
            def enter_fragment_spread(self, inner_node, *_args: object) -> None:  # type: ignore[no-untyped-def]
                fragment_names.append(inner_node.name.value)

        visit(node, FragmentSpreadVisitor())

        for fragment_name in fragment_names:
            if fragment_name in seen:
                continue
            seen.add(fragment_name)
            fragment = fragments[fragment_name]
            add_from_node(fragment)
            ordered.append(fragment)

    add_from_node(operation)
    return ordered


def camel_to_snake(value: str) -> str:
    first_pass = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    second_pass = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first_pass)
    return second_pass.lower()


def write_operations_module(operations: list[OperationInfo]) -> None:
    lines = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Literal",
        "",
        "",
        "@dataclass(frozen=True)",
        "class OperationSpec:",
        "    operation_name: str",
        "    operation_type: Literal['query', 'mutation', 'subscription']",
        "    document: str",
        "    variable_map: dict[str, str]",
        "",
        "",
        "OPERATION_REGISTRY: dict[str, OperationSpec] = {",
    ]

    for operation in operations:
        lines.extend(
            [
                f"    {operation.method_name!r}: OperationSpec(",
                f"        operation_name={operation.operation_name!r},",
                f"        operation_type={operation.operation_type!r},",
                f"        document={operation.document!r},",
                f"        variable_map={operation.variable_map!r},",
                "    ),",
            ]
        )

    lines.extend(["}", ""])
    OPERATIONS_MODULE_PATH.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
