from pyteal import *


def initial_approval_program():
    on_creation = Return(Int(1))
    on_deletion = Return(Int(1))
    on_update = Return(Int(1))
    on_closeout = Return(Int(1))

    on_optin = Seq([App.localPut(Int(0), Bytes("address"), Txn.sender()),
                    Return(Int(1))])

    on_clear = Return(Int(1))

    get_address_of_sender = App.localGetEx(Int(0), App.id(), Bytes("address"))

    asa_allowed_address = Return(And(get_address_of_sender.hasValue(
    ), get_address_of_sender.value() == Gtxn[1].sender()))

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_deletion],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_optin],
        [Txn.on_completion() == OnComplete.ClearState, on_clear],
        [Txn.application_args[0] == Bytes(
            "asa_allowed_address"), asa_allowed_address]
    )

    return program


def clear_state_program():
    return Int(1)


with open('asa.teal', 'w') as f:
    compiled = compileTeal(initial_approval_program(), Mode.Application)
    f.write(compiled)

with open('asa_clear.teal', 'w') as f:
    compiled = compileTeal(clear_state_program(), Mode.Application)
    f.write(compiled)
