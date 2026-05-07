using System.Text.Json;

if (args.Contains("--healthcheck"))
{
    return;
}

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var serviceName = "aca-dapr-pubsub-binding";

app.MapGet("/healthz", () => Results.Json(new { ok = true, service = serviceName }));

app.MapGet("/readyz", () => Results.Json(new
{
    ready = true,
    checks = new[] { "dapr-sidecar", "service-bus-pubsub", "cosmos-state", "key-vault-secret-store" }
}));

app.MapPost("/orders", (JsonElement payload) =>
{
    var orderId = payload.TryGetProperty("orderId", out var value) ? value.GetString() : "demo-order";
    return Results.Accepted("/orders-handler", new
    {
        orderId,
        pubsub = Environment.GetEnvironmentVariable("DAPR_PUBSUB_NAME") ?? "servicebus-pubsub",
        topic = Environment.GetEnvironmentVariable("DAPR_TOPIC") ?? "orders",
        stateStore = Environment.GetEnvironmentVariable("DAPR_STATE_STORE") ?? "cosmos-state",
        secretStore = Environment.GetEnvironmentVariable("DAPR_SECRET_STORE") ?? "keyvault-secrets"
    });
});

app.MapPost("/orders-handler", (JsonElement payload) =>
{
    var eventId = payload.TryGetProperty("id", out var id) ? id.GetString() : "local-event";
    return Results.Json(new
    {
        handled = true,
        replayKey = eventId,
        stateBinding = "cosmos-state",
        secretBinding = "keyvault-secrets"
    });
});

app.Run();
