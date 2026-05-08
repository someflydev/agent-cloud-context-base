package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
)

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--healthcheck" {
		os.Exit(0)
	}

	e := echo.New()
	e.GET("/healthz", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]any{"ok": true, "service": "public-api-private-worker-job"})
	})
	e.GET("/readyz", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]any{"ready": true, "checks": []string{"firestore", "gcs", "pubsub", "secret-manager"}})
	})
	e.GET("/cleanup", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]any{"job": "nightly-cleanup", "expired_items_removed": 0})
	})
	e.POST("/submit", func(c echo.Context) error {
		var payload map[string]any
		_ = c.Bind(&payload)
		submissionID, _ := payload["submission_id"].(string)
		if submissionID == "" {
			submissionID = "demo-submission"
		}
		return c.JSON(http.StatusAccepted, map[string]any{
			"submission_id":     submissionID,
			"state_document":    "workflow/" + submissionID,
			"attachment_bucket": getenv("ATTACHMENT_BUCKET", "accb-dev-cloudrun-attachments"),
			"fanout_topic":      getenv("REVIEW_TOPIC", "accb-dev-cloudrun-review"),
			"callback_target":   getenv("WORKER_CALLBACK_URL", "http://127.0.0.1:8080/callback"),
		})
	})
	e.POST("/callback", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]any{
			"accepted":     true,
			"iam_audience": getenv("CALLBACK_AUDIENCE", "private-worker"),
		})
	})

	e.Logger.Fatal(e.Start(":" + getenv("PORT", "8080")))
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
