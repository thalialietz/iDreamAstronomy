CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar,
  "fname" varchar,
  "lname" varchar,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "favorites" (
  "favorite_id" SERIAL PRIMARY KEY,
  "user_id" int,
  "asteroid_id" int
);

CREATE TABLE "asteroids" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "potentially_hazardous" boolean,
  "close_approach_date" datetime,
  "nasa_jpl_url" varchar,
  "relative_velocity_kilometers_per_hour" int,
  "relative_velocity_miles_per_hour" int,
  "orbiting_body" varchar,
  "miss_distance_kilometers" int,
  "miss_distance_miles" int,
  "estimated_diameter_kilometers_min" int,
  "estimated_diameter_kilometers_max" int,
  "estimated_diameter_miles_min" int,
  "estimated_diameter_miles_max" int
);

ALTER TABLE "favorites" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "favorites" ADD FOREIGN KEY ("asteroid_id") REFERENCES "asteroids" ("id");
