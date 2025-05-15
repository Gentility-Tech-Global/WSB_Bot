import random

def generate_account_number(user_id: str) -> str:
    """
    Generate a 10-digit account number.
    Example implementation based on a random logic or phone-number style account .
    """

    return f"30{str(user_id).zfill(8)[-8]}"