package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"
)

type demoRequest struct {
	StartTime string `json:"startTime"`
	EndTime   string `json:"endTime"`
}

type demoResponse struct {
	Message   string      `json:"message"`
	Method    string      `json:"method"`
	Path      string      `json:"path"`
	RequestID string      `json:"requestId,omitempty"`
	Data      demoRequest `json:"data"`
}

func logRequest(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("http request handled: method=%s path=%s duration=%s remote=%s", r.Method, r.URL.Path, time.Since(start), r.RemoteAddr)
	})
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil {
		log.Printf("encode json response: %v", err)
	}
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func demoHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	defer r.Body.Close()

	var req demoRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": fmt.Sprintf("invalid json body: %v", err),
		})
		return
	}

	writeJSON(w, http.StatusOK, demoResponse{
		Message:   "Hello from Go HTTP demo!",
		Method:    r.Method,
		Path:      r.URL.Path,
		RequestID: r.Header.Get("X-Request-ID"),
		Data:      req,
	})
}

func main() {
	addr := flag.String("addr", ":8080", "server listen address")
	flag.Parse()

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthHandler)
	mux.HandleFunc("/demo", demoHandler)

	server := &http.Server{
		Addr:              *addr,
		Handler:           logRequest(mux),
		ReadHeaderTimeout: 5 * time.Second,
	}

	log.Printf("HTTP demo server listening on %s", *addr)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("serve http: %v", err)
	}
}
