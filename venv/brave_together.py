import app.dal.models as models
from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Tag': models.Tag,
        'Media': models.Media,
        'Story': models.Story,
        'Event': models.Event,
        'Changelog': models.Changelog,
        'User': models.User,
        'Role': models.Role,
        'EventParticipation': models.EventParticipation
    }
