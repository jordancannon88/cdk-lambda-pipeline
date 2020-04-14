from aws_cdk import (
    core,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_events_targets as targets
)

# Emails for receiving alerts.
notification_emails = [
    'jocannon@1strategy.com',
]


class SnsStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs):
        super().__init__(app, id, **kwargs)

        # [ SNS ] Topic:
        #
        # - The error topic for all issues.

        topic = sns.Topic(self, 'Topic', display_name='Pipeline Alert')

        # [ SNS ] Topic:
        #
        # - The error topic for all issues.

        sns_target = targets.SnsTopic(topic)

        # [ SNS ] Subscription:
        #
        # - Takes all emails in the list and creates email subscriptions for each.

        for email in notification_emails:
            topic.add_subscription(
                sns_subscriptions.EmailSubscription(
                    email_address=email
                )
            )

        # [ SNS ]
        #
        #

        self.sns_target = sns_target
