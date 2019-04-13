

class ModelMixin():
    def to_string(self):
        model_dict = {}

        allfields = self._meta.get_fields()
        for field in allfields:
            model_dict[field.attname] = getattr(self, field.attname)

        return model_dict