package main

import (
	"log"
	"os"
)

func main() {
	log.Printf("accb eks worker processing kafka lag with env=%s", getenv("ACCB_ENV", "dev"))
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
