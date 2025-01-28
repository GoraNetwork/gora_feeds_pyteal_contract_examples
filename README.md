# gora_feeds_pyteal_contract_examples

This project has been generated using AlgoKit. See below for default getting started instructions.

## Repository Breakdown

At first glance at the repository, you will see the `smart_contracts` folder, this contains every file we will need in this template.

`contracts` folder contains everything needed for a smart contract to make a request to the gora oracle.
Located in the `contracts` folder are the :

- `config.py` : This contains 2 constants `GORA_TOKEN_ID` and `GORA_CONTRACT_ID` which are to be filled with the Gora contract and token ID.

- `contract.py` : Contains our sample contract we use in calling and handling oracle responses.

- `inline_assembly.py` : Contains InlineAssembly which is used to inject TEAL source directly into a PyTEAL program.

- `misc_methods.py` : Contains helper methods which is utilized by our sample contract.

- `oracle_specs.py` : Contains a class of named tuples which is used to encode/decode the oracle response and requests.

`demo_configs` folder contains everything needed to test our sample smart contract.
Located in the `demo_configs` folder are the :

- `deploy_to_localnet.py` : Contains the neccessary preparations need to deploy the sample smart contract to localnet.

- `request_specs.py` : Contains the request paramenters for making a request to the oracle. these are the way request arguments are structured before sending a request.

`feed_examples` folder contains examples as to how to use the oracle for different use cases.
Located in the `feed_examples` folder are the :

- `setup.py` : Run `python3 setup.py` to setup the Gora localnet node for development.

- `custom_url_feed.py` : Contains the different ways you can make a custom oracle request.

- `flight_feed.py` : Contains the different ways you can make calls to the gora flight feeds.

- `pricepair_feed.py` : Contains the different ways you can use the price feed, you can even deploy your own price beacon.

- `sports_feed.py` : Contains the different ways you can use the gora sports feed in your contract.

- `weather_feeds.py` : Contains the different ways you can use the gora weather feed on your contract.

### NOTE : Follow the instructions at [Setup](#setup) section.

`gora_utils` folder contains the gora oracle contract ABI and some utility functions used in testing the contract.
Located in the `gora` folder are the :

- `abi.py` : Contains the gora oracle contract ABI.
- `utils.py` : Contains some utility functions used for deploying and testing the sample contract. this functions are gora specific that is why the are in the gora folder.

`helpers` This is an algokit generated folder, it contains functions for building and deploying a contract.
Located in the `helpers` folder are the :

- `build.py` : This contains the functions neccessary for converting (building) an pyteal code to proper teal code.

- `deploy.py` : This contains the functions neccessary for deploying the contract to the blockchain.

## Understanding The Gora Oracle

Gora is designed to be simple to use (plug-n-play), however I will drop somethings to note as a developer who have used gora in one of my projects.

There are 3 types of requests you can make with the gora oracle:

- _`Classic requests`_ : These are requests made to the gora feeds, these feeds are the ones provided by gora.

- _`custom or url based requests`_ : These are requests made to a thirdparty url, with gora you can setup your own feed using you company's own API.

- _`Offchain computation requests`_ : These are requests made to a node given a code to execute on chain.

For more details on how these requests work please check out the following resources:

