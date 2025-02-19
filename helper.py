"""Custom helper module for handling a VM."""

__author__ = "Jeyakumar, Shankar Kumar"
__credits__ = [
    "https://github.com/azure-samples/virtual-machines-python-manage/blob/master/example.py",
]

import argparse

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient

import paramiko


class VMManager:
    """Doc string."""

    def __init__(self):
        AZURE_SUBSCRIPTION_ID = ""
        AZURE_CLIENT_ID = ""
        AZURE_CLIENT_SECRET = ""
        AZURE_TENANT_ID = ""

        credentials = ServicePrincipalCredentials(
            client_id=AZURE_CLIENT_ID,
            secret=AZURE_CLIENT_SECRET,
            tenant=AZURE_TENANT_ID,
        )
        self.compute_client = ComputeManagementClient(
            credentials, AZURE_SUBSCRIPTION_ID
        )

        self.GROUP_NAME = ""

    def list_vms(self):
        """Doc string."""

        print("\nList VMs in subscription")
        for vm in self.compute_client.virtual_machines.list_all():
            print("VM: {}".format(vm.name))

    def start_vm(self, VM_NAME):
        """Doc string."""

        # Start the VM
        print("\nStart VM")
        async_vm_start = self.compute_client.virtual_machines.start(
            self.GROUP_NAME, VM_NAME
        )
        async_vm_start.wait()
        print("'{}' started.".format(VM_NAME))

    def restart_vm(self, VM_NAME):
        """Doc string."""

        # Restart the VM
        print("\nRestart VM")
        async_vm_restart = self.compute_client.virtual_machines.restart(
            self.GROUP_NAME, VM_NAME
        )
        async_vm_restart.wait()
        print("'{}' restarted.".format(VM_NAME))

    def stop_vm(self, VM_NAME):
        """Doc string."""

        # Stop the VM
        print("\nStop VM")
        async_vm_stop = self.compute_client.virtual_machines.power_off(
            self.GROUP_NAME, VM_NAME
        )
        async_vm_stop.wait()
        print("'{}' stopped.".format(VM_NAME))

    def get_vm(self, VM_NAME):
        """Doc string."""

        # Fetch the VM
        return self.compute_client.virtual_machines.get(
            self.GROUP_NAME, VM_NAME
        )

    def establish_ssh_connection_to_vm(
        self, public_ip, port, username, key_path
    ):
        """Doc string."""

        k = paramiko.RSAKey.from_private_key_file(key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=public_ip, port=port, username=username, pkey=k)
        return ssh

    def run_ssh_command_on_vm(self, ssh, command):
        """Doc string."""

        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        print("Command run completed.")


if __name__ == "__main__":
    my_vm_manager = VMManager()
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--vm_name", required=True)
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["start-vm", "stop-vm", "start-container"],
    )
    parser.add_argument("-ip", "--public_ip", default=None)
    parser.add_argument("-po", "--port", default=None)
    parser.add_argument("-us", "--username", default=None)
    parser.add_argument("-kp", "--key_path", default=None)
    parser.add_argument("-cn", "--container_name", default=None)
    args = parser.parse_args()

    action = args.action
    vm_name = args.vm_name

    if action == "start-vm":
        my_vm_manager.start_vm(vm_name)

    if action == "stop-vm":
        my_vm_manager.stop_vm(vm_name)

    if action == "start-container":
        public_ip = args.public_ip
        port = args.port
        username = args.username
        key_path = args.key_path
        container_name = args.container_name

        if public_ip and port and username and key_path:
            print("Establishing SSH connection.")
            ssh = my_vm_manager.establish_ssh_connection_to_vm(
                public_ip, port, username, key_path
            )
            if container_name:
                print("Starting container '{}'.".format(container_name))
                command = """sudo docker start {}""".format(container_name)
                my_vm_manager.run_ssh_command_on_vm(ssh=ssh, command=command)
            else:
                print("'container_name' must be specified.")
        else:
            print(
                "'public_ip', 'port', 'username' and 'key_path' are necesssary to establish a SSH connection."
            )
