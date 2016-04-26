from cx_Freeze import setup, Executable

setup(
    name = "PhotoOrganizer",
    version = "0.1",
    description = "A application for organizing photos.",
    executables = [Executable("src/__init__.py", base=None, targetName="PhotoOrganizer")]
)
