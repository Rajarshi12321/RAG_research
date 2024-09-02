resource "aws_instance" "Langchain_QA" {
  ami           = "ami-0f58b397bc5c1f2e8"  # Ubuntu 24.04 LTS AMI ID for ap-south-1, change accordingly
  instance_type = "t2.micro"
  tags = {
    Name = "Lang_QA"
  }

  # Open all traffic to the instance
  security_groups = ["default"]

  # Configure block device mapping
  root_block_device {
    volume_type           = "gp3"  # Change to the desired volume type, e.g., gp2
    volume_size           = 24     # Specify the size in GB
    delete_on_termination = true   # Set to false if you want to keep the volume after instance termination
  }
}

data "aws_security_group" "default" {
  for_each = aws_instance.Langchain_QA.security_groups

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

resource "aws_security_group_rule" "custom_tcp_ingress" {
  for_each = data.aws_security_group.default

  type                     = "ingress"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = each.value.id
}

resource "aws_ecr_repository" "Langchain_QA" {
  name = "langchain_qa"
  tags = {
    Name = "latest"
  }
}



output "ec2_public_ipv4" {
  description = "EC2 Public IP"
  value = aws_instance.Langchain_QA.public_ip
}

output "ecr_repository_uri" {
  description = "URI of ECR Repository"
  value = aws_ecr_repository.Langchain_QA.repository_url
}