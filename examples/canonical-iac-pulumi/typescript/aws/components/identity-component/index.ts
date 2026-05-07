import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface IdentityArgs {
  environment: string;
  namePrefix: string;
  bucketArn: pulumi.Input<string>;
  queueArn: pulumi.Input<string>;
  secretArn: pulumi.Input<string>;
}

export class IdentityComponent extends pulumi.ComponentResource {
  public readonly roleArn: pulumi.Output<string>;
  constructor(name: string, args: IdentityArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:aws:IdentityComponent", name, {}, opts);
    const stack = pulumi.getStack();
    const role = new aws.iam.Role(`${args.namePrefix}-${args.environment}-${stack}-role`, {
      assumeRolePolicy: JSON.stringify({ Version: "2012-10-17", Statement: [{ Action: "sts:AssumeRole", Effect: "Allow", Principal: { Service: "lambda.amazonaws.com" } }] }),
    }, { parent: this });
    this.roleArn = role.arn;
    this.registerOutputs({ roleArn: this.roleArn });
  }
}
