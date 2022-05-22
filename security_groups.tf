# Create SG for allowing TCP/8000 from * and TCP/22 from your IP in eu-west-1
resource "aws_security_group" "splunk_sg" {
  name        = "tf-splunk-sg"
  description = "Allow TCP/8000 & TCP/22"
  vpc_id      = aws_vpc.splunk_vpc.id
  ingress {
    description = "Allow 22 from our public IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.external_ip]
  }
  ingress {
    description = "Allow anyone on port 8000"
    from_port   = var.webserver-port
    to_port     = var.webserver-port
    protocol    = "tcp"
    cidr_blocks = [var.external_ip]
  }
  ingress {
    description = "Allow anyone on port 8443"
    from_port   = var.webserver-port-https
    to_port     = var.webserver-port-https
    protocol    = "tcp"
    cidr_blocks = [var.external_ip]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}