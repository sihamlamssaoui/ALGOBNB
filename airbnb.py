from pyteal import *

def contract_init():
	on_creation = Seq([
		App.globalPut(Bytes("Host"), Txn.sender()),
		Assert(Txn.application_args.length() == Int(7)),
		App.globalPut(Bytes("Guest"), Txn.application_args[0]),
		App.globalPut(Bytes("Rent"), Btoi(Txn.application_args[1])),
		App.globalPut(Bytes("H_deposit"), Btoi(Txn.application_args[2])),
		App.globalPut(Bytes("G_deposit"), Btoi(Txn.application_args[3])),
		App.globalPut(Bytes("myparam"), Txn.application_args[4]),
		App.globalPut(Bytes("Begin_stay"), Btoi(Txn.application_args[5])),
        	App.globalPut(Bytes("End_stay"), Btoi(Txn.application_args[6])),
		Return(Int(1))
		])

        ## verify if the host sent the right deposit
	is_h_deposit = Return(And(
        Gtxn[1].sender() == App.globalGet(Bytes("Host")),
        Gtxn[1].amount() == App.globalGet(Bytes("H_deposit"))
    	))

	## verify if the guest sent the right deposit 
	is_g_deposit = Return(And(
        Gtxn[1].sender() == App.globalGet(Bytes("Guest")),
        Gtxn[1].amount() == App.globalGet(Bytes("G_deposit"))
    	))

	## verify if the guest sent the right rent
	is_rent = Return(And(
        Gtxn[1].sender() == App.globalGet(Bytes("Guest")),
        Gtxn[1].amount() == App.globalGet(Bytes("Rent"))
    	))

	## check whether guest is in the house using "nuki" return 1 till implement it
	in_house = Int(1)

	## Check if the host is legible to cancel
	#is_h_cancel = And(
        	#Global.round() >= App.globalGet(Bytes("Begin_stay")),
        	#Global.round() <= App.globalGet(Bytes("End_stay")),
		#Txn.sender() == App.globalGet(Bytes("Host"))
    		#)
	is_h_cancel = Int(1) 

	## Host want to cancel, if is_h_cancel is true we should do an atomic transfer to the host and the guest
	h_cancel = If(is_h_cancel,
		Return(And(
		Gtxn[1].type_enum() == TxnType.Payment,
                Gtxn[2].type_enum() == TxnType.Payment,
        	#Gtxn[0].sender() == Gtxn[1].sender(),
        	#Gtxn[2].close_remainder_to() == Global.zero_address(),
        	Gtxn[1].receiver() == App.globalGet(Bytes("Host")),
        	Gtxn[2].receiver() == App.globalGet(Bytes("Guest")),
        	Gtxn[1].amount() == Int(0),
        	Gtxn[2].amount() == (App.globalGet(Bytes("Rent"))+ App.globalGet(Bytes("H_deposit")) + App.globalGet(Bytes("G_deposit"))) - Txn.fee())),
		Return(Int(0))
		)

	## Check if the Guest is legible to cancel
	is_g_cancel = And(
        	Global.round() > App.globalGet(Bytes("Begin_stay")),
        	Global.round() < App.globalGet(Bytes("End_stay")),
		Txn.sender() == App.globalGet(Bytes("Guest"))
    		)

	## Guest want to cancel, if is_g_cancel is true we should do an atomic transfer to the host and the guest
	g_cancel = If(is_g_cancel,
		Return(And(
		Gtxn[0].type_enum() == TxnType.Payment,
        	Gtxn[0].sender() == Gtxn[1].sender(),
        	Gtxn[0].close_remainder_to() == Global.zero_address(),
        	Gtxn[0].receiver() == App.globalGet(Bytes("Host")),
        	Gtxn[1].receiver() == App.globalGet(Bytes("Guest")),
        	Gtxn[1].amount() == App.globalGet(Bytes("Rent")),
        	Gtxn[0].amount() == App.globalGet(Bytes("H_deposit")) + App.globalGet(Bytes("G_deposit")))),
		Return(And(
        	Gtxn[0].sender() == Gtxn[1].sender(),
        	Gtxn[0].close_remainder_to() == Global.zero_address(),
        	Gtxn[0].receiver() == App.globalGet(Bytes("Host")),
        	Gtxn[1].receiver() == App.globalGet(Bytes("Guest")),
        	Gtxn[0].amount() == App.globalGet(Bytes("Rent")) /  Int(2) + App.globalGet(Bytes("H_deposit")),
        	Gtxn[1].amount() == App.globalGet(Bytes("G_deposit"))
		)))
 
	## check if guest is in house
	is_out_house = Int(1)
	
	complaint = Int(0)

	## check if the grace period is ended and if there is any complaint
	is_contract_ended = And(

        	Global.round() >= App.globalGet(Bytes("End_stay")),
		Txn.sender() == App.globalGet(Bytes("Host")), 
		is_out_house
    		)

	## send the right amount from escrow account to host and guest based on is_contract_ended result
	contract_ended = If(is_contract_ended, 
				Return(And(
        			Gtxn[0].sender() == Gtxn[1].sender(),
        			Gtxn[0].close_remainder_to() == Global.zero_address(),
        			Gtxn[0].receiver() == App.globalGet(Bytes("Host")),
        			Gtxn[1].receiver() == App.globalGet(Bytes("Guest")),
        			Gtxn[0].amount() == App.globalGet(Bytes("Rent")) /  Int(2) + App.globalGet(Bytes("H_deposit")),
        			Gtxn[1].amount() == App.globalGet(Bytes("G_deposit")))),
				Return(And(
        			Gtxn[0].sender() == Gtxn[1].sender(),
        			Gtxn[0].close_remainder_to() == Global.zero_address(),
        			Gtxn[0].receiver() == App.globalGet(Bytes("Host")),
        			Gtxn[1].receiver() == App.globalGet(Bytes("Guest")),
        			Gtxn[0].amount() == App.globalGet(Bytes("Rent")) /  Int(2) + App.globalGet(Bytes("H_deposit")) + App.globalGet(Bytes("G_deposit")),
        			Gtxn[1].amount() == Int(0))))

	is_update =If(Int(0) == Txn.application_id(), 
            App.globalPut(Bytes("Escrow"), Txn.application_args[0]), 
            Return(Int(1)))

	on_deletion = Return(Int(1))
	## check if the escrow account has 0 balance then delete app if needed
	#on_deletion = If(Int(0) == Txn.application_id(), 
         #   App.globalPut(Bytes("Host"), Txn.sender()), 
          #  Return(And(Txn.close_remainder_to() == App.globalGet(Bytes("Host")),
              #           Txn.receiver() == Global.zero_address(),
                #         Txn.amount() == Int(0))))
		
	## Host can only close out the contract if the grace period is ended
	on_closeout = If(
        And(Txn.sender() == App.globalGet(Bytes("Host")), Global.round() > App.globalGet(Bytes("End_stay"))),
        Return(Int(1)))

	## 
	OptIn =  Return(Int(1))
   
	program = Cond(
        	[Txn.application_id() == Int(0), on_creation],
		[Txn.on_completion() == OnComplete.DeleteApplication, on_deletion],
		[Txn.on_completion() == OnComplete.UpdateApplication, is_update],
		[Txn.on_completion() == OnComplete.CloseOut, on_closeout],
		[Txn.on_completion() == OnComplete.OptIn, OptIn],
        	[Bytes("send_rent") == Txn.application_args[0], is_rent],
		[Bytes("send_h_deposit") == Txn.application_args[0], is_h_deposit],
		[Bytes("send_g_deposit") == Txn.application_args[0], is_g_deposit],
		[Bytes("host_cancel") == Txn.application_args[0], h_cancel],
		[Bytes("guest_cancel") == Txn.application_args[0], g_cancel],
		[Bytes("end_grace_period") == Txn.application_args[0], contract_ended],
        	)

	return program


def clear_state_program():

    return Int(1)


with open('airbnb.teal', 'w') as f:
    compiled = compileTeal(contract_init(), Mode.Application)
    f.write(compiled)

with open('airbnb_clear.teal', 'w') as f:
        compiled = compileTeal(clear_state_program(), Mode.Application)
        f.write(compiled)
