import beaker
from gora_caller.config import GORA_CONTRACT_ADDRESS_BIN
from pyteal import (abi,Expr,Seq,Int,Global,Bytes,Assert,Txn)

from gora_caller.oracle_specs import (ResponseBody,SourceSpec,BoxType,RequestSpec,
                                    RequestSpecUrl,RequestSpecOffChain,MyContractStore,
                                    SourceSpecOffChain,SourceSpecUrl
                                )
from gora_caller.misc_methods import (auth_dest_call,smart_assert,opt_in_asset,gora_opt_in,make_oracle_request)


app = beaker.Application(
    "CustomeGoraRequester",
    state=MyContractStore(),
    build_options=beaker.BuildOptions(avm_version=8))
app.apply(beaker.unconditional_opt_in_approval, initialize_local_state=True)




@app.external
def opt_in_assets(
    gora_token_reference: abi.Asset,
    gora_app_reference: abi.Application,
):
    """ OPTIN THE CONTRACT TO THE NATIVE TOKEN AND GORA CONTRACT """
    return Seq(
        Assert(Txn.sender() == Global.creator_address()),
        opt_in_asset(Txn.assets[0]),  # this is for the Gora token
        gora_opt_in(Txn.applications[1]),  # This is for the goracle main contract
        
    )



@app.external(read_only=True)
def return_oracle_response(user_data:abi.DynamicBytes,*, output: abi.DynamicBytes) -> Expr:
    """
        READ THE ORACLE RESPONSE, 
        THIS USES THE USER DATA AS THE KEY TO THE BOX BECAUSE WE USED THE USER 
        DATA AS THE KEY TO THE BOX WHEN SAVING THE ORACLE REPONSE .
    """

    return Seq(
        Assert(app.state.oracle_response[user_data.get()].exists()),
        app.state.oracle_response[user_data.get()].store_into(output)
    )

@app.external
def handle_oracle_response(resp_type: abi.Uint32,resp_body_bytes: abi.DynamicBytes):
    """ 
        THIS IS A SAMPLE DESTINATION METHOD, THIS SHOWS HOW THE RESPONSE FROM THE 
        ORACLE CAN BE SAVED/USED IN A SMART CONTRACT. 
        IN OUR CASE WE ONLY SAVE THE RESPONSE TO THE SMART CONTRACT

        USING A BOX STORAGE INSTEAD OF USING A LOCAL OR GLOBAL STORAGE,
        GIVES US THE FREEDOM TO RETURN ENTIRE JSON RESPONSE INSTEAD OF JUST A SINGLE JSON DATA VALU
    """

    
    return Seq(
        auth_dest_call(Bytes(GORA_CONTRACT_ADDRESS_BIN)),
        smart_assert(resp_type.get() == Int(1)),
        (resp_body := abi.make(ResponseBody)).decode(resp_body_bytes.get()),
        resp_body.oracle_value.store_into(
            oracle_value := abi.make(abi.DynamicBytes)
        ),
        (oracle_response := abi.make(abi.DynamicBytes)).decode(oracle_value.get()),
        resp_body.user_data.store_into(
            user_data := abi.make(abi.DynamicBytes)
        ),
        app.state.oracle_response[user_data.get()].set(oracle_response),

    )

@app.external
def send_classic_oracle_request(
        request_type : abi.Uint64, 
        request_key : abi.DynamicBytes, 
        sourceSpec : abi.DynamicArray[SourceSpec], 
        destination_app_id :  abi.Uint64,
        destination_method : abi.DynamicBytes, 
        aggregation_number : abi.Uint32, 
        user_data : abi.DynamicBytes, 
        box_references : abi.DynamicArray[BoxType], 
        app_references : abi.DynamicArray[abi.Uint64],
        asset_references : abi.DynamicArray[abi.Uint64], 
        account_references : abi.DynamicArray[abi.Address]
    
    )-> Expr:
    
    """
        Make an classic oracle request with specified parameters.
        This type of request are requests sent to the gora oracle for results from the oracle.
    """

    return Seq(
        

        (request_spec := abi.make(RequestSpec)).set(
            sourceSpec, aggregation_number, user_data,
        ),

        (requestSpec := abi.DynamicBytes()).set(request_spec.encode()), # TODO : check the request spec

        make_oracle_request(
            request_type,
            request_key,
            requestSpec,
            destination_app_id,
            destination_method,
            user_data,
            box_references,
            app_references,
            asset_references,
            account_references,
        )        
    )



@app.external
def send_custom_oracle_request(
        request_type : abi.Uint64, 
        request_key : abi.DynamicBytes, 
        sourceSpec : abi.DynamicArray[SourceSpecUrl], 
        destination_app_id :  abi.Uint64,
        destination_method : abi.DynamicBytes, 
        aggregation_number : abi.Uint32, 
        user_data : abi.DynamicBytes, 
        box_references : abi.DynamicArray[BoxType], 
        app_references : abi.DynamicArray[abi.Uint64],
        asset_references : abi.DynamicArray[abi.Uint64], 
        account_references : abi.DynamicArray[abi.Address]
    
    )-> Expr:
    
    """
        Make an custom oracle request with specified parameters.
        This type of request are requests sent to a custom url/api for results, 
        this url/api can include anything or it might even be a webpage.
    """

    return Seq(
        

        (request_spec := abi.make(RequestSpecUrl)).set(
            sourceSpec, aggregation_number, user_data,
        ),
        (requestSpec := abi.DynamicBytes()).set(request_spec.encode()), # TODO : check the request spec

        make_oracle_request(
            request_type,
            request_key,
            requestSpec,
            destination_app_id,
            destination_method,
            user_data,
            box_references,
            app_references,
            asset_references,
            account_references,
        )
    )




@app.external
def send_offchain_oracle_request(
        request_type : abi.Uint64, 
        request_key : abi.DynamicBytes, 
        sourceSpec : abi.DynamicArray[SourceSpecOffChain], 
        destination_app_id :  abi.Uint64,
        destination_method : abi.DynamicBytes, 
        aggregation_number : abi.Uint32, 
        user_data : abi.DynamicBytes, 
        box_references : abi.DynamicArray[BoxType], 
        app_references : abi.DynamicArray[abi.Uint64],
        asset_references : abi.DynamicArray[abi.Uint64], 
        account_references : abi.DynamicArray[abi.Address]
    
    )-> Expr:
    
    """
        Make an offchain oracle request with specified parameters.
        This type of request are requests sent to an off-chain service for results, 
    """

    return Seq(
        

        (request_spec := abi.make(RequestSpecOffChain)).set(
            sourceSpec, aggregation_number, user_data,
        ),

        (requestSpec := abi.DynamicBytes()).set(request_spec.encode()), # TODO : check the request spec

        make_oracle_request(
            request_type,
            request_key,
            requestSpec,
            destination_app_id,
            destination_method,
            user_data,
            box_references,
            app_references,
            asset_references,
            account_references,
        )
    )
