using System.Text.Json;

var role = "job";
var eventId = Environment.GetEnvironmentVariable("ACCB_EVENT_ID") ?? "local";
var result = new {
    role,
    event_id = eventId,
    status = "accepted",
    environment = Environment.GetEnvironmentVariable("ACCB_ENV") ?? "dev"
};

Console.WriteLine(JsonSerializer.Serialize(result));
