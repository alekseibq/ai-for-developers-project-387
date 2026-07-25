using TypeSpec.Http;

@route("/api/v1/meeting-types")
@get op listMeetingTypes(): Result<MeetingTypeDto[]>;

@route("/api/v1/meeting-types")
@post op createMeetingType(body: CreateMeetingTypeRequest): Result<MeetingTypeDto>;
