import crypto from "node:crypto";

export type BlobReceiptEvent = {
  name: string;
  version?: string;
  etag?: string;
  content_type?: string;
  bytes_len?: number;
  merchant?: string;
  total?: number;
  currency?: string;
};

export function processBlob(event: BlobReceiptEvent) {
  const version = event.version ?? event.etag ?? "noversion";
  const idempotencyKey = crypto.createHash("sha256").update(`${event.name}:${version}`).digest("hex");
  const receipt = {
    id: idempotencyKey,
    blob_name: event.name,
    blob_version: version,
    merchant: event.merchant ?? "unknown",
    total: event.total ?? 0,
    currency: event.currency ?? "USD",
    ocr_status: "completed"
  };
  return {
    idempotency_key: idempotencyKey,
    cosmos_document: receipt,
    event_grid_event: {
      eventType: "accb.receipt.ocr.completed",
      subject: event.name,
      data: {
        receipt_id: idempotencyKey,
        blob_version: version
      }
    },
    log: {
      provider: "azure",
      service: "azure-functions",
      example: "blob-trigger-receipt-ocr",
      idempotency_key: idempotencyKey
    }
  };
}
