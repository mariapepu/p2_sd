from fastapi.security import OAuth2PasswordBearer
from pydantic.tools import lru_cache
import utils


@lru_cache()
def get_settings():
    return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
