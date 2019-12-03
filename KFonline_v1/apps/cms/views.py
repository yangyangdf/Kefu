from flask import (
    Blueprint,
    render_template,
    views, request,
    session, redirect,
    url_for, g,
    jsonify)

from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
    UpdateUserForm,
    AddUserForm,
    AddFuserForm,
    UpdateFuserForm,
    AddrolesForm,
    UpdateRoleForm
)


from .models import CMSUser, CMSPermission, cms_role_user, CMSRole
from ..front.models import FrontUser
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, kfcache
import string
import random
from tasks import send_mail
from flask_paginate import Pagination,get_page_parameter

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')


@bp.route('/logout')
@login_required
def logout():
    # session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入邮箱参数！')

    soure = list(string.ascii_letters)
    soure.extend(map(lambda x: str(x), range(0, 10)))
    captcha = ''.join(random.sample(soure, 6))

    # 给这个邮箱发送邮件
    # message = Message(
    #     '在线知识库邮箱验证',
    #     recipients=[email],
    #     body='您的验证码是：%s' % captcha
    # )
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    send_mail.delay('在线知识库邮箱验证',[email],'您的验证码是：%s' % captcha)
    kfcache.set(email, captcha)
    return restful.success()


@bp.route('/email/')
def send_email():
    message = Message(
        '在线系统邮件发送',
        recipients=['412880433@qq.com'],
        body='测试',
    )
    mail.send(message)
    return 'success'


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts = PostModel.query.slice(start,end)
    pagination = Pagination(bs_version=3,page=page,total=PostModel.query.count(),outer_window=0,inner_window=2)
    context = {
        'posts':posts,
        'pagination':pagination
    }


    return render_template('cms/cms_posts.html',**context)


@bp.route('/hpost/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/dpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这个板块')

    db.session.delete(post)
    db.session.commit()
    return restful.success()

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    print(form.board_id)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')

    if not board_id:
        return restful.params_error(message='请传入板块id！')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    fusers_models = FrontUser.query.all()
    context = {
        'fusers':fusers_models
    }
    return render_template('cms/cms_fusers.html',**context)


@bp.route('/afuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def afuser():
    form = AddFuserForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        username = form.username.data
        password = form.password.data
        user = FrontUser(telephone=telephone,username=username,password=password,)
        db.session.add(user)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dfuser/',methods=['POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def dfuser():
    user_id = request.form.get('user_id')
    print(user_id)
    if not user_id:
        return restful.params_error(message='请传入用户id')

    user = FrontUser.query.get(user_id)
    if not user_id:
        return restful.params_error(message='没有这个用户')
    db.session.delete(user)
    db.session.commit()
    return restful.success()


@bp.route('/ufuser/',methods=['POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def ufuser():
    form = UpdateFuserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        username = form.username.data
        telephone = form.telephone.data
        password = form.password.data
        user = FrontUser.query.get(user_id)
        if user:
            user.username = username
            user.telephone = telephone
            user.password = password
            db.session.commit()
            return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    cusers_models = CMSUser.query.all()
    context = {
        'cusers':cusers_models
    }
    return render_template('cms/cms_cusers.html',**context)

@bp.route('/auser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def auser():
    form = AddUserForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = CMSUser(username=username,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uuser/',methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def uuser():
    form = UpdateUserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        username = form.username.data
        email = form.email.data
        user = CMSUser.query.get(user_id)
        if user:
            user.username = username
            user.email = email
            db.session.commit()
            return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/duser/',methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def duser():
    user_id = request.form.get('user_id')

    if not user_id:
        return restful.params_error(message='请传入用户id')

    user = CMSUser.query.get(user_id)
    if not user_id:
        return restful.params_error(message='没有这个用户')
    db.session.delete(user)
    db.session.commit()
    return restful.success()

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    cmsusers = CMSUser.query.all()
    context = {
        'cmsusers':cmsusers
    }
    return render_template('cms/cms_croles.html',**context)

# @bp.route('/aroles/')
# @login_required
# @permission_required(CMSPermission.CMSUSER)
# def aroles():
#     form = AddrolesForm(request.form)
#     if form.validate():
#         email = form.email.data
#         role = form.role.data
#         user = CMSUser.query.filter_by(email=email).first()
#         print(user)
#         if user:
#             role = CMSRole.query.filter_by(role=role).first()
#             if role:
#                 role.users.append(user)
#                 db.session.commit()
#                 print('用户添加角色成功')
#             else:
#                 print('没有这个角色：%s' % role)
#         else:
#             print('%s邮箱没有这个用户！' % email)
#         return restful.success()
#     else:
#         return restful.params_error(message=form.get_error())
#
# @bp.route('/uroles/',methods=['POST'])
# @login_required
# @permission_required(CMSPermission.CMSUSER)
# def uroles():
#     form = UpdateRoleForm(request.form)
#     if form.validate():
#         user_id = form.user_id.data
#         userId = form.cms_user_id.data
#         roleId = form.cms_role_id.data
#         user = CMSUser.query.get(user_id)
#         if user:
#             user.cms_user_id = userId
#             user.cms_role_id = roleId
#             db.session.commit()
#             return restful.success()
#         else:
#             return restful.params_error(message=form.get_error())


@bp.route('/droles/',methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def droles():
    user_id = request.form.get('user_id')
    if not user_id:
        return restful.params_error(message='请传入用户id')

    user = CMSUser.query.get(user_id)
    if not user_id:
        return restful.params_error(message='没有这个用户')
    db.session.delete(user)
    db.session.commit()
    return restful.success()


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请输入轮播图id')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            passwprd = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(passwprd):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 如果设置session.permanent = True
                    # name过期时间是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                # self.get()
                return self.get(message='邮箱或者密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
