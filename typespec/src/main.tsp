import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

import "./models/result.tsp";
import "./models/health.tsp";
import "./models/meeting-type.tsp";
import "./models/slot.tsp";
import "./models/booking.tsp";

import "./routes/health.tsp";
import "./routes/meeting-types.tsp";
import "./routes/slots.tsp";
import "./routes/bookings.tsp";

using TypeSpec.Http;
using TypeSpec.Rest;
