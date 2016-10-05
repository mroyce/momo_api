from datetime import datetime

from django.db import models


class ActiveModelMixin(models.Model):
    """
    Has an `is_active` field for tracking whether
    a certain model is active.
    """
    is_active = models.BooleanField(blank=True, default=True)
    inactive_on = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.is_active:
            self.inactive_on = datetime.now
        super(ActiveModelMixin, self).save(*args, **kwargs)


class TrackEditsModelMixin(models.Model):
    """
    Has a `edited_at` field for tracking the last
    time a model was edited.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    @property
    def edited(self):
        """
        `True` if the model has ever been edited.
        """
        return self.created_at != self.edited_at
