from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_models, get_model


def _implements_interface(model_class):
    return hasattr(model_class, 'get_search_manager')


class Command(BaseCommand):
    args = "<app_label[.Model] ...>"
    help = u"""Rebuild tsearch2's indexes for all the specified apps/models."""

    def handle(self, *args, **options):
        models_to_rebuild = []

        if not len(args):
            raise CommandError(u"Specify at least one app name or model as 'app_label.Model'.")

        # Make sure we can import all models and that they are SearchableModels
        for arg in args:
            try:
                app_label, model_name = arg.split('.')
            except ValueError:
                app_label, model_name = arg, None

            # Try loading the model
            if not model_name:
                try:
                    app_module = get_app(app_label)
                    klasses = get_models(app_module)
                    if not klasses:
                        raise RuntimeError
                except ImproperlyConfigured:
                    raise CommandError(u"""Couldn't load an app named '%s'.""" % arg)
                except RuntimeError:
                    raise CommandError(u"""Couldn't load any models for the app '%s'.""" % arg)
            # Try loading all models for the app
            else:
                klass = get_model(app_label, model_name)
                if klass is None:
                    raise CommandError(u"""Couldn't load a model named '%s'.""" % arg)
                klasses = [klass]

            # Check if the models innherit from SearchableModel or implement the same interface
            klasses = filter(_implements_interface, klasses)
            if not klasses:
                raise CommandError(u"""Couldn't find *any* models that implement the get_search_manager() interface.
Are you sure they inherit from SearchableModel?""")

            models_to_rebuild.extend(klasses)

            for model_class in models_to_rebuild:
                print u"Rebuilding index for %s.%s..." % (
                    model_class._meta.app_label, model_class._meta.module_name)
                model_class.get_search_manager().update_index()
            print u"Done."