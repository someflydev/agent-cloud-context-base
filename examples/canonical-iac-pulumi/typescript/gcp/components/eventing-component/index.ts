import * as pulumi from "@pulumi/pulumi";

export interface EventingArgs { environment: string; namePrefix: string }

export class EventingComponent extends pulumi.ComponentResource {
  public readonly topicName: pulumi.Output<string>;
  constructor(name: string, args: EventingArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:gcp:EventingComponent", name, {}, opts);
    const stack = pulumi.getStack();
    this.topicName = pulumi.output(`${args.namePrefix}-${args.environment}-${stack}-events`);
    this.registerOutputs({ topicName: this.topicName });
  }
}
