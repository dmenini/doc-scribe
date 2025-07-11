from collections import defaultdict
from pathlib import Path

ALLOWED_EXTENSIONS = [".py", ".kt", ".ts", ".vue"]


class CodebaseLoader:
    def __init__(self, root_path: Path, exclude: list[str] | None = None, include: list[str] | None = None) -> None:
        self.root_path = root_path
        self.exclude = exclude or []
        self.include = include or []

    def _get_file_paths(self) -> list[Path]:
        """Recursively finds all Python files in the given directory."""
        if self.root_path.is_file() and self.root_path.suffix in ALLOWED_EXTENSIONS:
            return [self.root_path]

        all_files = [file for ext in ALLOWED_EXTENSIONS for file in self.root_path.rglob("*" + ext)]
        relevant = [file for file in all_files if self._is_included(file) and not self._is_excluded(file)]
        return sorted(relevant)

    def load_file(self, file_path: Path) -> str:
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()

    def load_all_files(self) -> dict[str, str]:
        python_files = self._get_file_paths()

        tree = {}
        for file in python_files:
            relative_path = file.relative_to(self.root_path)  # Preserve structure
            code = self.load_file(file)
            if code.strip():
                tree[str(relative_path)] = code
        return tree

    def load_all_modules(self, file_separator: str = "\n\n") -> dict[str, str]:
        filepaths = self._get_file_paths()
        top_modules = set()

        for path in filepaths:
            relative_path = path.relative_to(self.root_path)
            parts = relative_path.parts
            if len(parts) > 1:
                top_modules.add(parts[0])  # First directory as top module

        tree = defaultdict(str)
        for module_name in sorted(top_modules):
            module_paths = self._get_module_files(filepaths=filepaths, module_name=module_name)
            module_code = map(self._load_formatted_file_content, module_paths)
            tree[module_name] = file_separator.join(module_code)

        return dict(tree)

    def _get_module_files(self, filepaths: list[Path], module_name: str) -> list[Path]:
        """Return all file paths belonging to the given module."""
        return [file for file in filepaths if file.relative_to(self.root_path).parts[0] == module_name]

    def _load_formatted_file_content(self, path: Path) -> str:
        """Load code and add a comment-like line at the top to include the file path."""
        template = "# File: {path}\n\n{code}"
        return template.format(path=path.relative_to(self.root_path), code=self.load_file(path))

    def _is_included(self, file: Path) -> bool:
        if not self.include:
            return True
        return any(inc in file.parts for inc in self.include)

    def _is_excluded(self, file: Path) -> bool:
        return any(exc in file.parts for exc in self.exclude)
