using TypeSpec.Http;

@route("/api/v1/health")
@get op health(): Result<HealthResponse>;
