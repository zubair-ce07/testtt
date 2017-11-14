import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SENTIMENTAL_MODEL_NAME = 'sentimental_classifier.pickle'
SENTIMENTAL_MODEL_PATH = BASE_DIR + '/services/analysis/' + SENTIMENTAL_MODEL_NAME