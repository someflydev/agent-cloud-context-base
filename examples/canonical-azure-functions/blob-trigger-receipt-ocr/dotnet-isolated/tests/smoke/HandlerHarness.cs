using Accb.AzureFunctions.BlobReceiptOcr;

var result = Function.ProcessBlob(new BlobReceiptEvent(
    "receipts/harness.pdf",
    "etag-harness",
    null,
    "Contoso",
    19.95m,
    "USD"
));

if (result.CosmosDocument.Id != result.IdempotencyKey)
{
    throw new InvalidOperationException("Cosmos document id must match idempotency key");
}

if (result.CosmosDocument.BlobVersion != "etag-harness")
{
    throw new InvalidOperationException("Blob version was not preserved");
}

Console.WriteLine("dotnet blob receipt handler harness passed");
