from pyteal import *

def escrow_account(h_receiver, g_receiver):
    """Only allow receiver (host and/or guest) to withdraw funds from this contract account."""
    is_two_tx = Global.group_size() == Int(2)
    is_app_call = Gtxn[0].type_enum() == Int(6)
    app_call = Gtxn[0].application_id() == Int(13078399)
    is_payment = Gtxn[0].type_enum() == Int(1)
    is_second_payment = Gtxn[1].type_enum() == Int(1)
    is_first_correct_receiver = Gtxn[0].receiver() == Addr(h_receiver)
    is_second_correct_receiver = Gtxn[1].receiver() == Addr(g_receiver)
    is_first_not_close = Gtxn[0].close_remainder_to() == Global.zero_address()
    is_first_not_close_asset = Gtxn[0].asset_close_to() == Global.zero_address()
    is_second_not_close = Gtxn[1].close_remainder_to() == Global.zero_address()
    is_second_not_close_asset = Gtxn[1].asset_close_to() == Global.zero_address()    

    return And( is_two_tx, is_app_call, app_call, is_payment, is_second_payment, is_first_correct_receiver,  is_second_correct_receiver, is_first_not_close, is_first_not_close_asset, is_second_not_close, is_second_not_close_asset)

with open('./escrow_account.teal', 'w') as f:
    compiled = compileTeal(escrow_account("YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I","7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU"), Mode.Application)
    f.write(compiled)



# app ID 12895806
# escrow account BQYS37XEBMGNXFOQY7WH6FGKRLAWNIZKP4MCJAT5AWI4DFEC7ZSG4CQAW4
# host YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I
# guest 7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU

