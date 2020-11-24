from pyteal import *

def escrow_account(h_receiver, g_receiver):
    """Only allow receiver (host and/or guest) to withdraw funds from this contract account."""
    app_call = Gtxn[0].application_id() == Int(13127362)
    is_payment = Gtxn[1].type_enum() == Int(1)
    is_second_payment = Gtxn[2].type_enum() == Int(1)
    is_first_correct_receiver = Gtxn[1].receiver() == Addr(h_receiver)
    is_second_correct_receiver = Gtxn[2].receiver() == Addr(g_receiver)   
    return And(app_call, is_payment, is_second_payment, is_first_correct_receiver,  is_second_correct_receiver)

with open('./escrow_account.teal', 'w') as f:
    compiled = compileTeal(escrow_account("A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I","7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU"), Mode.Application)
    f.write(compiled)





