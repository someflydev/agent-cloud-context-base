import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface SecretArgs { environment: string; namePrefix: string }

export class SecretComponent extends pulumi.ComponentResource {
  public readonly secretArn: pulumi.Output<string>;
  constructor(name: string, args: SecretArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:aws:SecretComponent", name, {}, opts);
    const stack = pulumi.getStack();
    const secret = new aws.secretsmanager.Secret(`${args.namePrefix}-${args.environment}-${stack}-config`, {}, { parent: this });
    this.secretArn = secret.arn;
    this.registerOutputs({ secretArn: this.secretArn });
  }
}
