
import os
import sys
import locale

def get_encoding():
    """Return system encoding. """
    try:
        encoding = locale.getpreferredencoding()
        'TEST'.encode(encoding)
    except:
        encoding = 'UTF-8'

    return encoding


def convert_on_bounds(func):
    """Decorator to convert string inputs & outputs.

    Covert string inputs & outputs between 'str' and 'unicode' at the
    application bounds using the preferred system encoding. It will convert
    all the string params (args, kwargs) to 'str' type and all the
    returned strings values back to 'unicode'.

    """
    def convert_item(item, to_unicode=False):
        """The actual function which handles the conversion.

        Args:
            item (-): Can be any python item.

            to_unicode (boolean): When True it will convert all the 'str' types
                to 'unicode'. When False it will convert all the 'unicode'
                types back to 'str'.

        """
        if to_unicode and isinstance(item, str):
            # Convert str to unicode
            return item.decode(get_encoding(), 'ignore')

        if not to_unicode and isinstance(item, str):
            # Convert unicode to str
            return item.encode(get_encoding(), 'ignore')

        if hasattr(item, '__iter__'):
            # Handle iterables
            temp_list = []

            for sub_item in item:
                if isinstance(item, dict):
                    temp_list.append((sub_item, convert_item(item[sub_item])))
                else:
                    temp_list.append(convert_item(sub_item))

            return type(item)(temp_list)

        return item

    def wrapper(*args, **kwargs):
        returned_value = func(*convert_item(args), **convert_item(kwargs))

        return convert_item(returned_value, True)

    return wrapper

# See: https://github.com/MrS0m30n3/youtube-dl-gui/issues/57
# Patch os functions to convert between 'str' and 'unicode' on app bounds
os_getenv = convert_on_bounds(os.getenv)
os_makedirs = convert_on_bounds(os.makedirs)
os_path_isdir = convert_on_bounds(os.path.isdir)
os_path_exists = convert_on_bounds(os.path.exists)
os_path_dirname = convert_on_bounds(os.path.dirname)
os_path_abspath = convert_on_bounds(os.path.abspath)
os_path_realpath = convert_on_bounds(os.path.realpath)
os_path_expanduser = convert_on_bounds(os.path.expanduser)

# Patch Windows specific functions
if os.name == 'nt':
    os_startfile = convert_on_bounds(os.startfile)

def remove_file(filename):
    if os_path_exists(filename):
        os.remove(filename)
        return True

    return False

def remove_shortcuts(path):
    """Return given path after removing the shortcuts. """
    return path.replace('~', os_path_expanduser('~'))


def absolute_path(filename):
    """Return absolute path to the given file. """
    return os_path_dirname(os_path_realpath(os_path_abspath(filename)))

def get_icons_dir():
    """Return absolute path to the icons icons folder.

    Note:
        Paths we search: __main__ dir, library dir

    """
    # search_dirs = [
    #     os.path.join(absolute_path(sys.argv[0]), ""),
    #     os.path.join(os_path_dirname(__file__), "")

    #     # absolute_path(sys.argv[0]),
    #     # os_path_dirname(__file__)
    # ]

    # for directory in search_dirs:
    icons_dir = os.path.join(os.getcwd(), "icons")

    if os_path_exists(icons_dir):
        return icons_dir

    return None

def get_icon_file():
    """Search for pWallet app icon.

    Returns:
        The path to pWallet icon file if exists, else returns None.

    """
    ICON_NAME = "walletlogo.ico"

    icons_dir = get_icons_dir()

    if icons_dir is not None:
        icon_file = os.path.join(icons_dir, ICON_NAME)

        if os_path_exists(icon_file):
            return icon_file

    return None

def convert_on_bounds(func):
    """Decorator to convert string inputs & outputs.

    Covert string inputs & outputs between 'str' and 'unicode' at the
    application bounds using the preferred system encoding. It will convert
    all the string params (args, kwargs) to 'str' type and all the
    returned strings values back to 'unicode'.

    """
    def convert_item(item, to_unicode=False):
        """The actual function which handles the conversion.

        Args:
            item (-): Can be any python item.

            to_unicode (boolean): When True it will convert all the 'str' types
                to 'unicode'. When False it will convert all the 'unicode'
                types back to 'str'.

        """
        if to_unicode and isinstance(item, str):
            # Convert str to unicode
            return item.decode(get_encoding(), 'ignore')

        if not to_unicode and isinstance(item, str):
            # Convert unicode to str
            return item.encode(get_encoding(), 'ignore')

        if hasattr(item, '__iter__'):
            # Handle iterables
            temp_list = []

            for sub_item in item:
                if isinstance(item, dict):
                    temp_list.append((sub_item, convert_item(item[sub_item])))
                else:
                    temp_list.append(convert_item(sub_item))

            return type(item)(temp_list)

        return item

    def wrapper(*args, **kwargs):
        returned_value = func(*convert_item(args), **convert_item(kwargs))

        return convert_item(returned_value, True)

    return wrapper



os_path_exists = convert_on_bounds(os.path.exists)
os_makedirs = convert_on_bounds(os.makedirs)

def get_encoding():
    """Return system encoding. """
    try:
        encoding = locale.getpreferredencoding()
        'TEST'.encode(encoding)
    except:
        encoding = 'UTF-8'

    return encoding

def check_path(path):
    """Create path if not exist. """
    if not os_path_exists(path):
        os_makedirs(path)


# 最小长度5，最大长度63，
# 可以.分隔，分隔的每一部分要求以小写字母开头，以数字或小写字母结尾; 每一部分的中间部分可以为：小写字母、数字、-; 每一部分的长度5~63
MIN_ACCOUNT_NAME_LENGTH = 5
MAX_ACCOUNT_NAME_LENGTH = 63
lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
def is_lower_alpha(ch):
    if lower_alpha.find(ch) == -1:
        return False
    return True

def is_valid_name(name):
    length = len(name)
    if length < MIN_ACCOUNT_NAME_LENGTH or length > MAX_ACCOUNT_NAME_LENGTH:
        return False

    begin = 0
    while True:
        end = name.find('.', begin)
        if end == -1:
            end = length
        if end - begin < MIN_ACCOUNT_NAME_LENGTH:
            return False
        
        if not is_lower_alpha(name[begin]):
            return False
        if not (is_lower_alpha(name[end-1]) or name[end-1].isdigit()):
            return False
        for index in range(begin+1, end-1):
            ch = name[index]
            if not (is_lower_alpha(ch) or ch.isdigit() or ch == '-'):
                return False
        if end == length:
            break
        begin = end + 1
    return True