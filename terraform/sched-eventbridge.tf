resource "aws_scheduler_schedule" "eventbridge" {
  name       = "eventbrdg-to-sns-to-lambdafunc-${var.function_name}"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(1 hours)"

  target {
    arn      = aws_sns_topic.default.arn
    role_arn = aws_iam_role.eventbridge.arn

    input = jsonencode({
      MessageBody = "{}"
    })

  }
}

resource "aws_iam_policy" "eventbridge" {
  name   = "eventbrdg-to-sns-to-lambdafunc-${var.function_name}"
  path   = "/"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "sns:Publish"
          ],
          "Resource": [
              "arn:aws:sns:*:${data.aws_caller_identity.current.account_id}:${aws_sns_topic.default.name}"
          ]
      }
  ]
}
EOF
}

resource "aws_iam_role" "eventbridge" {
  name               = "eventbrdg-to-sns-to-lambdafunc-${var.function_name}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Principal": {
              "Service": "scheduler.amazonaws.com"
          },
          "Action": "sts:AssumeRole",
          "Condition": {
              "StringEquals": {
                  "aws:SourceAccount": ${data.aws_caller_identity.current.account_id}
              }
          }
      }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "eventbridge" {
  role       = aws_iam_role.eventbridge.name
  policy_arn = aws_iam_policy.eventbridge.arn
}
