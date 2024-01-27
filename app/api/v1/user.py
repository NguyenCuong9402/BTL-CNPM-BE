import os
import re
import uuid

from flask import Blueprint, request
from sqlalchemy import asc, desc
from sqlalchemy import distinct
from app.models import db, User
from app.utils import send_error, get_timestamp_now, send_result, format_birthday


api = Blueprint('user', __name__)


def is_valid_email(email):
    # Biểu thức chính quy để kiểm tra email
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    # Sử dụng re.match để kiểm tra tính hợp lệ
    match = re.match(email_pattern, email)
    # Trả về True nếu email hợp lệ, ngược lại trả về False
    return bool(match)


@api.route("/register", methods=["POST"])
def register():
    try:
        body_request = request.get_json()
        #Loai bo khoang trang
        for key, value in body_request.items():
            if isinstance(value, str):
                body_request.update({key: value.strip()})

        #validate theo yêu cầu
        for key, value in body_request.items():
            if key in ["first_name", "last_name", "password", "repassword", "email"] and value == "":
                return send_error(message=f" Không được để {key} trống.")
            if key in ["first_name", "last_name"] and len(value) > 25:
                return send_error(message=f" Không được để {key} vượt quá 25 kí tự.")
            if key == "password" and len(value) < 6:
                return send_error(message=f" Không được để {key} ít hơn 6 kí tự.")

            if key == "language" and value not in ["visual_basic", "java", "net", "language"]:
                return send_error(message=f"Bạn chưa chọn {key}")
            if key == "news" and value not in ["weekly", "monthly", "news_one"]:
                return send_error(message=f"Bạn chưa chọn {key}")
        password = body_request.get("password")
        repassword = body_request.get("repassword")
        if password != repassword:
            return send_error(message=f"Bạn nhập chưa đúng mật khẩu.")

        email = body_request.get("email")
        if not is_valid_email(email):
            return send_error(message="Bạn nhập chưa đúng format email.")

        query = User.query.filter(User.email == email).first()
        if query is not None:
            return send_error(message=f"Email {email} đã được đăng ký ")
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password=password,
            address=body_request.get("address"),
            first_name=body_request.get("first_name"),
            last_name=body_request.get("last_name"),
            sex=body_request.get("sex", 0),
            language=body_request.get("language"),
            news=body_request.get("news"),
            birth=body_request.get("birthdate")
        )
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        return send_result(message="Dang ky thanh cong")


    except Exception as ex:
        db.session.rollback()
        return send_error(message=str(ex))







