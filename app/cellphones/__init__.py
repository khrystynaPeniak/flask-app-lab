from flask import Blueprint

cellphone_bp = Blueprint("cellphone", __name__, url_prefix="/cellphone", template_folder="templates/cellphones", 
                         static_folder="static", static_url_path="cellphones/static")
from . import views