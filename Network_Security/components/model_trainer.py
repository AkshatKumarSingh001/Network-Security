import os
import sys

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

from Network_Security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from Network_Security.entity.config_entity import ModelTrainerConfig

from Network_Security.utils.main_utils.ml_utils.model.estimator import NetworkModel
from Network_Security.utils.main_utils.utils import save_object,load_object
from Network_Security.utils.main_utils.utils import load_numpy_array_data
from Network_Security.utils.main_utils.ml_utils.metric.classification_metric import get_classification_score
from Network_Security.utils.main_utils.ml_utils.model_selection import evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, r2_score, recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow
import mlflow.sklearn as mlflow_sklearn

## Importing dagshub for experiment tracking and logging
import dagshub
dagshub.init(repo_owner='AkshatKumarSingh001', repo_name='Network-Security', mlflow=True)
print(mlflow.get_tracking_uri())  # add this temporarily



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def track_mlflow(self, best_model, train_metric, test_metric):
        with mlflow.start_run():
            mlflow.log_param("model_name", type(best_model).__name__)

            mlflow.log_metric("train_f1_score", train_metric.f1_score)
            mlflow.log_metric("train_precision_score", train_metric.precision_score)
            mlflow.log_metric("train_recall_score", train_metric.recall_score)

            mlflow.log_metric("test_f1_score", test_metric.f1_score)
            mlflow.log_metric("test_precision_score", test_metric.precision_score)
            mlflow.log_metric("test_recall_score", test_metric.recall_score)

            print("Artifact URI:", mlflow.get_artifact_uri())
            mlflow_sklearn.log_model(best_model, name="model")
            print("Model artifact logged successfully")
            

        

    def train_model(self,X_train,y_train,x_test,y_test):
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            model_report:dict = evaluate_models(x_train=X_train, y_train = y_train, x_test = x_test, y_test = y_test,
                   models = models, param = params)

            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            # To get the best model name from dict
            best_model_name = list(model_report.keys())[
                 list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)

            classification_train_metric = get_classification_score(y_true = y_train,y_pred = y_train_pred)

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred = y_test_pred)

            ## Track the experiments with mlflow
            self.track_mlflow(best_model, classification_train_metric, classification_test_metric)


            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            Network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=Network_model)


            save_object("final_model/model.pkl", best_model)


            ## Model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          train_metric_artifact=classification_train_metric,
                                                            test_metric_artifact=classification_test_metric
                                                            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact



    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train, y_train, x_test, y_test)
            return model

        except Exception as e:
            raise NetworkSecurityException(e,sys)