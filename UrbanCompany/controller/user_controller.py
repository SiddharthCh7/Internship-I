from app import app
from flask import request
from model.info_model import info_model


obj=info_model()

@app.route("/user/getall/package")
def info_getall_package_controller():
    return obj.info_getall_package()

