using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/healthz", () => Results.Ok(new { status = "ok" }));
app.MapPost("/events", ([FromBody] EventPayload payload) =>
    Results.Accepted($"/events/{payload.Id}", new {
        event_id = payload.Id,
        status = "queued",
        scenario = "subscription-event-hydrator"
    }));

app.Run();

record EventPayload(string Id, string Source);
