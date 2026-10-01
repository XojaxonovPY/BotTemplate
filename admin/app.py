from starlette_admin.contrib.sqla import Admin, ModelView

from admin.provider import UsernameAndPasswordProvider
from db.engine import engine
from db.models import User

admin = Admin(
    engine,
    title="Fast API Admin",
    base_url="/admin",
    secret_key="sdgfhjhhsfdghn",
    auth_provider=UsernameAndPasswordProvider(),
)


class UserModelView(ModelView):
    fields = [User.id, User.username]


user_model = UserModelView(User)
admin.add_view(user_model)
