GORACLE_ABI = {
  "name": "GoracleMain",
  "networks": {
    "default": {
      "appID": 1
    }
  },
  "methods": [
    {
      "name": "init",
      "desc": "initialize the contract",
      "args": [
        { "name": "token", "type": "asset" },
        { "name": "manager", "type": "address" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "update_protocol_settings",
      "desc": "a hook to change settings for the goracle protocol",
      "args": [
        { "name": "manager_address", "type": "address" },
        { "name": "refund_request_made_percentage", "type": "uint64" },
        { "name": "refund_processing_percentage", "type": "uint64" },
        { "name": "algo_request_fee", "type": "uint64" },
        { "name": "gora_request_fee", "type": "uint64" },
        { "name": "voting_threshold", "type": "uint64" },
        { "name": "time_lock", "type": "uint64" },
        { "name": "vote_refill_threshold", "type": "uint64" },
        { "name": "vote_refill_amount", "type": "uint64" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "request",
      "desc": "Request an oracle response",
      "args": [
        { "name": "request_args", "type": "byte[]", "desc": "includes source ID and source args" },
        { "name": "destination", "type": "byte[]", "desc": "includes app ID and method signature" },
        { "name": "type", "type": "uint64", "desc": "request type" },
        { "name": "key", "type": "byte[]", "desc": "request key, this is used to access the request box, the box will be named Sha512_256(Concat(<REQUSTER_ADDR>, <KEY>))" },
        { "name": "app_refs", "type": "uint64[]", "desc": "list of app references to pass through to destination" },
        { "name": "asset_refs", "type": "uint64[]", "desc": "list of asset references to pass through to destination" },
        { "name": "account_refs", "type": "address[]", "desc": "list of account references to pass through to destination" },
        { "name": "box_refs", "type": "(byte[],uint64)[]", "desc": "list of box references to pass through to destination" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "register_participation_account",
      "desc": "",
      "args": [
        { "name": "public_key", "type": "address" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "unregister_participation_account",
      "desc": "",
      "args": [],
      "returns": { "type": "void" }
    },
    {
      "name": "stake",
      "desc": "Stake tokens to participate",
      "args": [
        { "name": "token_txn", "type": "axfer" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "unstake",
      "desc": "Unstake tokens to participate",
      "args": [
        { "name": "unstake_amount", "type": "uint64" },
        { "name": "application_token", "type": "asset" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "deposit_token",
      "desc": "Deposit tokens to pay for services",
      "args": [
        { "name": "token_txn", "type": "axfer" },
        { "name": "application_token", "type": "asset" },
        { "name": "account_to_deposit_to", "type": "account" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "deposit_algo",
      "desc": "Deposit algorand to help cover fees",
      "args": [
        { "name": "algorand_txn", "type": "pay" },
        { "name": "account_to_deposit_to", "type": "account" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "withdraw_token",
      "desc": "Withdraw deposited tokens",
      "args": [
        { "name": "withdraw_amount", "type": "uint64" },
        { "name": "application_token", "type": "asset" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "withdraw_algo",
      "desc": "Withdraw deposited algo",
      "args": [
        { "name": "withdraw_amount", "type": "uint64" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "claim_rewards",
      "desc": "claims fees and rewards for voting",
      "args": [
        { "name": "rewards_address", "type": "account" },
        { "name": "previous_vote", "type": "byte[129]" },
        { "name": "previous_vote_requester", "type": "account" },
        { "name": "voting_contract", "type": "application" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "deploy_voting_contract",
      "desc": "deploys voting contracts",
      "args": [
        { "name": "algo_xfer", "type": "pay" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "refund_request",
      "desc": "refunds a request when a request was not processed in time",
      "args": [
        { "name": "requester", "type": "account" },
        { "name": "request_key_hash", "type": "byte[32]" }
      ],
      "returns": { "type": "void" }
    },
    {
      "name": "update_request_status",
      "desc": "voting app updates a requests status when request has completed",
      "args": [
        { "name": "voting_contract", "type": "application" },
        { "name": "request_key_hash", "type": "byte[32]" },
        { "name": "status", "type": "string" },
        { "name": "requester", "type": "account" },
        { "name": "proposal_bytes", "type": "byte[56]" }
      ],
      "returns": { "type": "(byte[32],uint64,uint64,uint64,uint64,byte[32])" }
    },
    {
      "name": "claim_rewards_vote_verify",
      "desc": "Method for verification logic sig AND claiming rewards for previous vote",
      "args": [
        { "name": "vrf_result", "type": "byte[64]" },
        { "name": "vrf_proof", "type": "byte[80]" },
        { "name": "request_round_seed", "type": "byte[32]" },
        { "name": "participation_account", "type": "account" },
        { "name": "main_account", "type": "account" },
        { "name": "voting_address", "type": "account" },
        { "name": "voting_app", "type": "application" },
        { "name": "request_key_hash", "type": "byte[32]" },
        { "name": "previous_vote", "type": "byte[88]" },
        { "name": "previous_vote_requester", "type": "account" }
      ],
      "returns": { "type": "void" }
    }
  ]
}
