from pathlib import Path
import sys,algokit_utils
from helpers.build import build
from gora_caller.contract import app
from gora_utils.utils import ALGOD_CLIENT


# "/" for linux "\" for windows
if "win" in str(sys.platform):
    system_delima = "\\"
else:
    system_delima = "/"

default_app_path = Path(f"artifacts{system_delima}")
absolute_app_path = f"{Path(__file__).parent.parent}{system_delima}"


def deploy_to_localnet(deployer):
    """THIS DEPLOYS THE TEST CONTRACT ON YOUR LOCALNET NORMAL ALGORAND CONTRACT DEPLOYMENT PROCESSES STILL APPLY"""

    build(default_app_path,app)
    app_spec_path = Path(f"{default_app_path.resolve()}{system_delima}application.json")


    requestContract = algokit_utils.ApplicationClient(
        algod_client=ALGOD_CLIENT,
        app_spec=app_spec_path,
        signer=deployer,
    )

    requestContract.create()
    requestContract.opt_in()
    print(
        f"CONTRACT SUCCESFULLY DEPLOYED\n\nCONTRACT ID :: {requestContract.app_id} \nCONTRACT ADDRESS :: {requestContract.app_address}"
    )

    return(requestContract,requestContract.app_id,requestContract.app_address)
