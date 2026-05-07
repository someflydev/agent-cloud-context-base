import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface FunctionArgs { environment: string; namePrefix: string; roleArn: pulumi.Input<string> }

export class FunctionComponent extends pulumi.ComponentResource {
  constructor(name: string, args: FunctionArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:aws:FunctionComponent", name, {}, opts);
    const stack = pulumi.getStack();
    new aws.lambda.Function(`${args.namePrefix}-${args.environment}-${stack}-handler`, {
      role: args.roleArn,
      runtime: "python3.12",
      handler: "handler.main",
      code: new pulumi.asset.AssetArchive({ "handler.py": new pulumi.asset.StringAsset("def main(event, context): return 'ok'") }),
    }, { parent: this });
    this.registerOutputs({});
  }
}
