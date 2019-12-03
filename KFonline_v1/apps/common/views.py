from flask import Blueprint,request,make_response,jsonify

from utils import restful
from utils import kfcache
from utils.captcha import Captcha
from io import BytesIO
import qiniu

bp = Blueprint('common',__name__,url_prefix='/c')

@bp.route('/')
def index():
    return 'common index'


@bp.route("/captcha/")
def graph_captcha():
    #获取验证码
    text,image=Captcha.gene_graph_captcha()
    #BytesIo 自载留
    kfcache.set(text.lower(),text.lower())
    out=BytesIO()
    image.save(out,"png")
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type="image/png"
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = 'X7a1DCsqPQ8M0TWXGjxahPaLMi3AVxWdLaKHYztR'
    secret_key = '-PFBtC0MxEW_gDKwLFBaUrhQBgDw7TBohgtxQifM'
    q = qiniu.Auth(access_key,secret_key)

    bucket = 'kfonline'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})