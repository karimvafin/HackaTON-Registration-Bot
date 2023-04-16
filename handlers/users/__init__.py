from .start import dp
from .help import dp
from .menu import dp
from .buttons import dp
from .registration import dp
from .change_user_data import dp
# команда error должна быть импортирована в конце
from .error import dp

# список параметров, которые можно импортировать с папки users
__all__ = ['dp']
