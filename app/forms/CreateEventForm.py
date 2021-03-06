from flask.ext.wtf import Form
from app.forms.fields import TimeField
from app.forms.CreateBlogPostForm import image_with_same_name
from wtforms import StringField, DateField, TextAreaField, BooleanField, \
    SelectField, IntegerField, RadioField
from wtforms.validators import Required, ValidationError, Optional, \
    NumberRange, Regexp, URL


def unique_with_database(form, field):
    message = "An event with that slug already exists."
    from app.models import Event, EventSeries
    if EventSeries.objects(slug=field.data).count() != 0:
        raise ValidationError(message)
    if Event.objects(slug=field.data).count() != 0:
        raise ValidationError(message)

class CreateEventForm(Form):

    title = StringField('Title', [
        Required(message="Please provide an event title.")])
    slug = StringField('Slug', [unique_with_database,
        Regexp('([0-9]|[a-z]|[A-Z]|-)*',
               message="Post slug should only contain numbers, letters and dashes.")])
    location = StringField('Location')
    start_date = DateField('Start date', [Optional()], format='%m/%d/%Y')
    start_time = TimeField('Start time', [Optional()])
    end_date = DateField('End date', [Optional()], format='%m/%d/%Y')
    end_time = TimeField('End time', [Optional()])
    is_recurring = BooleanField('Is Recurring')
    frequency = SelectField('Repeats', choices=[('weekly', 'Weekly')],
                            default="weekly")
    every = IntegerField('Every', [NumberRange(min=1, max=30)], default=1)
    ends = RadioField('Ends', choices=[
        ("after", "After"),
        ("on", "On")
    ], default="after")
    num_occurances = IntegerField('Every', [NumberRange(min=1)], default=1)
    recurrence_end_date = DateField('Repeat End Date', [Optional()],
                                format='%m/%d/%Y')
    recurrence_summary = StringField('Summary')
    short_description = TextAreaField('Short description', default="Short Description.  This should be **one to two** sentences long.")
    long_description = TextAreaField('Long description', default="Long Description.  This should be **four to five** sentences.  Feel free to include [links](http://adicu.com).")
    published = BooleanField('Published')
    update_all = BooleanField('Update all', default=False)
    facebook_url = StringField('Facebook  URL', [Optional(), URL()])
    event_image = StringField('Image', [image_with_same_name])

    def post_validate(form, validation_stopped):
        """Make sure that the start datetime comes before the end datetime"""
        start_date = form.start_date.data
        start_time = form.start_time.data
        end_date = form.end_date.data
        end_time = form.end_time.data

        # Start and end dates should be in order.
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date should come before end date")
        if all([start_date, start_time, end_date, end_time]) and \
                start_time > end_time:
            raise ValidationError("Start time should come before end date")
