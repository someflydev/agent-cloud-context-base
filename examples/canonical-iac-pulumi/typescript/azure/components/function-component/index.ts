import * as pulumi from "@pulumi/pulumi";

export interface FunctionArgs { environment: string; namePrefix: string; identityRef: pulumi.Input<string> }

export class FunctionComponent extends pulumi.ComponentResource {
  constructor(name: string, args: FunctionArgs, opts?: pulumi.ComponentResourceOptions) {
    super("accb:azure:FunctionComponent", name, {}, opts);
    const stack = pulumi.getStack();
    this.registerOutputs({ functionName: `${args.namePrefix}-${args.environment}-${stack}-handler` });
  }
}
