from aws_cdk import core
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.aws_ec2 import (
    Vpc,
    SecurityGroup,
    Instance,
    Peer,
    Port,
    MachineImage,
    InstanceType,
    SubnetConfiguration,
    SubnetType,
    BlockDeviceVolume,
    BlockDevice,
    UserData,
)


class OpenedxNativeStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        setup_script_path: str,
        install_script_path: str,
        ssh_allowed_ip: str,
        key_name: str,
        ami_id: str = "ami-0b48089553c9d7962",
        instance_type: str = "t2.large",
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.ami_id = ami_id
        self.setup_script = setup_script_path
        self.install_script = install_script_path
        self.ssh_allowed_ip = "{}/32".format(ssh_allowed_ip)

        # Create a new VPC
        vpc = Vpc(
            self,
            id="{}-vpc".format(id),
            nat_gateways=0,
            subnet_configuration=[
                SubnetConfiguration(
                    name="{}-public".format(id), subnet_type=SubnetType.PUBLIC
                )
            ],
        )

        # Create a new security group
        security_group = SecurityGroup(
            self,
            id="{}-sg".format(id),
            vpc=vpc,
            security_group_name="{}-sg".format(id),
            allow_all_outbound=True,
        )
        # TODO Make the IP rule configurable
        security_group.add_ingress_rule(
            peer=Peer.ipv4(self.ssh_allowed_ip),
            connection=Port.tcp(22),
            description="Allow ssh from internet",
        )

        security_group.add_ingress_rule(
            peer=Peer.ipv4(self.ssh_allowed_ip),
            connection=Port.tcp_range(18000, 18999),
            description="Allow access to open edX services",
        )

        security_group.add_ingress_rule(
            peer=Peer.ipv4(self.ssh_allowed_ip),
            connection=Port.tcp(80),
            description="Allow http from internet",
        )

        # Select the AMI
        ami = MachineImage.generic_linux({self.region: self.ami_id})

        # Create Volume
        ebs = BlockDevice(
            device_name="/dev/sda1",
            volume=BlockDeviceVolume.ebs(50, delete_on_termination=True),
            mapping_enabled=True,
        )

        # Create the Instance
        openedx = Instance(
            self,
            id=id,
            instance_name="{}-instance".format(id),
            instance_type=InstanceType(instance_type),
            machine_image=ami,
            vpc=vpc,
            security_group=security_group,
            key_name=key_name,
            block_devices=[ebs],
        )

        # TODO write LMS and CMS bases using variables
        with open(self.setup_script) as f:
            setup_script = f.read()

        openedx.user_data.add_commands(setup_script)

        # Script in S3 as Asset
        # asset = Asset(self, id="{}-asset".format(id), path=self.setup_script)

        # local_path = openedx.user_data.add_s3_download_command(
        #    bucket=asset.bucket, bucket_key=asset.s3_object_key
        # )
        # asset.grant_read(openedx.role)

        # openedx.user_data.add_execute_file_command(file_path=local_path)

        core.CfnOutput(self, "{}-output".format(id), value=openedx.instance_public_ip)
