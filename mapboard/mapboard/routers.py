class GeoRouter:
    """
    A router to control all database operations on models in the
    geospatial application.
    """
    def db_for_read(self, model, **hints):
        """Send all read operations on geospatial models to the 'geospatial' database."""
        if model._meta.app_label == 'geospatial':
            return 'geospatial'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on geospatial models to the 'geospatial' database."""
        if model._meta.app_label == 'geospatial':
            return 'geospatial'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the geospatial app is involved."""
        if obj1._meta.app_label == 'geospatial' or \
           obj2._meta.app_label == 'geospatial':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure the geospatial app only appears in the 'geospatial' database."""
        if app_label == 'geospatial':
            return db == 'geospatial'
        return None
