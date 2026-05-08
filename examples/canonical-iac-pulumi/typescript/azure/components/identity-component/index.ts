import * as pulumi from "@pulumi/pulumi";

export interface IdentityArgs {
  environment: string;
  namePrefix: string;
  storageName: pulumi.Input<string>;
  eventingName: pulumi.Input<string>;
  secretRef: pulumi.Input<string>;
}

export class IdentityComponent extends pulumi.ComponentResource {
  public readonly serviceAccountEmail: pulumi.Output<string>;
  constructor(name: string, args: IdentityArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:azure:IdentityComponent", name, {}, opts);
    const stack = pulumi.getStack();
    this.serviceAccountEmail = pulumi.output(`${args.namePrefix}-${args.environment}-${stack}-runtime`);
    this.registerOutputs({ serviceAccountEmail: this.serviceAccountEmail });
  }
}
