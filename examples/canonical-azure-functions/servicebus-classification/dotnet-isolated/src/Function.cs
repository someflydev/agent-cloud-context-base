using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;

namespace Accb.AzureFunctions.ServiceBusClassification;

public record TicketMessage(string MessageId, string Body, int DeliveryCount);
public record ClassificationResult(string IdempotencyKey, string Team, string CosmosId, string Topic, string DlqReason);

public static class Function
{
    [Function("servicebus-classification")]
    public static string Run([ServiceBusTrigger("tickets", Connection = "ServiceBusConnection")] string message)
    {
        var ticket = JsonSerializer.Deserialize<TicketMessage>(message) ?? new TicketMessage("missing", "", 0);
        return JsonSerializer.Serialize(Classify(ticket));
    }

    public static ClassificationResult Classify(TicketMessage ticket)
    {
        var key = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(ticket.MessageId))).ToLowerInvariant();
        var team = ticket.Body.Contains("billing", StringComparison.OrdinalIgnoreCase) ? "billing" : "support";
        var dlqReason = ticket.DeliveryCount > 5 ? "max-delivery-exceeded" : "";
        return new ClassificationResult(key, team, $"ticket-{key}", $"team-{team}", dlqReason);
    }
}
