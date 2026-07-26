using TypeSpec.Http;

@route("/api/v1/holidays")
@get op listHolidays(): Result<HolidayDto[]>;

@route("/api/v1/holidays")
@post op createHoliday(body: CreateHolidayRequest): Result<HolidayDto>;

@route("/api/v1/holidays/{id}")
@delete op deleteHoliday(id: string): Result<null>;
