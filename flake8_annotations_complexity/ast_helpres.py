import ast
from typing import List, Tuple, Any


def get_annotation_compexity(annotation_node) -> int:
    if isinstance(annotation_node, ast.Str):
        annotation_node = ast.parse(str(annotation_node.s))
    if isinstance(annotation_node, ast.Subscript):
        return 1 + get_annotation_compexity(annotation_node.slice.value)  # type: ignore
    if isinstance(annotation_node, ast.Tuple):
        return max(get_annotation_compexity(n) for n in annotation_node.elts)
    return 1


def validate_annotations_in_ast_node(node, max_annotations_complexity) -> List[Tuple[str, Any, int]]:
    too_difficult_annotations = []
    func_defs = [
        f for f in ast.walk(node)
        if isinstance(f, ast.FunctionDef)
    ]
    for funcdef in func_defs:
        annotations = list(filter(None, [a.annotation for a in funcdef.args.args]))
        if funcdef.returns:
            annotations.append(funcdef.returns)
        for annotation in annotations:
            complexity = get_annotation_compexity(annotation)
            if complexity > max_annotations_complexity:
                too_difficult_annotations.append((
                    annotation,
                    complexity,
                ))
    return too_difficult_annotations
