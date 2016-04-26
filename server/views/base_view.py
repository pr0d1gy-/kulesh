from flask.views import MethodView


class BaseMethodView(MethodView):

    kwargs = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs
