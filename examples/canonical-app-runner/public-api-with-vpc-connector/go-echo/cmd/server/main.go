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
		return c.JSON(http.StatusOK, map[string]any{"ok": true, "service": "public-api-with-vpc-connector"})
	})
	e.GET("/readyz", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]any{
			"ready":         true,
			"database_host": getenv("DB_HOST", "private-aurora.internal"),
			"secret_path":   getenv("DB_SECRET_PATH", "/accb/dev/apprunner/db"),
		})
	})
	e.POST("/suppliers", func(c echo.Context) error {
		var payload map[string]any
		_ = c.Bind(&payload)
		supplierID, _ := payload["supplier_id"].(string)
		if supplierID == "" {
			supplierID = "demo-supplier"
		}
		return c.JSON(http.StatusAccepted, map[string]any{
			"supplier_id":  supplierID,
			"db_operation": "insert",
			"connectivity": "app-runner-vpc-connector",
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
