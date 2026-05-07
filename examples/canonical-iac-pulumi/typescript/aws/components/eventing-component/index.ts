import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface EventingArgs { environment: string; namePrefix: string }

export class EventingComponent extends pulumi.ComponentResource {
  public readonly queueArn: pulumi.Output<string>;
  constructor(name: string, args: EventingArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:aws:EventingComponent", name, {}, opts);
    const stack = pulumi.getStack();
    const dlq = new aws.sqs.Queue(`${args.namePrefix}-${args.environment}-${stack}-dlq`, {}, { parent: this });
    const queue = new aws.sqs.Queue(`${args.namePrefix}-${args.environment}-${stack}-main`, {
      redrivePolicy: dlq.arn.apply(arn => JSON.stringify({ deadLetterTargetArn: arn, maxReceiveCount: 5 })),
    }, { parent: this });
    this.queueArn = queue.arn;
    this.registerOutputs({ queueArn: this.queueArn });
  }
}
