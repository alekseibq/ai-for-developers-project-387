using TypeSpec.Http;

@route("/api/v1/slots")
@get op getSlots(
  @query date: string,
  @query meeting_type_id: string,
): Result<SlotDto[]>;
