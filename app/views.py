from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from app import app, mail
from .forms import ContactForm

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Jessica Anderson")

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    """Render the website's contact page."""
    form = ContactForm()
    if request.method == 'POST':
        # Validate form entries
        if form.validate_on_submit():
            # Get email fields
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            msg_body = form.message.data
            msg = Message(subject,
                          sender=(name, email),
                          recipients=["jespaiand@gmail.com"])
            msg.body = msg_body
            mail.send(msg)
            # confirmation message
            flash(u'Your message has been sent.', 'success')
            # Redirect user to homepage
            return redirect(url_for('home'))
        else:
            # Display errors
            flash_errors(form)
    return render_template('contact.html', form=form)

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
