from src.masks import get_mask_account, get_mask_card_number, get_date

print(get_mask_card_number("1234567890987654"))
print(get_mask_account("1234567890987654"))
print(get_date("11","07","2018"))
