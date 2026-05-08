FROM golang:1.22-alpine AS build
WORKDIR /app
COPY src/api/go.mod src/api/main.go ./
RUN go build -o /out/api .

FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/api /app/api
EXPOSE 8080
CMD ["/app/api"]
