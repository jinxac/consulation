from commons.models.manager import LogicalDeletedManager


class ClientManager(LogicalDeletedManager):
    def create_user(self, user):
        if not user:
            raise ValueError('User must be set!')
        user = self.model(user=user)
        user.save(using=self._db)
        return user
