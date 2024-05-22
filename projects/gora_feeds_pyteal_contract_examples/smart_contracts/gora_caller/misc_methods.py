import sys
import beaker as BK
from pyteal import *
from typing import Union
from .inline_assembly import InlineAssembly
from gora_caller.config import GORA_CONTRACT_ID
from gora_caller.oracle_specs import BoxType,SourceSpec,DestinationSpec,REQUEST_METHOD_SPEC



def to_u16(i: Expr) -> Expr:
    return Suffix(Itob(i), Int(6))




def auth_dest_call(GORA_CONTRACT_ADDRESS_BIN:abi.Byte):
    """
        Confirm that current call to a destination app is coming from Gora.
    """

    return Seq(
        (caller_creator_addr := AppParam.creator(Global.caller_app_id())),
        smart_assert(caller_creator_addr.value() == GORA_CONTRACT_ADDRESS_BIN),
    )



def smart_assert(cond):
    """
        Assert with a number to indentify it in API error message. The message will be:
        "shr arg too big, (1000000%d)" where in "%d" is the line number.
    """

    err_line = sys._getframe().f_back.f_lineno # calling line number
    return If(Not(cond)).Then(
        InlineAssembly("int 0\nint {}\nshr\n".format(1000000 + err_line))
    )


@Subroutine(TealType.none)
def opt_in_asset(asset_id)->Expr:
    return Seq([
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: asset_id,
            TxnField.asset_receiver: Global.current_application_address(),
            TxnField.asset_amount: Int(0)
        }),
        InnerTxnBuilder.Submit()
    ])


@Subroutine(TealType.none)
def gora_opt_in(goracle_main_app_id)->Expr:
    return Seq([
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: goracle_main_app_id,
            TxnField.on_completion: OnComplete.OptIn,
        }),
        InnerTxnBuilder.Submit(),
    ])



def make_oracle_request(
        request_type : abi.Uint64, 
        request_key : abi.DynamicBytes, 
        requestSpec : abi.DynamicBytes, # RequestSpec | RequestSpecUrl | RequestSpecOffChain 
        destination_app_id :  abi.Uint64,
        destination_method : abi.DynamicBytes,
        user_data : abi.DynamicBytes, 
        box_references : abi.DynamicArray[BoxType], 
        app_references : abi.DynamicArray[abi.Uint64],
        asset_references : abi.DynamicArray[abi.Uint64], 
        account_references : abi.DynamicArray[abi.Address]
    ):
    
    """
        Make an oracle request with specified parameters.
    """

    return Seq(
        (request_type_abi := abi.Uint64()).set(request_type),
        (app_references := abi.make(abi.DynamicArray[abi.Uint64])).set([]),
        
        (asset_references := abi.make(abi.DynamicArray[abi.Uint64])).set([]),
        (account_references := abi.make(abi.DynamicArray[abi.Address])).set([]),
        
        (current_app_id := abi.make(abi.Uint64)).set(Global.current_application_id()),


        (data_box := abi.make(BoxType)).set(user_data,current_app_id),
        (box_references := abi.make(abi.DynamicArray[BoxType])).set([data_box]),
        (destination_app_id_abi := abi.Uint64()).set(destination_app_id or Global.current_application_id()),

        (dest := abi.make(DestinationSpec)).set(destination_app_id_abi, destination_method),
        (destination_abi := abi.DynamicBytes()).set(dest.encode()),


        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.MethodCall(
            app_id=Int(GORA_CONTRACT_ID),
            method_signature="request" + REQUEST_METHOD_SPEC,
            args=[ 
                requestSpec, 
                destination_abi, 
                request_type_abi, 
                request_key,
                app_references, 
                asset_references, 
                account_references, 
                box_references 
            ],
        ),
        InnerTxnBuilder.Submit(),
        
    )

