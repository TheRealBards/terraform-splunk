output "splunk_instance_address" {
  description = "Splunk URL"
  value       = "https://${aws_instance.splunk-instance.public_ip}:${var.webserver-port-https}"
}

output "splunk_ec2_ip_address" {
  description = "Public EC2 IP address"
  value       = aws_instance.splunk-instance.public_ip
}