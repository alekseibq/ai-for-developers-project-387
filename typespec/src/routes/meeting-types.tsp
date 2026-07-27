using TypeSpec.Http;

@route("/api/v1/meeting-types")
@get op listMeetingTypes(): Result<MeetingTypeDto[]>;

@route("/api/v1/meeting-types/{id}")
@get op getMeetingType(id: string): Result<MeetingTypeDto>;

@route("/api/v1/meeting-types")
@post op createMeetingType(body: CreateMeetingTypeRequest): Result<MeetingTypeDto>;

@route("/api/v1/meeting-types/{id}")
@patch op updateMeetingType(id: string, body: UpdateMeetingTypeRequest): Result<MeetingTypeDto>;
