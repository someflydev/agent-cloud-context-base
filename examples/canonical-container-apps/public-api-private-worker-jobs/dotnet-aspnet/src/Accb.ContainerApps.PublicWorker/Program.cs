using System.Text.Json;

if (args.Contains("--healthcheck"))
{
    return;
}

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var serviceName = "aca-public-api-private-worker-jobs-dotnet";

app.MapGet("/healthz", () => Results.Json(new { ok = true, service = serviceName }));

app.MapGet("/readyz", () => Results.Json(new
{
    ready = true,
    checks = new[] { "cosmos", "blob-storage", "service-bus", "key-vault", "managed-identity" }
}));

app.MapGet("/retry", () => Results.Json(new
{
    job = "servicebus-batch-retry",
    trigger = "servicebus",
    keda_rule = "queueLength >= 5",
    retried = 0
}));

app.MapPost("/submit", (JsonElement payload) =>
{
    var submissionId = payload.TryGetProperty("submission_id", out var value) ? value.GetString() : "demo-submission";
    return Results.Accepted("/process", new
    {
        submission_id = submissionId,
        state_container = Environment.GetEnvironmentVariable("COSMOS_CONTAINER") ?? "workflow",
        attachment_container = Environment.GetEnvironmentVariable("ATTACHMENT_CONTAINER") ?? "attachments",
        work_queue = Environment.GetEnvironmentVariable("SERVICEBUS_QUEUE") ?? "accb-dev-aca-work",
        worker_url = Environment.GetEnvironmentVariable("WORKER_URL") ?? "http://worker.internal/process",
        scale_signal = "keda-servicebus-queue-depth"
    });
});

app.MapPost("/process", (JsonElement payload) =>
{
    var messageId = payload.TryGetProperty("message_id", out var value) ? value.GetString() : "local-message";
    return Results.Json(new
    {
        accepted = true,
        internal_ingress = true,
        message_id = messageId,
        secret_ref = Environment.GetEnvironmentVariable("API_SECRET_NAME") ?? "keyvaultref:api-key"
    });
});

app.Run();
