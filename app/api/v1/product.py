import os
import uuid
from flask import Blueprint, request, make_response, send_file, Response
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from sqlalchemy import asc, desc
from io import BytesIO
import datetime
import io
import shutil

from sqlalchemy_pagination import paginate
from werkzeug.utils import secure_filename

from app.api.v1.picture import FILE_PATH, FILE_PATH_PRODUCT
from app.models import db, Product, User, Orders, OrderItems, CartItems, PhanLoai
from app.schema import ProductSchema, GetTypeSchema
from app.utils import send_error, get_timestamp_now, send_result, escape_wildcard

api = Blueprint('product', __name__)


@api.route("", methods=["POST"])
@jwt_required()
def add_product():
    try:
        jwt = get_jwt()
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        if user.admin == 0 or (not jwt.get("is_admin")):
            return send_result(message="Bạn không phải admin.")
        file = request.files.get('file', None)
        name = request.form.get('name', '')
        old_price = int(request.form.get('old_price', 0))
        giam_gia = int(request.form.get('giam_gia', 0))
        phan_loai_id = request.form.get('phan_loai_id', '')
        describe = request.form.get('describe', '')
        cac_mau = request.form.get('cac_mau', [])
        cac_mau = cac_mau.split(',')
        if len(cac_mau) == 0:
            return send_error(message='Chưa chọn màu cho sản phẩm')
        if phan_loai_id == "":
            return send_error(message='Vui lòng chọn loại sản phẩm')
        if len(name) > 40:
            return send_error(message='Tên quá dài!')
        if check_coincided_name(name):
            return send_error(message="Tên sản phẩm đã tồn tại")
        if file is None:
            product = Product(
                id=str(uuid.uuid4()),
                name=name,
                old_price=old_price,
                phan_loai_id=phan_loai_id,
                price=old_price*(100-giam_gia)/100,
                cac_mau=cac_mau,
                giam_gia=giam_gia,
                describe=describe,
                created_date=get_timestamp_now()
            )
        else:
            filename, file_extension = os.path.splitext(file.filename)
            id_product = str(uuid.uuid4())
            file_name = secure_filename(id_product + file_extension)
            if not os.path.exists(FILE_PATH_PRODUCT):
                os.makedirs(FILE_PATH_PRODUCT)
            file.save(os.path.join(FILE_PATH_PRODUCT + file_name))
            product = Product(
                id=str(uuid.uuid4()),
                name=name,
                old_price=old_price,
                phan_loai_id=phan_loai_id,
                price=old_price * (100 - giam_gia) / 100,
                cac_mau=cac_mau,
                giam_gia=giam_gia,
                describe=describe,
                created_date=get_timestamp_now(),
                picture=file_name
            )
        db.session.add(product)
        db.session.flush()
        db.session.commit()
        return send_result(message="Thêm sản phẩm thành công")
    except Exception as ex:
        db.session.rollback()
        return send_error(message=str(ex))


@api.route("/get-item", methods=["POST"])
def get_list_item():
    try:
        body_request = request.get_json()
        khoang_tien = body_request.get("khoang_tien", {})
        page = request.args.get('page', 1, int)
        page_size = request.args.get('page_size', 10, int)
        order_by = request.args.get('order_by', 'created_date')
        order = request.args.get('order', 'desc')
        text_search = request.args.get('text_search', None)
        phan_loai_id = request.args.get('phan_loai_id', None)
        if phan_loai_id == "" or phan_loai_id is None:
            query = Product.query.filter()
            if query.count() < 1:
                add_pro()
        else:
            check = PhanLoai.query.filter(PhanLoai.id == phan_loai_id).first()
            if check is None:
                return send_error(message='Loại không tồn tại')
            get_child_type = PhanLoai.query.filter(PhanLoai.parent_id == phan_loai_id).all()
            list_id = [item.id for item in get_child_type]
            list_id.append(phan_loai_id)
            query = Product.query.filter(Product.phan_loai_id.in_(list_id))
        if text_search is not None and text_search != "":
            text_search = text_search.strip()
            text_search = text_search.lower()
            text_search = escape_wildcard(text_search)
            text_search = "%{}%".format(text_search)
            query = query.filter(Product.name.ilike(text_search))
        if len(khoang_tien) > 0:
            if khoang_tien.get('start') is not None and khoang_tien.get('end') is None:
                query = query.filter(Product.price >= int(khoang_tien.get('start')))
            elif khoang_tien.get('start') is None and khoang_tien.get('end') is not None:
                query = query.filter(Product.price <= int(khoang_tien.get('end')))
            elif khoang_tien.get('start') is not None and khoang_tien.get('end') is not None:
                if int(khoang_tien.get('start')) > int(khoang_tien.get('end')):
                    query = query.filter(Product.price >= int(khoang_tien.get('start')))
                else:
                    query = query.filter(Product.price >= int(khoang_tien.get('start')),
                                         Product.price <= int(khoang_tien.get('end')))
        column_sorted = getattr(Product, order_by)
        list_ds = query.order_by(desc(column_sorted)) if order == "desc" else query.order_by(asc(column_sorted)).all()
        query = query.order_by(desc(column_sorted)) if order == "desc" else query.order_by(asc(column_sorted))

        paginator = paginate(query, page, page_size)

        products = ProductSchema(many=True).dump(paginator.items)

        product_all = ProductSchema(many=True, only=["id"]).dump(list_ds)
        response_data = dict(
            items=products,
            total_pages=paginator.pages if paginator.pages > 0 else 1,
            total=paginator.total,
            all_product=product_all
        )
        return send_result(data=response_data)
    except Exception as ex:
        return send_error(message=str(ex))


