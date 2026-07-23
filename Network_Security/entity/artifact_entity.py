from dataclasses import dataclass # dataclass is a decorator that automatically generates special methods like __init__() and __repr__() for classes. It is used to create classes that primarily store data and reduces boilerplate code.

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

