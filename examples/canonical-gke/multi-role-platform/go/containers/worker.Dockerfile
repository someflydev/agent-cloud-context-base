FROM golang:1.22-alpine AS build
WORKDIR /app
COPY src/worker/go.mod src/worker/main.go ./
RUN go build -o /out/worker .

FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/worker /app/worker
CMD ["/app/worker"]
