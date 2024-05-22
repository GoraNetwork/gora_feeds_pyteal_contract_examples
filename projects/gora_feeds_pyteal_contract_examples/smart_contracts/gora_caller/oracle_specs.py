from pyteal import abi
from typing import Literal as L
from beaker.lib.storage import BoxMapping


REQUEST_METHOD_SPEC = "(byte[],byte[],uint64,byte[],uint64[],uint64[],address[],(byte[],uint64)[])void"


# Storage box specification.
class BoxType(abi.NamedTuple):
    key: abi.Field[abi.DynamicBytes]
    app_id: abi.Field[abi.Uint64]

    
# Oracle source specification
class SourceSpec(abi.NamedTuple):
    source_id: abi.Field[abi.Uint32]
    source_arg_list: abi.Field[abi.DynamicArray[abi.DynamicBytes]]
    max_age: abi.Field[abi.Uint32]

# Oracle source specification for General URL (type #2) requests.
class SourceSpecUrl(abi.NamedTuple):
    url: abi.Field[abi.DynamicBytes]
    auth_url: abi.Field[abi.DynamicBytes]
    value_expr: abi.Field[abi.DynamicBytes]
    timestamp_expr: abi.Field[abi.DynamicBytes]
    max_age: abi.Field[abi.Uint32]
    value_type: abi.Field[abi.Uint8]
    round_to: abi.Field[abi.Uint8]
    gateway_url: abi.Field[abi.DynamicBytes]
    reserved_0: abi.Field[abi.DynamicBytes]
    reserved_1: abi.Field[abi.DynamicBytes]
    reserved_2: abi.Field[abi.Uint32]
    reserved_3: abi.Field[abi.Uint32]

# Oracle source specification for off-chain (type #3) requests.
class SourceSpecOffChain(abi.NamedTuple):
    api_version: abi.Field[abi.Uint32] # Minimum off-chain API version required
    spec_type: abi.Field[abi.Uint8] # executable specification type:
                                          # 0 - in-place code,
                                          # 1 - storage box (8-byte app ID followed by box name)
                                          # 2 - URL
    exec_spec: abi.Field[abi.DynamicBytes] # executable specification
    exec_args: abi.Field[abi.DynamicArray[abi.DynamicBytes]] # input arguments
    reserved_0: abi.Field[abi.DynamicBytes] # reserved for future use
    reserved_1: abi.Field[abi.DynamicBytes]
    reserved_2: abi.Field[abi.Uint32]
    reserved_3: abi.Field[abi.Uint32]

# Oracle classic request specification.
class RequestSpec(abi.NamedTuple):
    source_specs: abi.Field[abi.DynamicArray[SourceSpec]]
    aggregation: abi.Field[abi.Uint32]
    user_data: abi.Field[abi.DynamicBytes]

# Oracle general URL (type #2) request specification.
class RequestSpecUrl(abi.NamedTuple):
    source_specs: abi.Field[abi.DynamicArray[SourceSpecUrl]]
    aggregation: abi.Field[abi.Uint32]
    user_data: abi.Field[abi.DynamicBytes]

# Oracle off-chain (type #3) request specification.
class RequestSpecOffChain(abi.NamedTuple):
    source_specs: abi.Field[abi.DynamicArray[SourceSpecOffChain]]
    aggregation: abi.Field[abi.Uint32]
    user_data: abi.Field[abi.DynamicBytes]

# Specification of destination called by the oracle when returning data.
class DestinationSpec(abi.NamedTuple):
    app_id: abi.Field[abi.Uint64]
    method: abi.Field[abi.DynamicBytes]

# Oracle response body.
class ResponseBody(abi.NamedTuple):
    request_id: abi.Field[abi.StaticBytes[L[32]]]
    requester_addr: abi.Field[abi.Address]
    oracle_value: abi.Field[abi.DynamicBytes]
    user_data: abi.Field[abi.DynamicBytes]
    error_code: abi.Field[abi.Uint32]
    source_errors: abi.Field[abi.Uint64]


# oracle game odds reponse body
class SportsResponseBody(abi.NamedTuple):
    startTime : abi.Field[abi.Uint64]
    status : abi.Field[abi.Uint64]
    homeTeamName : abi.Field[abi.String]
    awayTeamName : abi.Field[abi.String]
    homeTeamScore : abi.Field[abi.Uint64]
    awayTeamScore : abi.Field[abi.Uint64]
    homeMoneyLine : abi.Field[abi.Uint64]
    awayMoneyLine : abi.Field[abi.Uint64]
    drawMoneyLine : abi.Field[abi.Uint64]


# A STATEFUL 
class MyContractStore:
    oracle_response = BoxMapping(abi.DynamicBytes, abi.DynamicBytes)  # This is a key value pair of the oracle response
