from dataclasses import dataclass # dataclass is a decorator that automatically generates special methods like __init__() and __repr__() for classes. It is used to create classes that primarily store data and reduces boilerplate code.

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

