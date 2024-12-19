import os
import sys
from PIL import Image
import sqlite3

def get_resource_path(resource_name):
   
    if hasattr(sys, '_MEIPASS'):
      
        return os.path.join(sys._MEIPASS, resource_name)
    else:
       
        return os.path.join(os.path.dirname(__file__), resource_name)

def load_image(image_name):
 
    image_path = get_resource_path(f'IMG/{image_name}') 
    return Image.open(image_path)

def get_db_connection(db_name):
    
    db_path = get_resource_path(db_name)
    return sqlite3.connect(db_path)