@api.route("/get-type", methods=["GET"])
def get_type():
    try:
        query = PhanLoai.query.filter().order_by(asc(PhanLoai.key)).all()
        data1 = [{"id": "", "name": "Tất cả"}]
        data = data1 + GetTypeSchema(many=True).dump(query)
        return send_result(data=data, message_id="1")

    except Exception as ex:
        return send_error(message=str(ex))


@api.route("/get-type2", methods=["GET"])
def get_typ2e():
    try:
        query = PhanLoai.query.filter().order_by(asc(PhanLoai.key)).all()
        data = GetTypeSchema(many=True).dump(query)
        return send_result(data=data)

    except Exception as ex:
        return send_error(message=str(ex))


@api.route("/<product_id>", methods=["PUT"])
@jwt_required()
def fix_item(product_id):
    try:
        jwt = get_jwt()
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        if user.admin == 0 or (not jwt.get("is_admin")):
            return send_result(message="Bạn không phải admin.")
        file = request.files.get('file', None)
        name = request.form.get('name', '').strip()
        try:
            old_price = int(request.form.get('old_price', 0))
            giam_gia = int(request.form.get('giam_gia', 0))
        except:
            return send_error(message='Nhập sai giá, giảm giá')
        if giam_gia < 0:
            return send_error('Vui lòng điền lại giảm giá.')
        if giam_gia > 50:
            return send_error(message='Bạn sẽ lỗ đó!')

        phan_loai_id = request.form.get('phan_loai_id', '').strip()
        describe = request.form.get('describe', '').strip()
        cac_mau = request.form.get('cac_mau', [])
        if cac_mau == "":
            return send_error(message="Chưa chọn màu")
        cac_mau = cac_mau.split(',')
        if len(cac_mau) == 0:
            return send_error(message='Chưa chọn màu cho sản phẩm')
        if phan_loai_id == "":
            return send_error(message='Vui lòng chọn loại sản phẩm')
        if len(name) > 40:
            return send_error(message='Tên quá dài!')
        existed_name = Product.query.filter(Product.name == name, Product.id != product_id).first()
        if existed_name is not None:
            return send_error(message="Tên đã tồn tại")

        product = Product.query.filter(Product.id == product_id).first()
        if product_id is None:
            return send_error(message='Sản phẩm đã bị xóa')
        product.name = name
        db.session.flush()

        product.old_price = old_price
        db.session.flush()

        product.giam_gia = giam_gia
        db.session.flush()

        product.price = old_price - old_price*giam_gia/100
        db.session.flush()

        product.describe = describe
        db.session.flush()

        product.phan_loai_id = phan_loai_id
        db.session.flush()

        product.cac_mau = cac_mau
        db.session.flush()
        # Lưu các thay đổi vào cơ sở dữ liệu
        db.session.commit()
        if file:
            filename, file_extension = os.path.splitext(file.filename)
            file_name = secure_filename(product_id + file_extension)
            if not os.path.exists(FILE_PATH_PRODUCT):
                os.makedirs(FILE_PATH_PRODUCT)
            file.save(os.path.join(FILE_PATH_PRODUCT + file_name))
            product.picture = file_name
            db.session.flush()
        db.session.commit()
        return send_result(data=ProductSchema().dump(product),
                           message="Thay đổi thông tin sản phẩm thành công")
    except Exception as ex:
        db.session.rollback()
        return send_error(message=str(ex))