[Gora Developer Quickstart](https://github.com/GoraNetwork/developer-quick-start)

[Gora Decentralized Oracle Documentation](https://github.com/GoraNetwork/.github/wiki/Gora-Decentralized-Oracle-Documentation)

## Prerequisites To Making A Call To The Gora Oracle

In order to make a call to the Gora oracle you need to have a couple of things in place these things include:

- You need to opt-in the calling contract to the Gora application.
- You need to opt-in the calling contract to the Gora token.
- You need some Algos to cover some box fees both for the calling contract and the Gora contract.
- You need some Gora to cover for calling costs to the Gora application.
- You need to stake/vest some Gora and Algo to the Gora application.

In this template you will be shown how each action can be done.

# Setup

### Pre-requisites

- [Python 3.10+](https://www.python.org/downloads/) (we recommended 3.12+)
- [Docker](https://www.docker.com/) (for LocalNet only)

> For interactive tour over the codebase, download [vsls-contrib.codetour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) extension for VS Code, then open the [`.codetour.json`](./.tours/getting-started-with-your-algokit-project.tour) file in code tour extension.

### Initial Setup

#### 1. Clone the Repository

Start by cloning this repository to your local machine.

#### 2. Install Pre-requisites

Ensure the following pre-requisites are installed and properly configured:

- **Docker**: Required for running a local Algorand network. [Install Docker](https://www.docker.com/).
- **AlgoKit CLI**: Essential for project setup and operations. Install the latest version from [AlgoKit CLI Installation Guide](https://github.com/algorandfoundation/algokit-cli#install). Verify installation with `algokit --version`, expecting `2.0.0` or later.

#### 3. Bootstrap Your Local Environment

Run the following commands within the project folder:

- **Install Poetry**: Required for Python dependency management. [Installation Guide](https://python-poetry.org/docs/#installation). Verify with `poetry -V` to see version `1.2`+.
- **Setup Project**: Execute `algokit project bootstrap all` to:
  - Install dependencies and setup a Python virtual environment in `.venv`.
  - Copy `.env.template` to `.env`.
- **Start LocalNet**: Use `algokit localnet start` to initiate a local Algorand network.

### Setup Gora Development Environment
To run test the example contracts provided in this repo.

- you need to run `python3 setup.py` located in the ```gora_feeds_pyteal_contract_examples/projects/gora_feeds_pyteal_contract_examples/smart_contracts
/feed_examples/```.
- create a `.env` file at ```gora_feeds_pyteal_contract_examples/projects
/gora_feeds_pyteal_contract_examples/``` directory.

- This `.env` will contain the following configurations
<pre>GORA_DEV_CLI_TOOL=/home/usr/gora_cli
GORA_DEV_CONFIG_FILE=/home/usr/gora_feeds_pyteal_contract_examples/.gora  </pre>

Replace the filepaths with the file paths of the .gora and gora_cli files generated when you executed `setup.py`



### Development Workflow

#### Terminal

Directly manage and interact with your project using AlgoKit commands:

1. **Build Contracts**: `algokit project run build` compiles all smart contracts.
2. **Deploy**: Use `algokit project deploy localnet` to deploy contracts to the local network.

#### VS Code

For a seamless experience with breakpoint debugging and other features:

1. **Open Project**: In VS Code, open the repository root.
2. **Install Extensions**: Follow prompts to install recommended extensions.
3. **Debugging**:
   - Use `F5` to start debugging.
   - **Windows Users**: Select the Python interpreter at `./.venv/Scripts/python.exe` via `Ctrl/Cmd + Shift + P` > `Python: Select Interpreter` before the first run.

#### JetBrains IDEs

While primarily optimized for VS Code, JetBrains IDEs are supported:

1. **Open Project**: In your JetBrains IDE, open the repository root.
2. **Automatic Setup**: The IDE should configure the Python interpreter and virtual environment.
3. **Debugging**: Use `Shift+F10` or `Ctrl+R` to start debugging. Note: Windows users may encounter issues with pre-launch tasks due to a known bug. See [JetBrains forums](https://youtrack.jetbrains.com/issue/IDEA-277486/Shell-script-configuration-cannot-run-as-before-launch-task) for workarounds.

## AlgoKit Workspaces and Project Management

This project supports both standalone and monorepo setups through AlgoKit workspaces. Leverage [`algokit project run`](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/project/run.md) commands for efficient monorepo project orchestration and management across multiple projects within a workspace.

> For guidance on `smart_contracts` folder and adding new contracts to the project please see [README](smart_contracts/README.md) on the respective folder.

# Tools

This project makes use of Python to build Algorand smart contracts. The following tools are in use:

- [Algorand](https://www.algorand.com/) - Layer 1 Blockchain; [Developer portal](https://developer.algorand.org/), [Why Algorand?](https://developer.algorand.org/docs/get-started/basics/why_algorand/)
- [AlgoKit](https://github.com/algorandfoundation/algokit-cli) - One-stop shop tool for developers building on the Algorand network; [docs](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md), [intro tutorial](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/tutorials/intro.md)
- [Beaker](https://github.com/algorand-devrel/beaker) - Smart contract development framework for PyTeal; [docs](https://beaker.algo.xyz), [examples](https://github.com/algorand-devrel/beaker/tree/master/examples)
- [PyTEAL](https://github.com/algorand/pyteal) - Python language binding for Algorand smart contracts; [docs](https://pyteal.readthedocs.io/en/stable/)
- [AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-py) - A set of core Algorand utilities that make it easier to build solutions on Algorand.
- [Poetry](https://python-poetry.org/): Python packaging and dependency management.

It has also been configured to have a productive dev experience out of the box in [VS Code](https://code.visualstudio.com/), see the [.vscode](./.vscode) folder.

- [AlgoKit Tealer Integration](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/tasks/analyze.md): AlgoKit Tealer Integration is a feature in the CLI that allows you to run [Tealer](https://github.com/crytic/tealer) static analyzer on your TEAL
  source code. The invocation of this command is included in:
- The github actions workflow file.
- A VSCode task ('Shift+CMD|CTRL+P' and search for 'Tasks: Run Task' and select 'Analyze TEAL contracts with AlgoKit Tealer integration').
- A `pre-commit` hook (if you have enabled `pre-commit` in your project).
