import os
from werkzeug.utils import secure_filename
import uuid

def delete_old_user_image(user_bp, image_filename):
    if image_filename != 'default.jpg':
            image_path = os.path.join(user_bp.root_path, 'static/img', image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                
def get_unique_filename(filename):
    ext = os.path.splitext(filename)[1]
    return f"{uuid.uuid4()}{ext}"
                
def save_user_image(file, user_bp):
    filename = secure_filename(file.filename)
    unique_filename = get_unique_filename(filename)
    image_path = os.path.join(user_bp.root_path, 'static/img', unique_filename)
    file.save(image_path)
    return unique_filename
    


