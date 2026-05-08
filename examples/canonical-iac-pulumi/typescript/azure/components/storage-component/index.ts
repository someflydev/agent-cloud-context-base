import * as pulumi from "@pulumi/pulumi";

export interface StorageArgs { environment: string; namePrefix: string }

export class StorageComponent extends pulumi.ComponentResource {
  public readonly bucketName: pulumi.Output<string>;
  constructor(name: string, args: StorageArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:azure:StorageComponent", name, {}, opts);
    const stack = pulumi.getStack();
    this.bucketName = pulumi.output(`${args.namePrefix}-${args.environment}-${stack}-artifacts`);
    this.registerOutputs({ bucketName: this.bucketName });
  }
}
