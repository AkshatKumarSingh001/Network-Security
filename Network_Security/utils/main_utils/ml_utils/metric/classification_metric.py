import os, sys
from Network_Security.entity.artifact_entity import ClassificationMetrticArtifact
from Network_Security.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classification_score(y_true,y_pred) -> ClassificationMetrticArtifact:
    try:

        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)

        classification_metric = ClassificationMetrticArtifact(f1_score=float(model_f1_score),
                    precision_score=float(model_precision_score),
                    recall_score=float(model_recall_score))
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        