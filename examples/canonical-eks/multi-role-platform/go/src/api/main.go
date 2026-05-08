package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

func main() {
	env := getenv("ACCB_ENV", "dev")
	http.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) {
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok", "env": env})
	})
	http.HandleFunc("/ingest", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		_ = json.NewEncoder(w).Encode(map[string]string{"accepted": "true", "stream": "msk"})
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
