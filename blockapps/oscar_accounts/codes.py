import random
import string

from oscar.core.loading import get_model

Account = get_model('oscar_accounts', 'Account')


def generate(size=5, chars=None):
    """
    Generate a new account code
    5位数开始，如果5位数用完，就6位数...，作为每个用户绑定的唯一数字ID，也是各种转账钱包的凭证.
    :size: Length of code
    :chars: Character set to choose from
    """
    if chars is None:
        chars = string.digits
    code = ''.join(random.choice(chars) for x in range(size))
    # Ensure code does not aleady exist
    try:
        Account.objects.get(code=code)
    except Account.DoesNotExist:
        return code
    return generate(size=size, chars=chars)
