using TypeSpec.Http;

@route("/api/v1/bookings")
@post op createBooking(body: CreateBookingRequest): Result<BookingRichDto>;

@route("/api/v1/bookings")
@get op listBookings(@query upcoming: boolean): Result<BookingRichDto[]>;
