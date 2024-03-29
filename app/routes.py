from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, EmptyForm, RatingForm
from app.models import User, Post, Rating
from sqlalchemy import select
from flask_login import login_user, current_user
from flask_login import logout_user
from flask_login import login_required

# Startseite und Post-Erstellung, erfordert Anmeldung
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.post.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    pagination = current_user.following_posts(page, per_page=20)
    posts = pagination.items
    rating_form = RatingForm()
    return render_template("index.html", title='Home Page', form=form, rating_form=rating_form, posts=posts, pagination=pagination)

# Anmeldefunktionalität
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Abmeldefunktionalität
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registrierungsfunktionalität
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Benutzerprofilseite
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    form = EmptyForm()
    rating_form = RatingForm()
    return render_template('user.html', user=user, posts=posts.items, pagination=posts, form=form, rating_form=rating_form)

# Profilbearbeitungsseite
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Folgen-Funktionalität
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# Entfolgen-Funktionalität
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# Route für das Entdecken von Beiträgen anderer Benutzer
@app.route('/explore')
@login_required
def explore():
    # Seitennummerierung, um durch die Beiträge zu blättern
    page = request.args.get('page', 1, type=int)
    # Abfrage der Posts in absteigender Reihenfolge nach Zeitstempel
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=20)
    # Formular für das Bewerten von Beiträgen
    rating_form = RatingForm()
    # Render des Templates für die Explore-Seite mit den abgefragten Beiträgen und dem Bewertungsformular
    return render_template('index.html', title='Explore', posts=posts.items, pagination=posts, rating_form=rating_form)

# Route für das Bewerten eines Posts
@app.route('/rate_post/<int:post_id>', methods=['POST'])
@login_required
def rate_post(post_id):
    # Instanzierung des Bewertungsformulars
    form = RatingForm()
    if form.validate_on_submit():
        # Erstellung eines neuen Rating-Objekts mit den Formulardaten
        rating = Rating(user_id=current_user.id, post_id=post_id, rating=form.rating.data)
        # Hinzufügen und Speichern des Ratings in der Datenbank
        db.session.add(rating)
        db.session.commit()
        # Benachrichtigung des Benutzers über den Erfolg der Aktion
        flash('Your rating has been submitted.')
    else:
        # Benachrichtigung des Benutzers, falls ein Fehler auftritt
        flash('There was an error with your rating.')
    # Umleitung zurück zur Startseite
    return redirect(url_for('index'))
