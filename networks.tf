##############
## Get Data ##
##############

# Get a list of available availability zones
data "aws_availability_zones" "azs" {
  state = "available"
}

######################
## Create resources ##
######################

# Create a VPC in eu-west-1
resource "aws_vpc" "splunk_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "tf-splunk-vpc"
  }
}

# Create a Internet Gateway in eu-west-1
resource "aws_internet_gateway" "splunk_vpc_igw" {
  vpc_id = aws_vpc.splunk_vpc.id
}

# Create a subnet in eu-west-1
resource "aws_subnet" "splunk_subnet_1" {
  availability_zone = element(data.aws_availability_zones.azs.names, 0)
  vpc_id            = aws_vpc.splunk_vpc.id
  cidr_block        = "10.0.1.0/24"
}

# Create a route table in eu-west-1
resource "aws_route_table" "splunk_internet_route" {
  vpc_id = aws_vpc.splunk_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.splunk_vpc_igw.id
  }
  lifecycle {
    ignore_changes = all
  }
  tags = {
    Name = "tf-splunk-RT"
  }
}

# Overwrite default route table of VPC with our route table entries
resource "aws_main_route_table_association" "set-master-default-rt-assoc" {
  vpc_id         = aws_vpc.splunk_vpc.id
  route_table_id = aws_route_table.splunk_internet_route.id
}