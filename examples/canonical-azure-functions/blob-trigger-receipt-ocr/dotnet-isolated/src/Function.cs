using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;

namespace Accb.AzureFunctions.BlobReceiptOcr;

public record BlobReceiptEvent(string Name, string? Version, string? Etag, string? Merchant, decimal Total, string? Currency);
public record ReceiptDocument(string Id, string BlobName, string BlobVersion, string Merchant, decimal Total, string Currency, string OcrStatus);
public record ReceiptOcrResult(string IdempotencyKey, ReceiptDocument CosmosDocument, object EventGridEvent);

public static class Function
{
    [Function("blob-trigger-receipt-ocr")]
    public static string Run([BlobTrigger("receipts/{name}", Connection = "BlobStorageConnection")] string blob, string name)
    {
        var receipt = JsonSerializer.Deserialize<BlobReceiptEvent>(blob) ?? new BlobReceiptEvent(name, null, null, null, 0, null);
        return JsonSerializer.Serialize(ProcessBlob(receipt with { Name = receipt.Name == "" ? name : receipt.Name }));
    }

    public static ReceiptOcrResult ProcessBlob(BlobReceiptEvent receipt)
    {
        var version = receipt.Version ?? receipt.Etag ?? "noversion";
        var key = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes($"{receipt.Name}:{version}"))).ToLowerInvariant();
        var document = new ReceiptDocument(
            key,
            receipt.Name,
            version,
            receipt.Merchant ?? "unknown",
            receipt.Total,
            receipt.Currency ?? "USD",
            "completed"
        );
        var gridEvent = new
        {
            eventType = "accb.receipt.ocr.completed",
            subject = receipt.Name,
            data = new { receipt_id = key, blob_version = version }
        };
        return new ReceiptOcrResult(key, document, gridEvent);
    }
}
