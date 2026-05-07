import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface StorageArgs { environment: string; namePrefix: string }

export class StorageComponent extends pulumi.ComponentResource {
  public readonly bucketArn: pulumi.Output<string>;
  constructor(name: string, args: StorageArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:aws:StorageComponent", name, {}, opts);
    const stack = pulumi.getStack();
    const bucket = new aws.s3.Bucket(`${args.namePrefix}-${args.environment}-${stack}-artifacts`, {}, { parent: this });
    this.bucketArn = bucket.arn;
    this.registerOutputs({ bucketArn: this.bucketArn });
  }
}
