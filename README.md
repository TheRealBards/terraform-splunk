![](https://www.logolynx.com/images/logolynx/81/81ca623fa5dbc14b9076ffa9f1f2e11e.png "Splunk")
# Terraform Splunk

This repository can be used to create a single node instance of Splunk. If you're working an incident and need to ingest some data to make life a little easier, or you just want to mess around, this could be of help.

I've mostly created this because I want to learn more about Terraform. I intend to update the provisioner to Ansible at some point.

## What it does?

It will create a the below resources:

* AWS VPC, Subnet, Internet Gateway ,Route table
* AWS Security Groups
* AWS EC2 instance, SSH key pair

## Expected Variables

This repository uses an AWS S3 backend that is configured in backend.tf. I recommend updating the bucket name or alternatively, store the Terraform statefile locally instead.

There are defaults set, however, I recommend updating them in variables.tf

* profile
* region
* external_ip
* instance_type
* webserver-port
* webserver-port-https
* private_key_path

## Deployment

```
git clone https://github.com/TheRealBards/terraform-splunk.git
cd terraform-splunk
terraform init
terraform validate
terraform apply
```

Once Terraform has completed the build, it will output the Splunk admin password (also stored locally on the server in `/home/ec2-user/splunk_password`).

# Feedback

All feedback is welcome! Feel free to submit an issue if something's not working.