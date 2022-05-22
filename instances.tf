##############
## Get Data ##
##############

# Get Linux AMI ID using SSM Parameter endpoint in eu-west-1
data "aws_ssm_parameter" "linuxAmi" {
  name = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
}


######################
## Create resources ##
######################

# Create a key-pair for logging in to the EC2
resource "aws_key_pair" "splunk-key" {
  key_name   = "tf-splunk-key"
  public_key = file(var.public_key_path)
}

# Create EC2 instance
resource "aws_instance" "splunk-instance" {
  ami                         = data.aws_ssm_parameter.linuxAmi.value
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.splunk-key.key_name
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.splunk_sg.id]
  subnet_id                   = aws_subnet.splunk_subnet_1.id
  tags = {
    Name = "tf-splunk"
  }
  depends_on = [
    aws_main_route_table_association.set-master-default-rt-assoc
  ]
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(var.private_key_path)
    host        = self.public_ip
  }

  provisioner "file" {
    source      = "files/install.sh"
    destination = "/tmp/install.sh"
  }

  provisioner "file" {
    source      = "files/splunk.py"
    destination = "/tmp/splunk.py"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install.sh",
      "/bin/bash /tmp/install.sh"
    ]
  }
}