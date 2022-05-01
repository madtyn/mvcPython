from model.model import Model


class Controller(object):
    def __init__(self, model: Model, class_view):
        self.model = model
        self.view = class_view(self)

        self.model.register_observer(self.view)

    @staticmethod
    def get_combo_options():
        """
        Returns options for the combo box in the GUI
        :return:
        """
        return 'option1', 'option2', 'option3', 'option4'

    def start(self):
        self.view.start()

    def collect_metrics(self, *args, **kwargs):
        pass
