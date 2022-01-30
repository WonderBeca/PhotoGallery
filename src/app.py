from boto3 import *
from bson import ObjectId
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_manager, login_required, login_user, logout_user
from controller.s3 import s3Controller as S3
from werkzeug.utils import secure_filename
from datetime import datetime
from model.database import mongo_client
from model.posts_model import fetch_posts

from model.user_model import User, admin_required
import hashlib

app = Flask(__name__,
            static_folder='view/static/',
            template_folder='view',)
app.url_map.strict_slashes = False

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "/register"


def redirect_to_response(destination: str):
    return jsonify({
        'redirect': destination
    })

@app.route("/login", methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data["login"]
    password = request_data["password"]
    find_user = User.get_by_email(email)
    if find_user and find_user.login(password):
        # Remember = Login automatico
        print('logging in')
        login_user(find_user, remember=True)
        flash('You have been logged in!', 'success')
    else:
        print('something went wrong')

    return redirect_to_response(url_for("render_gallery_feed"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        request_data = request.get_json()
        existing_user = User.get_by_email(request_data['login'])
        if existing_user is None:
            User.register(
                username=request_data['username'],
                email=request_data['login'],
                password=request_data['password'],
                role=request_data['role']
            )
            flash('Conta criada com sucesso')
            return redirect_to_response(url_for("home_page"))

        else:
            return jsonify('That username already exist!')


@login_manager.user_loader
def load_user(user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        user.toggle_login_on()
        return user
    else:
        return None


@app.route("/")
@login_required
def home_page():
    return render_template("register.html")


@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if request.method == 'POST':

        file_to_upload = request.files['file']
        content_type = request.mimetype

        if file_to_upload:

            file_name = hashlib.md5(
                (str(datetime.now()) + '-' + secure_filename(file_to_upload.filename)).encode())
            bucket_name = "mygallerytest"

            file_owner = mongo_client.get_collection(
                'users').find_one({"email": current_user.email})

            S3.s3_upload_small_files(
                file_to_upload, bucket_name, file_name.hexdigest(), content_type)
            flash(
                f'Success - {file_to_upload} Is uploaded to {bucket_name}', 'success')
            image = mongo_client.get_collection('images')
            image.insert_one({
                'image_hash': file_name.hexdigest(),
                'approved': 0,
                'file_owner': ObjectId(file_owner['_id']),
                'upload_date': datetime.now().strftime("%d/%m/%y")})

    return redirect(url_for('render_gallery_feed'))


@app.route('/gallery/feed')
@login_required
def render_gallery_feed():
    image_data = fetch_posts({'approved': 1})

    images = S3.s3_read_objects('mygallerytest', image_data)
    return render_template("gallery.html", images=images)


@app.route('/gallery/pendent')
@login_required
def render_gallery_pendent():
    if ('user' in current_user.roles):
        image_data = fetch_posts({'approved': {"$in": [0, 2]}, 'file_owner': current_user._id})

        images = S3.s3_read_objects('mygallerytest', image_data)
        return render_template("gallery_pendent.html", images=images)
    else:
        image_data = fetch_posts({'approved': 0})

        images = S3.s3_read_objects('mygallerytest', image_data)
        return render_template("gallery_toapprove.html", images=images)


@app.route('/approve_image', methods=['POST'])
@login_required
def approve_image():
    request_data = request.get_json()
    mongo_client.get_collection('images').find_one_and_update({
        'image_hash': request_data['image']
    },
    {
        "$set": {'approved': request_data['status']}
    })
    return redirect_to_response(url_for('render_gallery_pendent'))


@app.route('/post_comment', methods=['POST'])
@login_required
def post_comment():
    request_data = request.get_json()
    mongo_client.get_collection('comments').insert_one(request_data)
    return redirect_to_response(url_for('render_gallery_feed'))


@app.route('/like_post', methods=['POST'])
@login_required
def like_post():
    request_data = request.get_json()
    try:
        request_data['user'] = ObjectId(request_data['user'])
        if request_data['liked'] == True and not mongo_client.get_collection('liked').find_one({'user': current_user._id, 'image_hash': request_data['image_hash']}):
            print('Inserting like')
            mongo_client.get_collection('liked').insert_one(request_data)
        else:
            print('Removing like')
            mongo_client.get_collection('liked').delete_one(
                {'user': current_user._id, 'image_hash': request_data['image_hash']})
    except:
        pass

    return redirect_to_response(url_for('render_gallery_feed'))


app.secret_key = 'super_super secret key'
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
