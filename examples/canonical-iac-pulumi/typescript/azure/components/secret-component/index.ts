import * as pulumi from "@pulumi/pulumi";

export interface SecretArgs { environment: string; namePrefix: string }

export class SecretComponent extends pulumi.ComponentResource {
  public readonly secretId: pulumi.Output<string>;
  constructor(name: string, args: SecretArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:azure:SecretComponent", name, {}, opts);
    const stack = pulumi.getStack();
    this.secretId = pulumi.output(`${args.namePrefix}-${args.environment}-${stack}-config`);
    this.registerOutputs({ secretId: this.secretId });
  }
}
