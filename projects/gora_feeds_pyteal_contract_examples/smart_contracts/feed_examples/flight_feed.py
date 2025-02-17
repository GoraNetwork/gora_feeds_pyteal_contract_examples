import os,sys,json,time
import beaker as BK
from pathlib import Path
import algokit_utils,uuid
from dotenv import load_dotenv
load_dotenv()
sys.path.append(f"{Path(__file__).parent.parent}")
from gora import cfg_path,is_dev_nr_running,run_cli
from demo_configs.request_specs import flightDataSource
from gora_caller.config import GORA_CONTRACT_ID,GORA_TOKEN_ID
from demo_configs.deploy_to_localnet import deploy_to_localnet
from gora_utils.utils import fund_account,stake_algo_for_requests,stake_gora_for_requests,get_gora_box_name,ALGOD_CLIENT



"""
    THIS SIMPLE EXAMPLE SHOWS HOW TO MAKE A CLASSIC REQUEST TO THE ORACLE FOR SOME INFO PARTAINING TO A FLIGHT
    TO SEE THE INFO USED AS THE ARGUMENTS/PARAMETER SEE "from demo_configs.request_specs import flightDataSource".

    THIS HANDLES THE ORACLE SPECIFICATIONS FOR A CLASSIC FLIGHT DATA REQUEST.
    
"""

owner = BK.localnet.get_accounts()[0]
requestContract,requestContractID,requestContractAddress = deploy_to_localnet(owner)


fund_account(owner.address, 1_000_000_000_000)
fund_account(requestContractAddress, 1_000_000_000_000)


print("OPTING INTO GORA AND GORA TOKEN")
requestContract.call(
    "opt_in_assets",
    gora_token_reference=GORA_TOKEN_ID,
    gora_app_reference=GORA_CONTRACT_ID,
)

print("STAKING SOME GORA AND ALGO TO THE GORA CONTRACT")
deposit_amount = 10_000_000_000
stake_algo_for_requests(
    ALGOD_CLIENT,
    owner,
    deposit_amount,
    requestContractAddress,
    GORA_CONTRACT_ID
)

stake_gora_for_requests(
    ALGOD_CLIENT,
    owner,
    deposit_amount,
    requestContractAddress,
    GORA_CONTRACT_ID,
    GORA_TOKEN_ID
)
print("STAKED GORA AND ALGO TO THE GORA CONTRACT")


""" MAKE AN ORACLE CALL TO GORACLE """
print("MAKING A CLASSIC ORACLE REQUEST")
req_key = uuid.uuid4().bytes
user_data = b"SOMETHING_RANDOM" 
box_name = get_gora_box_name(req_key,requestContractAddress)

# A GORA SOURCE SPECIFICATION IS A LIST CONSISTING OF THE SOURCE ID, 
# THE QUERY ARGUMENTS AND THE AGGREGATION NUMBER WHICH IS JUST 0 to N WITH ZERO DENOTING MAXIMUM RESULTS AGE
# THE SOURCE SPECIFICATION ARE IN THE FORM [int,[byte,byte.......,byte],int]
sourceSpec = [
    flightDataSource.get("sourceId"), # Source ID
    flightDataSource.get("queryArgs") , # Query arguments
    0 # Maximum result age (0 - no limit)
],

try:
    result = requestContract.call(
        "send_classic_oracle_request",
        request_type = 1,
        request_key=req_key,
        sourceSpec=sourceSpec,
        destination_app_id = requestContractID,
        destination_method = b"handle_oracle_response",
        aggregation_number = 0,
        user_data=user_data,
        box_references=[],
        app_references=[],
        asset_references=[],
        account_references=[],

        transaction_parameters=algokit_utils.OnCompleteCallParameters(
            foreign_apps=[ GORA_CONTRACT_ID ],
            boxes=[ (GORA_CONTRACT_ID, box_name),(GORA_CONTRACT_ID, user_data), ],
        ),
    )
    print("REQUEST SENT")
    print(f"Confirmed in round: {result.confirmed_round}")
    print(f"Top txn ID: {result.tx_id}\n")

    # WE HAVE SENT THE REQUEST, NOW STARTUP THE LOCAL GORA NODE AND VIEW THE REQUEST.
    # NOTE : YOU WOULD NOT NEED TO DO THIS IN PRODUCTION/MAINNET

    if is_dev_nr_running():
        print("Detected development Gora node running in the background")
    else:
        print("Background development Gora node not detected, running one temporarily")
        run_cli("docker-start", [], {
            "GORA_CONFIG_FILE": cfg_path,
            "GORA_DEV_ONLY_ROUND": str(result.confirmed_round),
        }, True)

    print("\nWaiting for for oracle return value (up to 5 seconds)\n")
    time.sleep(10)
except Exception as e:
    print(f"Oracle couldn't process request because ::: {e}")


# READ THE RESPONSE RETURNED BY GORACLE
try:
    value = requestContract.call(
        "return_oracle_response",
        user_data=user_data,
        transaction_parameters=algokit_utils.OnCompleteCallParameters(
            signer=owner.signer,
            sender=owner.address,
            boxes=[(requestContractID, user_data)],
        ),
    )
    gora_value = value.raw_value

    decoded_response = gora_value.decode('utf-8')
    decoded_response = json.loads(decoded_response) # IN THE SOURCE SPEC IF WE USED b"$.data" instead of b"$.data.awayTeamScore" 
    # THIS WILL RETURN THE ENTIRE JSON RESPONSE FROM THE ORACLE THAN A SINGLE DATA VALUE
    print(f"DECODED RAW JSON DATA RETURNED BY THE ORACLE : {decoded_response}")
except Exception as e:
    print(f"Oracle returned no data becuase ::: {e}")
