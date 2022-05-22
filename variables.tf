variable "profile" {
  type    = string
  default = "default"
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "external_ip" {
  type    = string
  default = "0.0.0.0/0"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

variable "webserver-port" {
  type    = number
  default = 8000
}

variable "webserver-port-https" {
  type    = number
  default = 8443
}

variable "private_key_path" {
  type    = string
  default = "~/.ssh/id_rsa"
}

variable "public_key_path" {
  type    = string
  default = "~/.ssh/id_rsa.pub"
}