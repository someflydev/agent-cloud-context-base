FROM golang:1.22-alpine AS build
WORKDIR /app
COPY src/cronjob/go.mod src/cronjob/main.go ./
RUN go build -o /out/cronjob .

FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/cronjob /app/cronjob
CMD ["/app/cronjob"]
