using TypeSpec.Http;

@route("/api/v1/breaks")
@get op listBreaks(): Result<BreakDto[]>;

@route("/api/v1/breaks")
@post op createBreak(body: CreateBreakRequest): Result<BreakDto>;

@route("/api/v1/breaks/{id}")
@delete op deleteBreak(id: string): Result<null>;
