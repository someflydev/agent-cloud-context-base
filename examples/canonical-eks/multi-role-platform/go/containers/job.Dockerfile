FROM golang:1.22-alpine AS build
WORKDIR /app
COPY src/job/go.mod src/job/main.go ./
RUN go build -o /out/job .

FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/job /app/job
CMD ["/app/job"]
