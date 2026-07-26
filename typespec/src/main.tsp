import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

import "./models/result.tsp";
import "./models/health.tsp";
import "./models/meeting-type.tsp";
import "./models/slot.tsp";
import "./models/booking.tsp";
import "./models/break.tsp";
import "./models/holiday.tsp";

import "./routes/health.tsp";
import "./routes/meeting-types.tsp";
import "./routes/slots.tsp";
import "./routes/bookings.tsp";
import "./routes/breaks.tsp";
import "./routes/holidays.tsp";

using TypeSpec.Http;
using TypeSpec.Rest;
