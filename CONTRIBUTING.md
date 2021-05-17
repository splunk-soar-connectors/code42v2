## Set up your development environment

You'll need a Phantom OVA VM image to run this application. To download the image, first register [here](https://my.phantom.us/signup/)
to create a Phantom account. Phantom will approve your registration and send you credentials for https://my.phantom.us.

Next, log in and go [here](https://my.phantom.us/downloads/) to download the Phantom VM image.

Follow these [instructions](https://docs.splunk.com/Documentation/Phantom/4.10.3/Install/InstallOVA) to install Splunk Phantom 
as a VM image. Use these [default credentials](https://docs.splunk.com/Documentation/Phantom/4.10.3/Install/Reference) to log in.
Confirm that you can connect to the VM via SSH on your host machine. You can use `hostname -I` on the remote machine to look up your IP address.
Also confirm that you can access the Phantom web app at `https://{phantom VM IP address}`.

NOTE: If you are consistently getting timeouts connecting to the Phantom VM, try disconnecting from the VPN and re-attempting.


## Deploying the app

Run the below command to install the Code42 app on Phantom. 

```bash
export PHANTOM_VM_IP_ADDR=0.0.0.0 # Replace with IP address for Phantom VM
./util.sh move
```

Open the Phantom web app and login as the `admin` user. Navigate to `Apps > Unconfigured Apps` and find the Code42 App.
Click Configure New Asset to supply the Console URL, username, and password to connect with. Fill out the fields in Asset Info
and Asset Settings. Save the Asset Configuration and then click Test Connectivity to test your connection. 

## Creating a virtual environment

To run the unit tests you will need to create a Python virtual environment for the Phantom app and its dependencies.

Install `pyenv` and `pyenv-virtualenv` via [homebrew](https://brew.sh/):

```bash
brew install pyenv pyenv-virtualenv
```

After installing `pyenv` and `pyenv-virtualenv`, be sure to add the following entries to your `.zshrc` (or `.bashrc` if you are using bash) and restart your shell:

```bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Then, create your virtual environment.

```bash
pyenv install 3.6.13
pyenv virtualenv 3.6.13 phantom
pyenv activate phantom
```

Use `source deactivate` to exit the virtual environment and `pyenv activate phantom` to reactivate it.

## Running the tests

Make sure you have created a Python virtual environment for the Phantom project as described above.

Then, activate the virtual environment and install the dependencies before running the tests.

```bash
pip install -e phantomstubs
pip install -e .
pytest
```

# TODO

When we implement actions, describe how to create dummy events in the UI and test the actions via a playbook.