@api.route("", methods=["DELETE"])
@jwt_required()
def remove_item():
    try:
        jwt = get_jwt()
        user_id = get_jwt_identity()
        body_request = request.get_json()
        list_id = body_request.get('list_id', [])
        user = User.query.filter(User.id == user_id).first()
        if user.admin == 0 or (not jwt.get("is_admin")):
            return send_result(message="Bạn không phải admin.")
        if len(list_id) == 0:
            return send_error(message='Chưa chọn item nào.')
        items = Product.query.filter(Product.id.in_(list_id)).all()

        for item in items:
            if item.picture is not None and item.picture != "":
                file_path = FILE_PATH_PRODUCT + item.picture
                if os.path.exists(os.path.join(file_path)):
                    os.remove(file_path)
        Product.query.filter(Product.id.in_(list_id)).delete()
        db.session.flush()
        db.session.commit()
        return send_result(message="Xóa sản phẩm thành công")
    except Exception as ex:
        db.session.rollback()
        return send_error(message=str(ex))


@api.route("/<product_id>", methods=["GET"])
def get_item(product_id):
    try:

        check_item = Product.query.filter(Product.id == product_id).first()
        if check_item is None:
            return send_error(message="Sản phẩm không tồn tại, F5 lại web")
        san_pham_lien_quan = Product.query.filter(Product.phan_loai_id == check_item.phan_loai_id,
                                                  Product.id != check_item.id)\
            .order_by(Product.created_date).limit(10).all()
        data = {
            "data": ProductSchema().dump(check_item),
            "lien_quan": ProductSchema(many=True).dump(san_pham_lien_quan),
        }

        return send_result(data=data)
    except Exception as ex:
        db.session.rollback()
        return send_error(message=str(ex))


def check_coincided_name(name=''):
    existed_name = Product.query.filter(Product.name == name).first()
    if existed_name is None:
        return False
    return True


def check_coincided_name_product(name='', product_id=''):
    existed_name = Product.query.filter(Product.name == name, Product.id != product_id).first()
    if existed_name is None:
        return False
    return True


def add_pro():
    try:

        FILE_PATH_MAU_ANH = "app/files/mau_anh"
        FILE_PATH_PRODUCT = "app/files/product/"
        quan = PhanLoai.query.filter(PhanLoai.key == 'quan').first()
        if quan is None:
            quan = PhanLoai(
                id=str(uuid.uuid4()),
                key='quan',
                name='Quần'
            )
            db.session.add(quan)
            db.session.flush()
            quan_au = PhanLoai(
                id=str(uuid.uuid4()),
                key='quan_au',
                name='Quần Âu',
                parent_id=quan.id
            )
            db.session.add(quan_au)
            db.session.flush()
        else:
            quan_au = PhanLoai.query.filter(PhanLoai.key == 'quan_au').first()
            if quan_au is None:
                quan_au = PhanLoai(
                    id=str(uuid.uuid4()),
                    key='quan_au',
                    name='Quần Âu',
                    parent_id=quan.id
                )
                db.session.add(quan_au)
                db.session.flush()

        product_default = [{'name': 'quần âu caro trẻ trung', 'picture': 'quan_au_caro.jpg', "old_price":100,"giam_gia": 10},
                           {'name': 'quần beggy', 'picture': 'quan_beggy.jpg', "old_price": 100,"giam_gia": 10},
                           {'name': 'quần âu nâu', 'picture': 'quan_au_nau.jpg', "old_price": 100,"giam_gia": 10},
                           {'name': 'quần thanh lịch', 'picture': 'quan_thanh_lich.jpg', "old_price": 100, "giam_gia": 10}]
        list_add_data = []
        for i, product in enumerate(product_default):
            check = Product.query.filter(Product.name == product['name']).first()
            if check is None:
                product_id = str(uuid.uuid4())
                old_image_path = os.path.join(FILE_PATH_MAU_ANH, f"{product['picture']}")
                new_image_path = os.path.join(FILE_PATH_PRODUCT, f"{product_id}.jpg")
                shutil.copyfile(old_image_path, new_image_path)
                add_pro = Product(
                    id=product_id,
                    name=product['name'],
                    old_price=product['old_price'],
                    giam_gia=product['giam_gia'],
                    price=product['old_price']*(100-product['giam_gia'])/100,
                    phan_loai_id=quan_au.id,
                    describe="Sản phẩm tuyệt vời",
                    picture=product_id + '.jpg',
                    created_date=get_timestamp_now() + i
                )
                list_add_data.append(add_pro)
        db.session.bulk_save_objects(list_add_data)
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))


