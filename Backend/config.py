import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(parent_directory, 'public', 'profile_pictures')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zzx1keyaskfbj123asdaASas2233f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///contactmanagement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
