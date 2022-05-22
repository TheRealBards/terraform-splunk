provider "aws" {
  profile = var.profile
  region  = var.region
  default_tags {
    tags = {
      "therealbards:environment" = "test"
      "therealbards:managedby"   = "TF"
    }
  }
}

